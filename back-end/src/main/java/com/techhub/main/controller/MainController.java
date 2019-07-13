package com.techhub.main.controller;

import com.techhub.main.entity.Info;
import com.techhub.main.entity.ResponseData;
import com.techhub.main.solrj.SolrJClient;
import org.apache.solr.common.SolrDocument;
import org.apache.solr.common.SolrDocumentList;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.*;

/**
 * @author ：Chen Xin
 * @date ：Created in 2019/7/8 10:52
 * @modified By：
 */
@RestController
public class MainController {
    private static Logger log = LoggerFactory.getLogger(MainController.class);

    @Value("${SolrJ.coreName}")
    private String coreName;

    private final SolrJClient solrJClient;

    @Autowired
    public MainController(SolrJClient solrJClient) {
        this.solrJClient = solrJClient;
    }

    @GetMapping("/search")
    public ResponseData search(@RequestParam("key") String key, @RequestParam("catalog") int catalog, @RequestParam("page") int page, @RequestParam("size") int size) {
        log.info("in search");

        HashMap<String, String> titleMap = new HashMap<>();
        titleMap.put("rows", "200"); // 默认只找200个
//        titleMap.put("start", String.valueOf((page - 1) * size));
        titleMap.put("fl", "*, score");
        if (catalog == -1) { // 直接对题目和正文进行搜索
            titleMap.put("q", "title:" + key);
        } else {
            titleMap.put("q", "title:" + key + " AND catalog:" + catalog);
        }
        List<Info> titleResult = searchAndReturn(titleMap, 0.6);


        HashMap<String, String> contentMap = new HashMap<>();
        contentMap.put("rows", "200"); // 默认只找200个
//        contentMap.put("start", String.valueOf((page - 1) * size));
        contentMap.put("fl", "*, score");
        if (catalog == -1) { // 直接对题目和正文进行搜索
            contentMap.put("q", "title:" + key);
        } else {
            contentMap.put("q", "title:" + key + " AND catalog:" + catalog);
        }
        List<Info> contentResult = searchAndReturn(contentMap, 0.4);

        List<Info> result = new ArrayList<>(titleResult);
        for (Info tmp: contentResult) {
            int index = result.indexOf(tmp);
            if (index == -1) {
                result.add(tmp);
            } else {
                Info existInfo =  result.get(index);
                existInfo.setScore(existInfo.getScore() + tmp.getScore());
            }
        }

        result.sort((info1, info2) -> info1.getScore() > info2.getScore() ? 1 : (info1.getScore() < info2.getScore()) ? -1 : 0);

        List<Info> real_result = new ArrayList<>();

        for (int i=(page-1)*size;i<result.size();i+=size) {
            for (int j=i;j<result.size() && j<i+size;j++) {
                real_result.add(result.get(j));
            }
        }

        ResponseData responseData = ResponseData.ok();
        responseData.putDataValue("result", real_result);
        responseData.putDataValue("total", result.size());
        return responseData;
    }

    @GetMapping("/getAllTag")
    public ResponseData getAllTag(@RequestParam("key") String key, @RequestParam("page") int page, @RequestParam("size") int size) {

        return null;
    }

    // help function
    private List<Info> searchAndReturn(HashMap<String, String> map, double rate) {
        SolrDocumentList solrDocumentList = solrJClient.query(map, coreName);
        List<Info> result = new ArrayList<>();
        if (solrDocumentList == null) {
            return result;
        }

        for (SolrDocument i: solrDocumentList) {
            String _id = (String) i.getFieldValue("_id");
            String title = (String) i.getFieldValue("title");
            String summary = (String) i.getFieldValue("summary");
            String url = (String) i.getFieldValue("url");
            List<String> tags = (List<String>) i.getFieldValue("tags");
            Integer _catalog = (Integer) i.getFieldValue("catalog");
            String content = (String) i.getFieldValue("content");
            String source = (String) i.getFieldValue("source");
            String date = (String) i.getFieldValue("date");
            String author = (String) i.getFieldValue("author");
            Double score = (Double)  i.getFieldValue("score") * rate;
            Info info = new Info(_id, title, summary, url, tags, _catalog, content, source, date, author, score);
            result.add(info);
        }

        return result;
    }

}

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
//        map.put("fl", "store_book_id");

        Set<Info> result = new HashSet<>();

        HashMap<String, String> titleMap = new HashMap<>();
        titleMap.put("rows", String.valueOf(size));
        titleMap.put("start", String.valueOf((page - 1) * size));
        if (catalog == -1) { // 直接对题目和正文进行搜索
            titleMap.put("q", "title:" + key);
        } else {
            titleMap.put("q", "title:" + key + " AND catalog:" + catalog);
        }
        Set<Info> titleResult = searchAndReturn(titleMap);


        HashMap<String, String> contentMap = new HashMap<>();
        contentMap.put("rows", String.valueOf(size));
        contentMap.put("start", String.valueOf((page - 1) * size));
        if (catalog == -1) { // 直接对题目和正文进行搜索
            contentMap.put("q", "title:" + key);
        } else {
            contentMap.put("q", "title:" + key + " AND catalog:" + catalog);
        }
        Set<Info> contentResult = searchAndReturn(contentMap);

        result.addAll(titleResult);
        result.addAll(contentResult);


        ResponseData responseData = ResponseData.ok();
        responseData.putDataValue("result", result);
        return responseData;
    }

    private Set<Info> searchAndReturn(HashMap<String, String> map) {
        SolrDocumentList solrDocumentList = solrJClient.query(map, coreName);
        Set<Info> result = new HashSet<>();
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
            Info info = new Info(_id, title, summary, url, tags, _catalog, content, source, date, author);
            result.add(info);
        }

        return result;
    }
}

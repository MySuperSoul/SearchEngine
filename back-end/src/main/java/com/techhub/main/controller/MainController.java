package com.techhub.main.controller;

import com.techhub.main.entity.*;
import com.techhub.main.service.InfoService;
import com.techhub.main.service.MongoService;
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

import java.sql.Timestamp;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
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

    private final InfoService infoService;

    private final MongoService mongoService;

    @Autowired
    public MainController(SolrJClient solrJClient, InfoService infoService, MongoService mongoService) {
        this.solrJClient = solrJClient;
        this.infoService = infoService;
        this.mongoService = mongoService;
    }

    // delta 0:所有 1:一天内 2:一周内 3:一月内 4:一年内
    @GetMapping("/search")
    public ResponseData search(@RequestParam("key") String key, @RequestParam("catalog") int catalog, @RequestParam("page") int page, @RequestParam("size") int size, @RequestParam("delta") int delta) {
        log.info("in search");
        long currentTimestamps = System.currentTimeMillis() / 1000;
        long first = System.currentTimeMillis() / 1000;
        HashMap<String, String> titleMap = new HashMap<>();
        titleMap.put("rows", "100"); // 默认只找100个
        titleMap.put("fl", "_id, title, summary, url, tags, catalog, source, date, author, score");
        if (catalog == -1) { // 直接对题目和正文进行搜索
            titleMap.put("q", "title:" + key);
        } else {
            titleMap.put("q", "title:" + key + " AND catalog:" + catalog);
        }
        List<Info> titleResult = searchAndReturn(titleMap, 0.6f);
        long second = System.currentTimeMillis() / 1000;
        log.info("第一次solr查询所用时间: " + String.valueOf(second - first));


        HashMap<String, String> contentMap = new HashMap<>();
        contentMap.put("rows", "100"); // 默认只找100个
        contentMap.put("fl", "_id, title, summary, url, tags, catalog, source, date, author, score");
        if (catalog == -1) { // 直接对题目和正文进行搜索
            contentMap.put("q", "content:" + key);
        } else {
            contentMap.put("q", "content:" + key + " AND catalog:" + catalog);
        }
        List<Info> contentResult = searchAndReturn(contentMap, 0.4f);
        long third = System.currentTimeMillis() / 1000;
        log.info("第二次solr查询所用时间: " + String.valueOf(third - second));


        List<Info> result = new ArrayList<>(titleResult);
        for (Info tmp: contentResult) {
            int index = result.indexOf(tmp);
            if (index == -1) {
                if (delta == 0) {
                    result.add(tmp);
                } else if (delta == 1) {
                    if (currentTimestamps - toTimeStamp(tmp.getDate()) <= 60 * 60 * 24) result.add(tmp);
                } else if (delta == 2) {
                    if (currentTimestamps - toTimeStamp(tmp.getDate()) <= 60 * 60 * 24 * 7) result.add(tmp);
                } else if (delta == 3) {
                    if (currentTimestamps - toTimeStamp(tmp.getDate()) <= 60 * 60 * 24 * 30) result.add(tmp);
                } else if (delta == 4) {
                    if (currentTimestamps - toTimeStamp(tmp.getDate()) <= 60 * 60 * 24 * 365) result.add(tmp);
                }
            } else {
                Info existInfo =  result.get(index);
                existInfo.setScore(existInfo.getScore() + tmp.getScore());
            }
        }

        result.sort((info1, info2) -> info1.getScore() > info2.getScore() ? 1 : (info1.getScore() < info2.getScore()) ? -1 : 0);

        // 多于100，取前100
        if (result.size() > 100) {
            result = result.subList(0, 100);
        }

        List<Info> real_result = new ArrayList<>();
        for (int i=(page-1)*size ; i<result.size() && i<page+size ; i++) {
            real_result.add(result.get(i));
        }

        long fourth = System.currentTimeMillis() / 1000;
        log.info("总共所用时间: " + String.valueOf(fourth - first));

        ResponseData responseData = ResponseData.ok();
        responseData.putDataValue("result", real_result);
        responseData.putDataValue("total", result.size());
        return responseData;
    }

    @GetMapping("/getAllTag")
    public ResponseData getAllTag(@RequestParam("key") String key, @RequestParam("page") int page, @RequestParam("size") int size) {
        log.info("in getAllTag");
        log.info(key);
        log.info(String.valueOf(page));
        log.info(String.valueOf(size));
        ResponseData responseData = ResponseData.ok();
        if (key.length() == 0) {
            Integer total = infoService.getAllTagsCount();
            List<TagCountMap> tags = infoService.getAllTags(page, size);

            responseData.putDataValue("result", tags);
            responseData.putDataValue("total", total);
            return responseData;
        } else {
            Integer total = infoService.getTagCount(key);
            List<Infos> list = infoService.getTag(key, (page - 1) * size, size);
            List<MongoDoc> result = new ArrayList<>();
            for (Infos i: list) {
                result.add(mongoService.getDocById(i.get_id()));
            }

            responseData.putDataValue("result", result);
            responseData.putDataValue("total", total);
            return responseData;
        }
    }

    // help function
    private List<Info> searchAndReturn(HashMap<String, String> map, float rate) {
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
            Float score = (Float)  i.getFieldValue("score") * rate;
            Info info = new Info(_id, title, summary, url, tags, _catalog, content, source, date, author, score);
            result.add(info);
        }

        return result;
    }

    private long toTimeStamp(String date) {
        if (date.length() == 0) {
            return 0;
        }
        DateFormat format = new SimpleDateFormat("yyyy-MM-dd");
        format.setLenient(false);
        try {
            Timestamp ts = new Timestamp(format.parse(date).getTime());
            return ts.getTime() / 1000;
        } catch (ParseException e) {
            e.printStackTrace();
            return 0;
        }
    }
}

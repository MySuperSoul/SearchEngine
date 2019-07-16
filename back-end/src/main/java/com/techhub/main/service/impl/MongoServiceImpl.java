package com.techhub.main.service.impl;

import com.techhub.main.entity.MongoDoc;
import com.techhub.main.service.MongoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;

/**
 * @author ：Chen Xin
 * @date ：Created in 2019/7/14 11:46
 * @modified By：
 */
@Service(value = "MongoService")
public class MongoServiceImpl implements MongoService {
    private final MongoTemplate mongoTemplate;

    @Autowired
    public MongoServiceImpl(MongoTemplate mongoTemplate) {
        this.mongoTemplate = mongoTemplate;
    }

    @Override
    public MongoDoc getDocById(String id) {
        Query query = new Query(Criteria.where("_id").is(id));
        return mongoTemplate.findOne(query, MongoDoc.class);
    }
}

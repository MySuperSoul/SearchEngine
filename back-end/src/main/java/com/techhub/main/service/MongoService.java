package com.techhub.main.service;

import com.techhub.main.entity.MongoDoc;

import java.util.List;

public interface MongoService {
    MongoDoc getDocById(String id);
}

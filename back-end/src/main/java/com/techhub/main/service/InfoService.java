package com.techhub.main.service;

import com.techhub.main.entity.Infos;

import java.util.List;

public interface InfoService {
    List<String> getAllTags();
    List<Infos> getTag(String tag);
    Integer getTagCount(String tag);
}

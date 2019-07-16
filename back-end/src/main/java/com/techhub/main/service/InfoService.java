package com.techhub.main.service;

import com.techhub.main.entity.Infos;
import com.techhub.main.entity.TagCountMap;

import java.util.List;

public interface InfoService {
    List<TagCountMap> getAllTags(int page, int size);
    Integer getAllTagsCount();
    List<Infos> getTag(String tag, int page, int size);
    Integer getTagCount(String tag);
}

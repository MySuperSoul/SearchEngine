package com.techhub.main.dao;

import com.techhub.main.entity.Infos;
import com.techhub.main.entity.TagCountMap;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface InfoDao {
    List<TagCountMap> getAllTags(@Param("page") int page, @Param("size") int size);
    Integer getAllTagsCount();
    List<Infos> getTag(@Param("tag") String tag, @Param("page") int page, @Param("size") int size);
    Integer getTagCount(@Param("tag") String tag);
}

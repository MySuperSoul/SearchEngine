package com.techhub.main.dao;

import com.techhub.main.entity.Infos;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface InfoDao {
    List<String> getAllTags();
    List<Infos> getTag(@Param("tag") String tag);
    Integer getTagCount(@Param("tag") String tag);
}

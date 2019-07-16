package com.techhub.main.service.impl;

import com.techhub.main.dao.InfoDao;
import com.techhub.main.entity.Infos;
import com.techhub.main.entity.TagCountMap;
import com.techhub.main.service.InfoService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author ：Chen Xin
 * @date ：Created in 2019/7/14 10:49
 * @modified By：
 */
@Service(value = "InfoService")
public class InfoServiceImpl implements InfoService {
    private static Logger log = LoggerFactory.getLogger(InfoServiceImpl.class);

    @Autowired
    private final InfoDao infoDao;

    public InfoServiceImpl(InfoDao infoDao) {
        this.infoDao = infoDao;
    }

    @Override
    public List<TagCountMap> getAllTags(int page, int size) {
        log.info("in getAllTags");
        return infoDao.getAllTags(page, size);
    }

    @Override
    public Integer getAllTagsCount() {
        log.info("in getAllTagsCount");
        Integer result = infoDao.getAllTagsCount();
        log.info("count: " + result);
        return result;
    }

    @Override
    public List<Infos> getTag(String tag, int page, int size) {
        log.info("in getTag");
        return infoDao.getTag(tag, page, size);
    }

    @Override
    public Integer getTagCount(String tag) {
        log.info("in getTagCount");
        Integer result = infoDao.getTagCount(tag);
        log.info("count: " + result);
        return result;
    }
}

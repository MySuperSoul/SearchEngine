package com.techhub.main.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * @author ：Chen Xin
 * @date ：Created in 2019/7/8 11:16
 * @modified By：
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Info {
    private String _id; // 唯一id
    private String title; // 文章名
    private String summary; // 摘要
    private String url; // 链接
    private List<String> tags; // 标签
    private Integer catalog; // 分类 0介绍，1使用手册，2源码分析，3demo，4教学视频，5相关问题
    private String content; // 正文
    private String source; // 来源
    private String date; // 发布日期
    private String author; // 作者
    private Float score; // 相关性评分

    @Override
    public int hashCode() {
        return _id.hashCode(); // 用_id来区分不同的Info
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;

        if (obj == null) return false;

        if (getClass() != obj.getClass()) return false;

        Info other = (Info) obj;
        return _id.equals(other.get_id());
    }
}


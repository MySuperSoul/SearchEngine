package com.techhub.main.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.util.List;

/**
 * @author ：Chen Xin
 * @date ：Created in 2019/7/14 11:30
 * @modified By：
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@Document(collection = "infos")
public class MongoDoc {
    @Id
    private String _id;

    @Field("title")
    private String title;

    @Field("summary")
    private String summary;

    @Field("url")
    private String url;

    @Field("tags")
    private List<String> tags;

    @Field("catalog")
    private Integer catalog;

    @Field("content")
    private String content;

    @Field("source")
    private String source;

    @Field("date")
    private String date;

    @Field("author")
    private String author;
}

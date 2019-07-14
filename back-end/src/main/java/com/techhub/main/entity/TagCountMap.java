package com.techhub.main.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * @author ：Chen Xin
 * @date ：Created in 2019/7/14 12:54
 * @modified By：
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class TagCountMap {
    private String tag;
    private Integer count;
}

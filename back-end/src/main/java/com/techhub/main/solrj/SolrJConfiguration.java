package com.techhub.main.solrj;

import org.apache.solr.client.solrj.impl.HttpSolrClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * @author ：Chen Xin
 * @date ：Created in 2019/7/8 10:52
 * @modified By：
 */
@Configuration
public class SolrJConfiguration {
    @Value("${SolrJ.url}")
    private String SOLR_URL;

    @Bean(name = "SolrJ.pool")
    public HttpSolrClient solrJPool() {
        return new HttpSolrClient.Builder(SOLR_URL)
                .withConnectionTimeout(10000)
                .withSocketTimeout(60000)
                .build();
    }
}

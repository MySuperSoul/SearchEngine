package com.techhub.main.solrj;

import org.apache.solr.client.solrj.impl.HttpSolrClient;
import org.apache.solr.client.solrj.response.QueryResponse;
import org.apache.solr.common.SolrDocumentList;
import org.apache.solr.common.params.MapSolrParams;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Map;

/**
 * @author ：Chen Xin
 * @date ：Created in 2019/7/8 10:53
 * @modified By：
 */
@Component
public class SolrJClient {
    @Value("${SolrJ.url}")
    private String SOLR_URL;

    private final HttpSolrClient solrJPool;

    @Autowired
    public SolrJClient(HttpSolrClient solrJPool) {
        this.solrJPool = solrJPool;
    }

    // q   *:*
    // fl  my_id, my_name
    public SolrDocumentList query(Map<String, String> queryParamMap, String coreName) {
        MapSolrParams queryParams = new MapSolrParams(queryParamMap);
        try {
            final QueryResponse response = solrJPool.query(coreName, queryParams);
            return response.getResults();
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    // 默认clean
    public boolean dataImport(String coreName, String entity) {
        try {
            String body = "command=full-import&verbose=false&clean=true&commit=true&core=" + coreName + "&entity=" + entity + "&name=dataimport";
            String url = SOLR_URL + "/" + coreName + "/dataimport?indent=on&wt=json";
            URL obj = new URL(url);
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
            con.setRequestProperty("Content-type", "application/x-www-form-urlencoded");
            con.setRequestProperty("Content-Length", String.valueOf(body.getBytes().length));
            con.setDoOutput(true);
            con.setDoInput(true);
            PrintWriter out = new PrintWriter(con.getOutputStream());
            out.print(body);
            out.flush();

            return con.getResponseCode() == 200;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

}
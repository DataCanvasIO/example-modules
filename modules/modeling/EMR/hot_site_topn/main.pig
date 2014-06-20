
raw_data = LOAD '$INPUT_query_log_s3_dir' USING PigStorage('\t') AS (id:chararray,query:chararray,querytime:chararray,rank:int,url:chararray) ;

url_data = FILTER raw_data BY url is not null;

site_data = FOREACH url_data GENERATE com.zetdata.udf.ExtractSite(url) AS site;

--Filter out the records which is not attached with a url
site_data = FILTER site_data BY site != '';

grouped_site = GROUP site_data BY site;

site_count = FOREACH grouped_site GENERATE group, COUNT(site_data) AS num;

ordered_site_count = ORDER site_count BY num DESC;

topN_site = LIMIT ordered_site_count $PARAM_topN;

STORE topN_site INTO '$OUTPUT_hot_site_topN_s3_dir' USING PigStorage('\t');


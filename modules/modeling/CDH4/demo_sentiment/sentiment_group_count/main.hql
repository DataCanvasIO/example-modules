DROP TABLE IF EXISTS ${MYNS}_senti_results;
CREATE EXTERNAL TABLE ${MYNS}_senti_results
    COMMENT "A table backed by Avro data with the Avro schema embedded in the CREATE TABLE statement"
    ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.avro.AvroSerDe'
    STORED AS
    INPUTFORMAT  'org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat'
    OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat'
    LOCATION '${INPUT_avro_path}'
    TBLPROPERTIES (
        'avro.schema.literal'='
      { "doc" : "A key/value pair",
  "fields" : [ { "doc" : "The key",
        "name" : "key",
        "type" : "string"
      },
      { "doc" : "The value",
        "name" : "value",
        "type" : { "fields" : [ { "name" : "text",
                  "type" : "string"
                },
                { "name" : "sentiment",
                  "type" : "string"
                },
                { "name" : "sentiment_vector",
                  "type" : { "items" : "double",
                      "type" : "array"
                    }
                }
              ],
            "name" : "NlpResult",
            "namespace" : "com.zetdata.avro",
            "type" : "record"
          }
      }
    ],
  "name" : "KeyValuePair",
  "namespace" : "org.apache.avro.mapreduce",
  "type" : "record"
}'
    );

DROP TABLE IF EXISTS ${OUTPUT_group_count_table};
CREATE TABLE ${OUTPUT_group_count_table}
AS
SELECT value.sentiment, count(value.sentiment) AS sentiment_count
FROM ${MYNS}_senti_results
GROUP BY value.sentiment;




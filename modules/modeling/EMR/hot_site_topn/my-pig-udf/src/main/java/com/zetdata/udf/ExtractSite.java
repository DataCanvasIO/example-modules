package com.zetdata.udf;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.pig.EvalFunc;
import org.apache.pig.data.DataType;
import org.apache.pig.data.Tuple;
import org.apache.pig.impl.logicalLayer.schema.Schema;
import org.apache.pig.impl.logicalLayer.schema.Schema.FieldSchema;

public class ExtractSite extends EvalFunc<String> {

    String pattern = "^http://(www\\.)?([a-zA-Z0-9\\-\\.]+)\\.(com|org|net|mil|edu|COM|ORG|NET|MIL|EDU)$";
    Pattern p = Pattern.compile(pattern);
    
    @Override
        public Schema outputSchema(Schema input) {
        if (input.size() != 1) {
            throw new RuntimeException("Expected (chararray), input does not have 1 field");
        }
        try {
            // Get the types for both columns and check them. If they are
            // wrong, figure out what types were passed and give a good error
            // message.
            if (input.getField(0).type != DataType.CHARARRAY ) {
                String msg = "Expected input (chararray), received schema (";
                msg += DataType.findTypeName(input.getField(0).type);
                msg += ")";
                throw new RuntimeException(msg);
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        // Construct our output schema, which is one field that is a long
        List schemas =new ArrayList<FieldSchema>();
        schemas.add(new FieldSchema("site", DataType.CHARARRAY));
        return new Schema(schemas);
    }
    @Override
        public String exec(Tuple tuple) throws IOException {
        try {
            String url = (String)tuple.get(0);
            Matcher matcher = p.matcher(url);
            String site = "";
            if(matcher.find()) site = matcher.group(2);
            return site;
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            throw new IOException("Extract Site exception",e);
        }
    }
}


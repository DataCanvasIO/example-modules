package com.zetdata.udf;

import java.util.ArrayList;

import org.apache.hadoop.hive.ql.exec.UDFArgumentException;
import org.apache.hadoop.hive.ql.exec.UDFArgumentLengthException;
import org.apache.hadoop.hive.ql.metadata.HiveException;
import org.apache.hadoop.hive.ql.udf.generic.GenericUDTF;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspector;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspectorFactory;
import org.apache.hadoop.hive.serde2.objectinspector.StructObjectInspector;
import org.apache.hadoop.hive.serde2.objectinspector.primitive.PrimitiveObjectInspectorFactory;

public class SplitWord extends GenericUDTF{

       @Override
       public void close() throws HiveException {
               // TODO Auto-generated method stub
       }

       @Override
       public StructObjectInspector initialize(ObjectInspector[] args)
                       throws UDFArgumentException {
               // Check input here.Query is expected.
               if(args.length!=1){
                       throw new UDFArgumentLengthException("SplitWord UDTF takes only one argument");
               }

               //Check the Category.
               if(args[0].getCategory()!=ObjectInspector.Category.PRIMITIVE){
                       throw new UDFArgumentException("SplitWord UDTF takes string as a parameter");
               }

               ArrayList<String> fileNames = new ArrayList<String>();
               ArrayList<ObjectInspector> fieldOIs = new ArrayList<ObjectInspector>();
               fileNames.add("token");
               fieldOIs.add(PrimitiveObjectInspectorFactory.javaStringObjectInspector);

               return ObjectInspectorFactory.getStandardStructObjectInspector(fileNames, fieldOIs);
       }

       @Override
       public void process(Object[] arg) throws HiveException {
               // Split Word and filter out 'com', 'www'
               if(arg[0].toString()==null||arg[0].toString().trim().equals("")) return;
               String query = arg[0].toString();
               String[] tokens = query.split(" ");
               for (String t : tokens) {
                               forward(new Object[]{t});
               }
       }

}

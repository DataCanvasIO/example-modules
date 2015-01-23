#!/bin/bash


screwjack run docker \
    --param-query="SELECT * FROM books;" \
    --DB="unittests/db_pg.json" \
    --O=tmp_pg.csv


screwjack run docker \
    --param-query="SELECT * FROM employees;" \
    --DB="unittests/db_mysql.json" \
    --O=tmp_mysql.csv


screwjack run docker \
    --param-query="SELECT * FROM Employee;" \
    --DB="unittests/db_sqlite.json" \
    --O=tmp_sqlite.csv


# echo "This case should be failed"
# screwjack run docker \
#     --param-query="SELECT * FROM employees;" \
#     --DB="unittests/db_oracle.json" \
#     --O=tmp_mysql.csv



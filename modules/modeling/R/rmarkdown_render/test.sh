#!/bin/bash


TEMP_BANK_ZIP=bank.zip
DEST_FILE=bank-full.csv

if [ ! -f $DEST_FILE ]; then
    wget -O $TEMP_BANK_ZIP https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip
    unzip -p $TEMP_BANK_ZIP bank-full.csv > $DEST_FILE
    rm -f $TEMP_BANK_ZIP
fi


cp -f report.Rmd io_4


# screwjack run local \
# screwjack run docker-machine \
screwjack run docker \
    --param-csv_sep ";" \
    --param-csv_header "TRUE" \
    --ds bank-full.csv \
    --rmd_report io_4 \
    --output_report output_report

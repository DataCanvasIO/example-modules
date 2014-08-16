#!/bin/sh

touch output.sbuxPrices.forecast.csv
touch output.sbux.forecast.pdf

# screwjack --full-build run docker \
screwjack run docker \
    --param-column_name="Adj.Close" \
    --param-start="1993 3" \
    --param-end="2008 3" \
    --param-frequency="12" \
    --param-forecast_number="10" \
    --TimeSeries sbuxPrices.csv \
    --Forecast output.sbuxPrices.forecast.csv \
    --PlotPdf output.sbux.forecast.pdf

# The local run works on a ubuntu.trusty with R and forecast library installed.
#sudo screwjack run local --TimeSeries sbuxPrices.csv --Forecast sbuxPrices.forecast.csv

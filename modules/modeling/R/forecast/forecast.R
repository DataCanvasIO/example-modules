
# Reference:
# http://faculty.washington.edu/ezivot/econ424/Working%20with%20Time%20Series%20Data%20in%20R.pdf

library(forecast)

inputTsFile = commandArgs(TRUE)[1]
print("loading input time series file: ")
print(inputTsFile)

mydata.df = read.csv(inputTsFile, header = TRUE, stringsAsFactors = FALSE)

paramColumnName = commandArgs(TRUE)[3]
paramStart = scan(text=commandArgs(TRUE)[4])
paramEnd = scan(text=commandArgs(TRUE)[5])
paramFreq = scan(text=commandArgs(TRUE)[6])
mydata.ts = ts(data=mydata.df[[paramColumnName]], frequency = paramFreq, start=paramStart, end=paramEnd)

mydata.fit<-arima(mydata.ts, order=c(1,0,1))

paramForecastCount = scan(text=commandArgs(TRUE)[7])
print(paramForecastCount)
mydata.forecast = forecast(mydata.fit, h=paramForecastCount)

# Plot
paramEnd = commandArgs(TRUE)[8]
pdf(paramEnd)
plot(mydata.forecast)
dev.off()

outputForecastResultFile = commandArgs(TRUE)[2]
write.csv(mydata.forecast, file=outputForecastResultFile)

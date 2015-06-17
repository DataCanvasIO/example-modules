
# forecast with R runtime

library(RDataCanvas)

getwd()

# First, Create a runtime object
rt <- DCRuntime()
print(jsonlite::toJSON(unclass(rt), pretty=TRUE, auto_unbox=TRUE))

library(rmarkdown)

# TODO: walk-around, the rmarkdown::render requires a ".Rmd" suffix
input_temp_filename = tempfile(fileext=".Rmd")
file.copy(rt$Input$rmd_report$Val, input_temp_filename)


render(input_temp_filename, params = list(
  csv_file = rt$Input$ds$Val,
  csv_sep = rt$Param$csv_sep$Val,
  csv_header = as.logical(rt$Param$csv_header)
), output_file = rt$Output$output_report$Val)

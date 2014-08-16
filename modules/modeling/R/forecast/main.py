#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import get_settings_from_file
import os
import sys
from subprocess import call

def main():
    settings = get_settings_from_file("spec.json")
    print(settings)

    command = '/usr/bin/Rscript forecast.R {} {} "{}" "{}" "{}" "{}" "{}" {}'.format(settings.Input.TimeSeries, settings.Output.Forecast, settings.Param.column_name, settings.Param.start, settings.Param.end, settings.Param.frequency, settings.Param.forecast_number, settings.Output.PlotPdf)
    ret = call(command, shell=True)
    if ret != 0:
        sys.exit(ret)
    # command = "/usr/bin/Rscript forecast.R {} {}".format(settings.Input.TimeSeries, settings.Output.Forecast)
    # print(command)
    # os.system(command);

    print("Done")

if __name__ == "__main__":
    main()

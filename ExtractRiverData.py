# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 21:39:15 2015

@author: PaulJ
"""

from jsonReadWriteFile import *
#from extractCharsFromString import *
import datetime as dt
import time
#import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
#import io
#import profiler


if __name__ == '__main__':
    #loadFileLocation = "Local"      #choose 1
    loadFileLocation = "Online"
    #loadFileLocation = "None"
    
    databaseFile = "Huron_River_Data.json"
    databaseCSVFile = "Huron_River_Data.csv"
    print("Reading JSON database into Dataframe...")
    startLoadTime = time.clock()
    try:                                            #Load local river database
        riverData = pd.read_csv(databaseCSVFile, sep=",", engine="c", index_col=0)
        riverData.index = pd.to_datetime(riverData.index, unit="s")
    except (OSError, ValueError):
        print("No good json file found, creating empty river data databse")
        riverData = pd.DataFrame(columns=['agency_cd',
                                          'site_no',
                                          'discharge',
                                          'temperature',
                                          'gage_height',
                                          'qualification'])
              #Main list of river data as dictionary (by ID) of dictionaries (by data type)
        startNoRiverData = 0
    else:
        startNoRiverData = len(riverData)
        print("Found json file and loaded into 'riverData' Dataframe with", startNoRiverData, "entries.", flush=True)
        stopLoadTime = time.clock()
        print("Time to Load:", '{:,.1f}'.format(stopLoadTime - startLoadTime), "s\n\n")

    approvedRiverData = riverData[riverData['qualification'] == 'A']
    
    beginDateString = approvedRiverData.index.max().strftime("%Y-%m-%d")
    endDateString = (dt.date.today() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
    
    dataURLBase = "http://nwis.waterdata.usgs.gov/mi/nwis/dv?cb_00060=on&cb_00010=on&format=rdb&site_no=04174500&referred_module=sw&period=&begin_date="
    dataURLBase = dataURLBase + beginDateString + "&end_date=" + endDateString

    print("Getting data from:", beginDateString, "\n" +
          "               to:",   endDateString)

    riverDataFromUSGS = urllib.request.urlopen(dataURLBase).read(2000000).decode()
    print("Finished reading data from USGS site\n")
    
    riverDataFromUSGS = riverDataFromUSGS.split("\n")
    counter = 0
    noNewLinesToEval = len(riverDataFromUSGS)
    print("Adding data from USGS site to 'riverData' Dataframe.")
    for aLine in riverDataFromUSGS:
        counter += 1
        if counter % 1000 == 0:
            print("Completed", counter, "of", noNewLinesToEval, "lines\n")
        if aLine[:4] != "USGS":     #just using USGS data for now
            continue
        dataOnLine = aLine.split("\t")
        tmpAgency = dataOnLine[0]
        tmpSite   = int(dataOnLine[1])
        tmpDateString = dataOnLine[2]
        if dataOnLine[3] != "":
            tmpDischarge = int(float(dataOnLine[3])) 
            tmpDischargeQualification = dataOnLine[4]
        else:
            tmpDischarge = np.NaN
        if len(dataOnLine) >= 6:
            if dataOnLine[5] != "":
                if dataOnLine[9] != "":
                    tmpTemp = float(dataOnLine[9])
                    #tmpTempQualification = dataOnLine[10]
                else:
                    tmpTemp = float(dataOnLine[5])
                    #tmpTempQualification = dataOnLine[6]
            else:
                tmpTemp = np.NaN
        else:
            tmpTemp = np.NAN
        tmpRiverData = pd.DataFrame([[tmpAgency,
                                      tmpSite,
                                      tmpDischarge,
                                      tmpTemp,
                                      np.NaN,
                                      tmpDischargeQualification]],
                                    index = [tmpDateString],
                                    columns=['agency_cd',
                                             'site_no',
                                             'discharge',
                                             'temperature',
                                             'gage_height',
                                             'qualification'])
        riverData = riverData.append(tmpRiverData)

    print("Finished adding USGS data to 'riverData' Dataframe.\n",
          "Eliminating duplicate dates...")
    riverData = riverData.reset_index().drop_duplicates(subset='index', take_last=True).set_index('index')
    print("Finished eliminating duplicates dates. Sorting by dates...")
    
    riverData = riverData.sort_index()
    print("Finished sorting 'riverData' by dates")

    print("Write River Data to file from Dataframe...")
    try:
        riverData.to_csv(databaseCSVFile, sep=",", header=True, index=True,
                         mode="w", line_terminator="\n")
        #riverData.to_json(outputBuffer, orient="index")
        #write_json(databaseFile, riverData)
    except OSError:
        print("Unable to write local databasefile")
        pass
    
    plt.figure()
    riverData['discharge'].dropna().plot(kind='line', figsize=(18,18))
import time
import datetime
import pandas as pd
import sys,os
import socket

class Sensors():
    def __init__(self):
        #start time for log name
        startTime = str(datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S'))
        startDate = str(datetime.datetime.now().strftime('%y-%m-%d_%H-%M'))
    def read(self):
        #define method of data collection
        pass

    def logg(self, info):
        #format data
        info = info.split(",")
        info = {'data1': info[0], 'data2': info[1], 'data3': info[2], 'data4': info[3]}

        #create save file based on initialize time
        savePath = sys.path.append(os.path.realpath('Log_'+self.startTime+".csv"))

        #append or create csv file
        if os.path.isfile(savePath):
            info.to_csv(savePath, mode='a', header=False, index=False)
        else:
            info.to_csv(savePath, header=True, index=False)



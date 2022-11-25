#!/usr/bin/env python3

#    Copyright 2022 github.com/nielm
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


import csv
from datetime import datetime, timedelta
import sys

def main():
    if(len(sys.argv) != 3):
        sys.exit("Usage: %s input.csv fileprefix\n" % sys.argv[0]);

    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            
            startTime = datetime.strptime(row['startTime'],"%Y-%m-%d %H:%M:%S")
            endTime = datetime.strptime(row['endTime'],"%Y-%m-%d %H:%M:%S")
            deltaMins = (endTime-startTime).seconds/60

            heartrecs = list(map(lambda x : int(x), row['heartRaw'].split(",")))
            o2recs = list(map(lambda x : int(x), row['spo2Raw'].split(",")))
            stagerecs = list(map(lambda x : int(x), row['stateRaw'].split(",")))
            if(len(o2recs) < deltaMins or len(heartrecs) < deltaMins) :
                print("warning fewer than expected records: start = %s, end = %s expected %d recs, got %d heart and %d o2" % (startTime, endTime, deltaMins, len(heartrecs), len(o2recs)))
        
            if(len(o2recs) != len(heartrecs)): 
                print("error: mismatched O2/Heart records: start = %s, end = %s expected %d recs, got %d heart and %d o2" % (startTime, endTime, deltaMins, len(heartrecs), len(o2recs)))
            else:
                filename = ("%soxy - %s.dat" % (sys.argv[2], row['startTime']))
                print ("Writing %s, %d mins" % ( filename, len(heartrecs)))

                with open(filename, "wb") as binary_file:

                    binary_file.write(b'\x00') # ID
                    binary_file.write((len(heartrecs)*60).to_bytes(2, byteorder='little', signed=False))

                    oneSecond = timedelta(seconds=1)
                    time=startTime
                    for i in range(0,len(heartrecs)):
                      for j in range (0,60):
                        binary_file.write(b'\x00\x00\x00') # nul, nul, ID
                        binary_file.write((time.year-2000).to_bytes(1,byteorder='little', signed=False))
                        binary_file.write((time.month).to_bytes(1,byteorder='little', signed=False))
                        binary_file.write((time.day).to_bytes(1,byteorder='little', signed=False))
                        binary_file.write((time.hour).to_bytes(1,byteorder='little', signed=False))
                        binary_file.write((time.minute).to_bytes(1,byteorder='little', signed=False))
                        binary_file.write((time.second).to_bytes(1,byteorder='little', signed=False))
                        binary_file.write(o2recs[i].to_bytes(1,byteorder='little', signed=False))
                        binary_file.write(heartrecs[i].to_bytes(1,byteorder='little', signed=False))
                        time += oneSecond

                filename=("%szeo - %s.csv" % (sys.argv[2], row['startTime']))
                print ("Writing %s, %d sleep records" % ( filename, len(stagerecs)))

                with open(filename, "w") as text_file:
                    text_file.write("Start of Night,ZQ,Time to Z,Time in Wake,Time in REM,Time in Light,Time in Deep,Awakenings,Morning Feel,Detailed Sleep Graph\n")
                    text_file.write(startTime.strftime("%m/%d/%Y %H:%M"))
                    text_file.write(",%s,%s,%s,%s,%d,%d,%d,%d," % (row['score'], 0, row['bedActive'], row['rem'], (int(row['n1']) + int(row['n2'])), (int(row['n4']) + int(row['n4'])), 0, 0 ))
                    # write DSG space separtated 30 secs records 1=awake, 2=rem, 3=light, 4=deep
                    # sleepon values 2=awake 3,4=light, 5=rem, 6,7=deep
                    #                   0,1,2,3,4,5,6,7,.......
                    sleepon_to_zeo_map=[0,0,1,3,3,2,4,4,0,0,0,0] 
                    for stage in stagerecs:
                        zeo_stage=sleepon_to_zeo_map[stage]
                        
                        text_file.write("%d %d " % (zeo_stage,zeo_stage))


if __name__ == "__main__":
    main()

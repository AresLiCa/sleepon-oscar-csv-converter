# sleepon-oscar-csv-converter

Converter tool for converting [sleepon](https://www.sleepon.us/) csv export files to SpO2 and sleep stages files that [OSCAR](https://sleepfiles.com/OSCAR/) can import.

## SpO2

SpO2 data is converted into MedView `.dat` files (ChoiceMMed MD300B, MD300KI, MD300I, MD300W1, MD300C318, MD2000A)

These files are binary data with a single day's SpO2 measurement record for every second. SleepOn only exports records every minute, so the exporter pads the files by recording each value 60 times

Binary format is [documented in OSCAR importer source code](https://gitlab.com/pholy/OSCAR-code/-/blob/master/oscar/SleepLib/loader_plugins/md300w1_loader.cpp#L150)

The exporter will create a file for each day in the SleepOn export. 

## Sleep Stage

Sleep Stage/quality data is exported as Zeo `.csv` files, with a file for each day in the SleepOn export. 

Detailed sleep stage info is exported by sleepon per minute, while Zeo .csv files expect every 30 seconds, so the exporter pads the files by exporting each value twice.

CSV file format is interpreted from the [OSCAR importer source](https://gitlab.com/pholy/OSCAR-code/-/blob/master/oscar/SleepLib/loader_plugins/zeo_loader.cpp)


## Usage

Requires Python3: 

```
./convertGo2SleepToOscar.py sleepon_file.csv export_prefix/
```

Generates the following files, with one of each per day of data

```
export_prefix/oxy - DATE-TIME.dat
export_prefix/zeo - DATE-TIME.csv
```

In OSCAR:

* use Data -> Oxymetry Wizard (F7) to "Import from a datafile" and select the 
`oxy - DATE TIME.dat` file you want to import
* use Data -> Import ZEO data and select the `zeo - DATE TIME.dat` file you want to import

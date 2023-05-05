# DISDRODB - A package to standardize, process and analyze global disdrometer data - Data repository

**Main project repository** : [GitHub - ltelab/disdrodb](https://github.com/ltelab/disdrodb)

This repository contains the disdrodb **folder structure**, **configuration** and **links** to download the measurements files.

DISDRODB is part of an initial effort to index, collect and homogenize drop size distribution (DSD) data sets across the globe, as well as to establish a global standard for disdrometers observations data sharing.

DISDRODB standards are being established following FAIR data best practices and Climate & Forecast (CF) conventions, and will facilitate the preprocessing, analysis and visualization of disdrometer data.




## Folders structure

The folder structure is composed of many data source (`DATA_SOURCE_1` eg. "EPFL") that contain one or many campaign (`CAMPAIGN_NAME_1` eg "EPFL_ROOF_2012" ). One campaign has one or many stations (`station_name_1`). Each station folder includes a json file to referance the file url and name.

```
  📁 DISDRODB
  ├── 📁 Raw
      ├── 📁 DATA_SOURCE_1
          ├── 📁 CAMPAIGN_NAME_1
              ├── 📁 issue
                  ├── 📜 station_name_1.yml
                  ├── 📜 station_name_2.yml
              ├── 📁 metadata
                  ├── 📜 station_name_1.yml
                  ├── 📜 station_name_2.yml  
```

For each folder in the /data directory (for each station) there must be an equally named **\*.yml** file in the /metadata folder.

The **metadata YAML** file contains relevant information of the station (e.g. type of device, position, …) which are required for the correct processing and integration into the DISDRODB database.




## How to download or upload data ?

Please refer to official documentation : [DISDRODB - Data](https://disdrodb.readthedocs.io/en/latest/data.html)




# DISDRODB - A package to standardize, process and analyze global disdrometer data - Data repository

**Main project repository** : [GitHub - ltelab/disdrodb](https://github.com/ltelab/disdrodb)

This repository contains the disdrodb **folder structure**, **configuration** and **links** to download the raw disdrometer measurements.

DISDRODB is part of an initial effort to index, collect and homogenize drop size distribution (DSD) data sets across the globe, as well as to establish a global standard for disdrometers observations data sharing.

DISDRODB standards are being established following FAIR data best practices and Climate & Forecast (CF) conventions, and will facilitate the preprocessing, analysis and visualization of disdrometer data.


## Folders structure

The folder structure is composed of many `<DATA_SOURCE>` (i.e. "EPFL") that contain one or many `<CAMPAIGN_NAME>`(`i.e. "HYMEX_LTE_SOP3").
Every campaign has one or many stations.

```
  📁 DISDRODB
  ├── 📁 Raw
      ├── 📁 <DATA_SOURCE>
          ├── 📁 <CAMPAIGN_NAME>
              ├── 📁 issue
                  ├── 📜 station_name_1.yml
                  ├── 📜 station_name_2.yml
              ├── 📁 metadata
                  ├── 📜 station_name_1.yml
                  ├── 📜 station_name_2.yml  
              ├── 📁 data
                  ├── 📁 station_name_1
                  ├── 📁 station_name_2 
```

For each folder in the `/data` directory (for each station) there must be an equally named `<station_name>.yml` file in the `/metadata` directory.

The **metadata YAML** file contains relevant information of the station (e.g. type of device, position, …) which are required for the correct processing and integration into the DISDRODB archive.


## How to download or contribute to the project with your own data ?


Please refer to official documentation : 
* [DISDRODB - Contributing guide](https://disdrodb.readthedocs.io/en/latest/contributors_guidelines.html)
* [DISDRODB - Data](https://disdrodb.readthedocs.io/en/latest/data.html)


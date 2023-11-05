# Welcome to the DISDRODB Metadata Archive

**Main project repository** : [GitHub - ltelab/disdrodb](https://github.com/ltelab/disdrodb)

This repository contains the DISDRODB Metadata Archive: **metadata** and **urls** to download raw disdrometer measurements from the DISDRODB Decentralized Data Archive.

DISDRODB is part of an initial effort to index, collect and homogenize drop size distribution (DSD) data sets across the globe, as well as to establish a global standard for disdrometers observations data sharing.
DISDRODB standards are being established following FAIR data best practices and Climate & Forecast (CF) conventions, and will facilitate the preprocessing, analysis and visualization of disdrometer data.


## Directory structure

The directory structure is composed of many `<DATA_SOURCE>` (i.e. `EPFL`) that contain one or many `<CAMPAIGN_NAME>`(i.e. `HYMEX_LTE_SOP3`).
Every campaign has one or many stations.

```
  📁 DISDRODB
  ├── 📁 Raw
      ├── 📁 <DATA_SOURCE>
          ├── 📁 <CAMPAIGN_NAME>
              ├── 📁 issue
                  ├── 📜 <station_name_1>.yml
                  ├── 📜 <station_name_2>.yml
              ├── 📁 metadata
                  ├── 📜 <station_name_1>.yml
                  ├── 📜 <station_name_2>.yml  
```

Each **metadata YAML** file contains relevant information of the station (e.g. type of device, position, disdrodb reader, disdrodb data url, …) which is required for the correct integration and processing into DISDRODB.

Each **issue YAML** file reports timesteps or time periods with instrument malfunctioning and measurements errors that must be discarded when processing the data.

## Frequently Asked Questions (FAQs)

* [How to Update DISDRODB Metadata?](https://disdrodb.readthedocs.io/en/latest/metadata_archive.html)
* [How to Contribute New Data to DISDRODB?](https://disdrodb.readthedocs.io/en/latest/contribute_data.html)
* [How to Download DISDRODB data?](https://disdrodb.readthedocs.io/en/latest/data_download.html)
* [What are the DISDRODB Contributing Guidelines](https://disdrodb.readthedocs.io/en/latest/contributors_guidelines.html)



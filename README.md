# Welcome to the DISDRODB Metadata Archive

**Software repository** : [disdrodb](https://github.com/ltelab/disdrodb)
**Documentation** : [disdrodb.readthedocs.io](https://disdrodb.readthedocs.io/en/latest/)

DISDRODB is an international initiative to index, collect, and harmonize drop size distribution (DSD) data from around the world.
The DISDRODB project aims to also establish a global standard for sharing disdrometer observations.
Built on FAIR data principles and Climate & Forecast (CF) conventions,
DISDRODB standards facilitates the processing, analysis, and visualization of disdrometer data.

This repository hosts the DISDRODB Metadata Archive, which serves as a central registry for:

- Station Inventory: a catalog of all available disdrometer sites

- Sensor Status: a register for any stations malfunctions

- Data Archives: URLs linking to the raw disdrometer data repositories

By using GitHub, we enable the community to collaboratively improve station metadata,
track sensor performance, and iteratively enhance data quality - while keeping every step transparent and fully reproducible.

To ensure quality and metadata consistency, we follow a comprehensive [standard set of metadata keys](https://disdrodb.readthedocs.io/en/latest/metadata.html).

Contributors can report sensor issues or periods with erroneous data via dedicated YAML files, making it easy to pinpoint and document any anomalies.

## DISDRODB Metadata Archive Structure

The DISDRODB Metadata Archive is composed of many `<DATA_SOURCE>` (i.e. `EPFL`) that contain one or many `<CAMPAIGN_NAME>`(i.e. `HYMEX_LTE_SOP3`).
Every campaign has one or many stations.

```
  📁 DISDRODB
  ├── 📁 METADATA
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

- [How to Download DISDRODB data ?](https://disdrodb.readthedocs.io/en/latest/quick_start.html)
- [How to Update the DISDRODB Metadata Archive ?](https://disdrodb.readthedocs.io/en/latest/metadata_archive.html)
- [How to Contribute New Data to DISDRODB ?](https://disdrodb.readthedocs.io/en/latest/contribute_data.html)
- [What are the DISDRODB Contributing Guidelines ?](https://disdrodb.readthedocs.io/en/latest/contributors_guidelines.html)

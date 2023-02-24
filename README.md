# DISDRODB - A package to standardize, process and analyze global disdrometer data - Data repository

**Main project repository** : [GitHub - ltelab/disdrodb](https://github.com/ltelab/disdrodb)

:card_file_box: This repository contains the disdrodb **folder structure**, **configuration** and **links** to download the measurements files.

DISDRODB is part of an initial effort to index, collect and homogenize drop size distribution (DSD) data sets across the globe, as well as to establish a global standard for disdrometers observations data sharing.

DISDRODB standards are being established following FAIR data best practices and Climate & Forecast (CF) conventions, and will facilitate the preprocessing, analysis and visualization of disdrometer data.

## Installation

Just clone the repository

```
git clone https://github.com/ltelab/disdrodb-data.git
```

## Folders structure

The folder structure is composed of many data source (`DATA_SOURCE_1` eg. "EPFL") that contain one or many campaign (`CAMPAIGN_NAME_1` eg "EPFL_ROOF_2012" ). One campaign has one or many stations (`station_name_1`). Each station folder includes a json file to referance the file url and name.

```
  📁 DISDRODB
  ├── 📁 Raw
      ├── 📁 DATA_SOURCE_1
          ├── 📁 CAMPAIGN_NAME_1
              ├── 📁 data_url
                  ├── 📁 station_name_1
                      ├── 📜 url.json
                  ├── 📁 station_name_2
                      ├── 📜 url.json
              ├── 📁 issue
                  ├── 📜 station_name_1.yml
                  ├── 📜 station_name_2.yml
              ├── 📁 metadata
                  ├── 📜 station_name_1.yml
                  ├── 📜 station_name_2.yml
  ├── 📁 app
      ├── 📜 download_data.py
  
```

For each folder in the /data directory (for each station) there must be an equally named **\*.yml** file in the /metadata folder.

The **metadata YAML** file contains relevant information of the station (e.g. type of device, position, …) which are required for the correct processing and integration into the DISDRODB database.

## (A) How to download the data locally ?

To get the measurements locally, just run the following python command :

```
cd <app folder path>
python download_data.py
```

This code parses all json files and download the corresponding data.

If you want to download only one specific folder (data_source, campaign_name, station_name) :

```
cd <app folder path>
python download_data.py -data_source <your-data-source> -campaign_name <your-campaign-name> -station_name <you-station-name>
```

By default, if a file is already in the local folder, it will not be overwritten. If you want to change this behavior and overwrite existing files, add the `-overwrite` parameter as follow :

```
cd <app folder path>
python download_data.py -overwrite True
```

## (B) How to add your own data to DISDRODB ?

Do you want to contribute to the project with your own data ? Great ! Just follow these steps :

1. Create a new branch
   
   ```
   git checkout -b "reader-<data_source>-<campaign_name>"
   ```

2. Add the your data source, campaign names, station name to the current folder structure.

3. Load your data to an external repository (eg. Zenodo). Github limits the file size to 50 MB, therefore no data can be loaded into the github repository.

4. For each campaign, create a `url.json` file and add the following information :
   
   ```
         {"<the-file-name>":"<the_url>"},
   ```

5. Add your **metadata YAML** file for each station `station_name.yml`, in a `metadata` directory in the campaign directory. We recommend you to copy-paste an existing metadata YAML file to get the correct structure.

6. (Optional) Add your **issues YAML** files, for each station `station_name.yml`, in an `issue` directory located in the campaign directory. We recommend you to copy-paste an existing metadata YAML file to get the correct structure.

7. Test that the integration of your new dataset functions, by deleting your data locally - and re-fetching it through the process detailed in (A).

8. Commit your changes and push your branch to GitHub

9. [Create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request), and wait for a maintainer to accepts it !

If you struggle with this process, don't hesitate to raise an [issue](https://github.com/ltelab/disdrodb-data/issues/new/choose) so we can help!

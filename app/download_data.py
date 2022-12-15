import os
import json
import pathlib
import re
import urllib3
import argparse


def get_list_urls_files(
    data_source: str = None, campaign_name: str = None, station_name: str = None
) -> list:
    """Return a list containing all url.json files paths

    Returns
    -------
    list
        List of all url.json files paths
    """

    folder_path = os.path.join(
        os.path.dirname(pathlib.Path(__file__).parent.resolve()), "DISDRODB", "Raw"
    )

    if data_source:
        folder_path = os.path.join(folder_path, data_source)
        if campaign_name:
            folder_path = os.path.join(folder_path, campaign_name)
            if station_name:
                folder_path = os.path.join(folder_path, "data", station_name)

    list_of_urls_files_paths = [
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(folder_path)
        for f in filenames
        if f == "url.json"
    ]

    return list_of_urls_files_paths


def check_url(url: str) -> bool:
    """Check url

    Parameters
    ----------
    url : str
        url

    Returns
    -------
    bool
        True if url well formated, False if not well formated
    """
    regex = r"^(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$"

    if re.match(regex, url):
        return True
    else:
        return False


def download_file(url: str, file_name: str) -> None:
    """Download file

    Parameters
    ----------
    url : str
        URL of the file to download
    file_name : str
        Local name of the file
    """

    chunk_size = 4096

    http = urllib3.PoolManager()
    r = http.request("GET", url, preload_content=False)

    with open(file_name, "wb") as out:
        while True:
            data = r.read(chunk_size)
            if not data:
                break
            out.write(data)

    r.release_conn()


def download_file_content(file_path: str, overwrite: bool = False) -> None:
    """Download the files based on the URLs included in the JSON files.

    Parameters
    ----------
    file_path : str
        Json file path
    overwrite : bool, optional
        Overwrite the raw data file is already existing, by default False
    """

    folder_path = os.path.dirname(file_path)

    with open(file_path, "r") as jsonFile:
        list_content = json.load(jsonFile)

    for file in list_content:
        file_name = file.get("file_name")
        url = file.get("url")
        if check_url(url):
            dest_path = os.path.join(folder_path, file_name)
            if os.path.exists(dest_path) and not overwrite:
                print(f"File {dest_path} already exists")
            else:
                download_file(url, dest_path)
                print(f"Download {url} into {dest_path}")


def download_all_files(
    data_source: str = None,
    campaign_name: str = None,
    station_name: str = None,
    overwrite: bool = False,
):
    """Batch function to execute download over all files in  folder.

    Parameters
    ----------
    data_source : str, optional
        Data source folder name (eg : EPFL) If not provided, all data sources will be downloaded, by default None
    campaign_name : str, optional
        Campaign name (eg :  EPFL_ROOF_2012). If not provided, all campaigns will be downloaded, by default None
    station_name : str, optional
        Station name. If not provided, all stations will be downloaded, by default None
    overwrite : bool, optional
        Overwrite the raw data file is already existing, by default False
    """

    for file in get_list_urls_files(data_source, campaign_name, station_name):
        download_file_content(file, overwrite)


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data_source", type=str, help="Define the data source")
    parser.add_argument(
        "-campaign_name", type=str, help="Define the name of the campaign"
    )
    parser.add_argument(
        "-station_name", type=str, help="Define the name of the station"
    )
    parser.add_argument(
        "-overwrite", type=bool, default=False, help="Overwite existing file ?"
    )

    return parser


def config_parser():
    opt = parser().parse_args()
    return opt


def main():
    download_all_files(
        data_source=args.data_source,
        campaign_name=args.campaign_name,
        station_name=args.station_name,
        overwrite=args.overwrite,
    )


if __name__ == "__main__":
    args = config_parser()
    main()

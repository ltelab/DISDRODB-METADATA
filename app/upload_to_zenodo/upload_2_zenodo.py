import os
import uuid
import datetime
import json
import yaml
import pynodo
import argparse
import time


# Parameters 
URLS_JSON_FILE_NAME = "url.json"
RAW_FOLDER_NAME = "Raw"
DATA_FOLDER_NAME = 'data'
CONFIG_FILE_NAME = 'secret.yml'




# read yaml file
def read_yaml_file(path_yaml_file: str) -> dict:
    """Read yaml file and return content as dict

    Parameters
    ----------
    path_yaml_file : str
        Path of the yaml file

    Returns
    -------
    dict
        Content of the yaml file
    """
    with open(path_yaml_file, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def get_zenodo_access_tocken() -> str :
    """Get the zenodo access tocken

    Returns
    -------
    str
        Tocken 

    Raises
    ------
    IOError
        If the config file does not exist
    AttributeError
        If the access tocken is not in the config file
    """
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),CONFIG_FILE_NAME)

    if not os.path.exists(config_path) :
        raise IOError("Config file does not exist ")
    
    conf = read_yaml_file(config_path)
    
    if not conf.get('zenodo_access_tocken') :
        raise AttributeError("zenodo_access_tocken is not set in the config file")

    return conf.get('zenodo_access_tocken')




# Function that return a list of raw file paths under a data folder
def get_dict_data_folder_path(initial_path : str) -> dict : 
    """Function that return a dict of raw file paths under a data folder

    Parameters
    ----------
    initial_path : str
        Initial path

    Returns
    -------
    list
        list of path 
    """
    result = [
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(initial_path)
        for f in filenames        
    ]


    dict_of_data_folder = dict()

    for item in result :
        list_of_path_element = os.path.normpath(item).split(os.sep)

        if RAW_FOLDER_NAME in list_of_path_element:
            index_raw_folder = os.path.normpath(item).split(os.sep).index(RAW_FOLDER_NAME)
            if len(list_of_path_element) > index_raw_folder + 3 and DATA_FOLDER_NAME == list_of_path_element[index_raw_folder+3] :
                
                # instutution name 
                institution_name = list_of_path_element[index_raw_folder+1]
                if not dict_of_data_folder.get(institution_name) :
                    dict_of_data_folder[institution_name] = dict()
                
                # campaign name 
                campaign_name = list_of_path_element[index_raw_folder+2]
                if not dict_of_data_folder.get(institution_name).get(campaign_name) :
                    dict_of_data_folder[institution_name][campaign_name] = list()
                
                dict_of_data_folder[institution_name][campaign_name].append(item)

    return dict_of_data_folder


def save_dict_to_json(path_json: str, content: dict):
    """Save text into new line a a text file. Creates the text file if needed

    Parameters
    ----------
    path_text_file : str
        path of the text file
    line : str
        text to add as new line
    """
    
    # load the current JSON content
    if os.path.exists(path_json):
        with open(path_json, "r") as jsonFile:
            dict_content = json.load(jsonFile)
    else:
        dict_content = {}

    # Add new content
    for k,v in content.items():
        dict_content[k] = v

    # Save the JSON
    with open(path_json, "w") as jsonFile:
        json.dump(dict_content, jsonFile, indent=4)



def upload_2_zenodo(file_path : str, depo_id : str,file_name_zenodo : str ) -> str :
    """Upload one file to zenodo

    Parameters
    ----------
    file_path : str
        File pyth
    depo_id : str
        Depo ID
    file_name_zenodo : str
        File name on zenodo

    Returns
    -------
    str
        File URL
    """
    # Connect to zenodo
    access_token = get_zenodo_access_tocken()
    zen_files = pynodo.DepositionFiles(deposition=depo_id, access_token=access_token, sandbox=False)

    filename = os.path.basename(file_path)
    # filename_zenodo = str(uuid.uuid4().hex)
    filename_zenodo = file_name_zenodo
    t_init = datetime.datetime.now()
    zen_files.upload(file_path, filename_zenodo)
    duration = datetime.datetime.now() - t_init
    message = f"{file_path} has been uploaded in {duration} sec"
    print(message)
    file_url = f"https://zenodo.org/record/{depo_id}/files/{filename_zenodo}"
    time.sleep(1) # Wait 1 sec to avoid zenodo api limitation rate
    return file_url


# Function that remove all file paths except the url.json file from the list
def remove_all_file_path_except_url_json(list_file_path : dict) -> dict :
    """Function that remove all file paths except the url.json file from the list

    Parameters
    ----------
    list_file_path : dict
        List of file path

    Returns
    -------
    dict
        List of file path
    """

    dict_json_file_path = {}


    for institution_name, content in  list_file_path.items() :
        for campaign_name, list_file_path in content.items() :
            for file_path in list_file_path :
                if file_path.endswith(URLS_JSON_FILE_NAME) :
                    if not dict_json_file_path.get(institution_name) :
                        dict_json_file_path[institution_name] = dict()
                    
                    if not dict_json_file_path.get(institution_name).get(campaign_name) :
                        dict_json_file_path[institution_name][campaign_name] = list()
                    
                    dict_json_file_path[institution_name][campaign_name].append(file_path)
            

    return dict_json_file_path 




def batch_upload_2_zenodo(dict_file_path : dict, depo_id : str, incremental_loading : bool = True) :


    dict_json_file_path = remove_all_file_path_except_url_json(dict_file_path)



    for institution_name, content in  dict_file_path.items() :
        for campaign_name, list_file_path in content.items() :
            list_of_elements_in_path = os.path.normpath(list_file_path[0]).split(os.sep)
            index_data_folder = list_of_elements_in_path.index(campaign_name)+2
            path_json = os.path.join('/',*list_of_elements_in_path[:index_data_folder],URLS_JSON_FILE_NAME)

            list_of_uploaded_files = list()

            if incremental_loading :
                list_of_json_file_paths = dict_json_file_path.get(institution_name).get(campaign_name)
                for item in list_of_json_file_paths :
                    if os.path.exists(item):
                        with open(item, "r") as jsonFile:
                            data = json.load(jsonFile)
                            for file in data.keys() :
                                list_of_uploaded_files.append(os.path.join(os.path.dirname(item),file))

    

            for file_path in list_file_path :
                
                if file_path in list_of_uploaded_files :
                    print(f"{file_path} already uploaded")
                else :
                    list_of_elements_in_path = os.path.normpath(file_path).split(os.sep)
                    file_name = os.path.join(*list_of_elements_in_path[index_data_folder:])
                    file_name_zenodo ='_'.join([institution_name,campaign_name,*list_of_elements_in_path[index_data_folder:]])
                    file_url = upload_2_zenodo(file_path,depo_id,file_name_zenodo)
                    save_dict_to_json(path_json,{file_name:file_url})

            


                
def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-path_ini", type=str, help="Define the initial path")
    parser.add_argument(
        "-session_id", type=str, help="Zenodo session ID"
    )
    parser.add_argument(
        "-incremental_loading", choices=('True','False'), help="Avoid loading already loaded files ?"
    )

    return parser


def config_parser():
    opt = parser().parse_args()
    return opt


def main():

    dict_path_to_upload =  get_dict_data_folder_path(args.path_ini)
    incremental_loading = True if args.incremental_loading == 'True' else False
    batch_upload_2_zenodo(dict_path_to_upload, args.session_id, incremental_loading)




if __name__ == "__main__":
    args = config_parser()
    main()


# local_path = "/ltenas8/data/disdrodb-data/disdrodb/Raw/EPFL/EPFL_2009"


# batch_upload_2_zenodo( get_dict_data_folder_path(local_path),7567694, True)



# # file = get_list_data_folder_path(local_path).get('EPFL').get('EPFL_2009')[0]


# # file_url = upload_2_zenodo(file,7567694)

# # print(file_url)

# # print(get_list_data_folder_path(local_path).get('EPFL').get('EPFL_2009')[:6])


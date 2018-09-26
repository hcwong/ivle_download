import os
import requests
import pprint
import gzip
import shutil
from dotenv import load_dotenv
load_dotenv()

IVLE_KEY = os.getenv("IVLE_KEY")
IVLE_TOKEN = os.getenv("IVLE_TOKEN")
DOWNLOAD_PATH= os.getenv("DOWNLOAD_PATH")

class IvleRequest:
  def __init__(self):
    self.ivle_key = IVLE_KEY
    self.ivle_token = IVLE_TOKEN
    self.url = "https://ivle.nus.edu.sg/api/Lapi.svc/"
  
  def validate(self):
    params = {"APIKey": self.ivle_key, "Token": self.ivle_token}
    r = requests.get(self.url + "Validate", params=params)
    data = r.json()
    print(f"Valid?: {data['Success']}")
    if not (data["Success"]):
      print(f"New IVLE Token generated: {data['Token']}")
      IVLE_TOKEN = data["Token"]
  
  def get_files(self, modules, duration):
    module_mappings = self.get_modules(modules)
    files_to_download = self.get_all_files_request(module_mappings, duration)
    self.download_all_files(files_to_download)
    print(f"Succesfully downloaded {len(files_to_download)} files")

  def get_all_files_request(self, module_mappings, duration):
    file_elements = []
    # TOFIX: A bit too nested. Clean up
    for key, value in module_mappings.items():
      results_list = self.get_file_request(value, duration)["Results"]
      if results_list:
        # TOFIX: Also returns files which were uploaded before that time period
        for element in results_list[0]["Folders"]:
          if element["Files"]:
            file_elements += (element["Files"])
    return file_elements

  def get_file_request(self, module_code, duration):
    params = {"APIKey": self.ivle_key, "AuthToken": self.ivle_token, "CourseID": module_code, 
              "Duration": duration, "WorkbinID": "", "TitleOnly": False}
    r = requests.get(self.url + "Workbins", params=params)
    return r.json()

  def download_all_files(self, files_list):
    for el in files_list:
      self.download_file(el["ID"], el["FileName"])

  def download_file(self, file_id, file_name):
    params = {"APIKey": self.ivle_key, "AuthToken": self.ivle_token, "ID": file_id, "target": "workbin"}
    url = "https://ivle.nus.edu.sg/api/downloadfile.ashx"
    r = requests.get(url, params=params)
    data = r.content
    with open(f"./{file_name}", "wb+") as f_out:
      f_out.write(data)

  def get_modules(self, selections):
    params = {"APIKey": self.ivle_key, "AuthToken": self.ivle_token}
    r = requests.get(self.url + "Modules", params=params)
    data = r.json()
    module_mapping = {}
    # Iterates through the results to get the module id of the relevant courses
    for element in selections:
      for module in data["Results"]:
        if element == module["CourseCode"]:
          module_mapping[module["CourseCode"]] = module["ID"]
          break
    print(module_mapping)
    return module_mapping


def main():
  ivle_request = IvleRequest()
  ivle_request.get_files(["CS1101S", "MA1521"], 7000)
  # ivle_request.download_file("1b8eec1c-b2de-4151-a2e5-ae2fc37f870d")


if __name__ == "__main__":
    main()
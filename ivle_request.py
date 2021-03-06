import os
import requests
import pprint
import argparse
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
      results_list = self.get_file_request(value.upper(), duration)["Results"]
      if results_list:
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
    with open(f"./{DOWNLOAD_PATH}/{file_name}", "wb+") as f_out:
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
  parser = argparse.ArgumentParser(description="Run the IVLE downloader")
  parser.add_argument("-d", "--duration")
  parser.add_argument("-m", "--modules")
  parser.add_argument("-v", "--validate")
  args = vars(parser.parse_args())
  ivle_request = IvleRequest()
  day_to_min = lambda x: int(x) * 1440
  ivle_request.get_files(args["modules"].split(" "), day_to_min(args["duration"]))

if __name__ == "__main__":
    main()
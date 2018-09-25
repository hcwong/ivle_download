import os
import requests
import pprint
from dotenv import load_dotenv
load_dotenv()

IVLE_KEY = os.getenv("IVLE_KEY")
IVLE_TOKEN = os.getenv("IVLE_TOKEN")

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
    self.get_all_files_request(module_mappings, duration)

  def get_all_files_request(self, module_mappings, duration):
    for key, value in module_mappings.items():
      results_list = self.get_file_request(value, duration)["Results"]
      files_to_dl = self.get_file_ids(results_list)
      for id in files_to_dl:
        self.download_file(id)

  def get_file_request(self, module_code, duration):
    params = {"APIKey": self.ivle_key, "AuthToken": self.ivle_token, "CourseID": module_code, 
              "Duration": duration, "WorkbinID": "", "TitleOnly": False}
    r = requests.get(self.url + "Workbins", params=params)
    # pprint.pprint(r.json())
    return r.json()

  def get_file_ids(self, files):
    # TOFIX: Assumed that there is no nesting of folders. Need to check
    results_list = []
    for f in files:
      results_list.append(f["ID"])
    return results_list

  def download_file(self, file_id):
    params = {"APIKey": self.ivle_key, "AuthToken": self.ivle_token, "ID": file_id}
    url = "https://ivle.nus.edu.sg/api/downloadfile.ashx"
    r = requests.get(url, params=params)
    # TOFIX: Response 200 need to figure a way to get the file downloaded
    print(r.text)

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
  ivle_request.get_files(["CS1101S", "MA1521"], 5000)


if __name__ == "__main__":
    main()
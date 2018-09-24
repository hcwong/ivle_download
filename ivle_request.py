import os
import requests
import xml.etree.ElementTree as et
from dotenv import load_dotenv
load_dotenv()

IVLE_KEY = os.getenv("IVLE_KEY")
IVLE_TOKEN = os.getenv("IVLE_TOKEN")

class IvleRequest:
  def __init__(self):
    self.ivle_key = IVLE_KEY
    self.ivle_token = IVLE_TOKEN
    self.url = "https://ivle.nus.edu.sg/api/Lapi.svc/"

  def get_files_request(self, module_code, duration):
    params = {"APIKey": self.ivle_key, "AuthToken": self.ivle_token, "CourseID": module_code, 
              "Duration": duration, "WorkbinID": "", "TitleOnly": False}
    r = requests.get(self.url + "Workbins", params=params)
    print(r.url)
    print(r.content)
    root = et.fromstring(r.content)

  def validate(self):
    params = {"APIKey": self.ivle_key, "Token": self.ivle_token}
    r = requests.get(self.url + "Validate", params=params)
    data = r.json()
    print(f"Valid?: {data['Success']}")

def main():
  ivle_request = IvleRequest()
  ivle_request.get_files_request("MA1521", 0)
  # ivle_request.validate()

if __name__ == "__main__":
    main()
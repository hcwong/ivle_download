import os
import requests

from dotenv import load_dotenv
load_dotenv()

IVLE_KEY = os.getenv("IVLE_KEY")

def main():
  authentication()

def authentication():
  auth_url = "https://ivle.nus.edu.sg/api/login/"
  auth_params = {"apikey": IVLE_KEY, "url": "http://localhost:5000"}
  r = requests.get(auth_url, params=auth_params)
  print(r.text)

if __name__ == "__main__":
    main()
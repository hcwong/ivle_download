Python Script to download IVLE Files with one command

# Installation
1. Install the venv dependencies (TODO: create the list of dependencies)
2. Run the install.sh script (chmod if necessary)
3. Then activate venv environment
4. Go [here](https://ivle.nus.edu.sg/LAPI/default.aspx) to get your LAPI key and put it in the env file
5. Run `FLASK_APP=server.py flask run` Go to http://localhost:5000, login to get your token
6. Put the token in the env file
7. Run `ivle` with the proper arguments to get your files downloaded. Running `ivle` without any args
will show the usage requirements

## TODO
1. Error checking and handling
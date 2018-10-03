#!/bin/bash

cd 
# Change this path to point to your source directory
echo "alias ivle= cd ./Desktop/Projects/ivle && ./ivle_request.sh" >> .bash_profile

# Reload bash profile
source .bash_profile

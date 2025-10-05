#!/bin/bash

sudo apt update
sudo apt install google-chrome-stable

version=$(google-chrome --version)

# install dependencies
sudo apt install -y unzip xvfb libxi6 libgconf-2-4

wget https://chromedriver.storage.googleapis.com/${version}/chromedriver_linux64.zip

unzip chromedriver_linux64.zip

sudo mv chromedriver /usr/local/bin/

sudo chmod +x /usr/local/bin/chromedriver


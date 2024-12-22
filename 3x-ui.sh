#!/bin/bash

echo "Installing Python3 and SQLite..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip sqlite3

echo "Downloading the Python script..."
curl -L https://raw.githubusercontent.com/ipcloudflaretamiz/x-ui.db/main/3x-ui.py -o 3x-ui.py

echo "Running the Python script..."
python3 3x-ui.py

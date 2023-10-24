#! /bin/bash

main_path=$(realpath "../Main/tracker.py")
api_key_file="../Configs/api_key.py"
launch_file="btc_tracker.sh"
launch_path="$HOME/Desktop/$launch_file"
error_log="/tmp/tracker_errors.log"

echo -e "This 'installer' will write your coinmarketcap api key"
echo -e "to file and create an executable script on your"
echo -e "Raspberry Pi Desktop that can be double clicked to launch"
echo

echo -e "Using this application will require acquiring an API Key from"
echo -e "https://pro.coinmarketcap.com/signup/"
echo

# Install pip packages
pip install -r ../requirements.txt

# Write API Key file if doesn't exist
if [ -f $api_key_file ]; then
    echo -e "API Key file found"
else
    echo -e "API Key file NOT found, please enter API key:"
    read userInput
    echo -e "Creating API Key file: $api_key_file"
    echo -e "api_key = \"$userInput\"" > $api_key_file
fi

echo
echo -e "coinmarketcap stats will be pulled from an external cache in"
echo -e "a future release, so this step will not be required"
echo

# Write Launch Script
echo -e "Writing launch file: $launch_path"
echo -e "#!/bin/sh" > "$launch_path"
echo -e "python $main_path 2> $error_log" >> "$launch_path"
sudo chmod 755 $launch_path

echo -e "Installation complete."
echo -e "Please run $launch_file from Desktop"

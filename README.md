# Setup + Installation
    1. Download repository and move to desired directory
    2. Run `pip install -r requirements.txt` to install any potentially missing packages
    3. Create a Webex Teams bot (https://developer.webex.com/my-apps/new/bot), and collect the Bot's access token provided upon creation 
    4. Obtain the room ID, from https://developer.webex.com/docs/api/v1/rooms/list-rooms - click the run button and then extract an ID from an entry in the response
    5. Go to the Meraki Dashboard and generate an API key for yourself
    6. Paste these values into the provided credentials.json file (if desired)
    7. Run script. The script will message your designated room with check your network for new devices every 5 minutes and message the desginated chat channel if it detects a new device. For instructions on running the script, read below


# Instructions
The script obtains its credentials in two ways: 
- Imported from a JSON file using the --credentials argument
- Individually assigned using the --apiKey, --botToken and --botRoom arguments

To run the script, enter `python[3] main.py [arguments]` and the script will begin, requiring no further input

# Description
The script will run and gather a list of all devices you have access to, and then check every 5 minutes for new devices. If new devices are found, a message will be sent to the webex teams room specified with an alert that a new device has been detected

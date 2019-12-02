# Requirements
- Requests (install at https://pypi.org/project/requests/)
- Meraki Dashboard API Key (Instructions on obtaining: https://documentation.meraki.com/zGeneral_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API)
- Webex Teams Bot and Room ID (bot creatable at https://developer.webex.com/, API documentation for obtaining a Webex Teams Room ID at https://developer.webex.com/docs/api/v1/rooms/list-rooms)

# Instructions
The script obtains its credentials in two ways: 
- Imported from a JSON file using the --credentials argument
- Individually assigned using the --apiKey, --botToken and --botRoom arguments

To run the script, enter `python[3] main.py [arguments]` and the script will begin, requiring no further input

# Description
The script will run and gather a list of all devices you have access to, and then check every 5 minutes for new devices. If new devices are found, a message will be sent to the webex teams room specified with an alert that a new device has been detected

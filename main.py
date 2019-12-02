from classes import Webex, Meraki
import time, argparse, json

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--apiKey', required=False, help='Your Meraki Dashboard API Key.')
    parser.add_argument('--botToken', required=False, help='Bot Token generated from https://developer.webex.com/.')
    parser.add_argument('--botRoom', required=False, help='The Room ID, gathered using the Webex Teams API. For more information, go to https://developer.webex.com/docs/api/v1/rooms/list-rooms.')
    parser.add_argument('--credentialsFile', required=False, help='JSON file with the API Key, Bot Token or Room you wish the bot to post in as the keys. Keys must be the same as the arguments.')

    args = parser.parse_args()

    apiKey = None
    botToken = None
    botRoom = None


    # If they've set the credentials argument, import the settings from the file
    if args.credentialsFile:
        with open(args.credentialsFile) as json_file:
            parsed = json.load(json_file)
            if "apiKey" in parsed:
                apiKey = parsed["apiKey"]
            if "botToken" in parsed:
                botToken = parsed["botToken"]
            if "botRoom" in parsed:
                botRoom = parsed["botRoom"]

    # And if they've used the individual arguments, override settings file with those
    if args.apiKey:
        apiKey = args.apiKey
    if args.botToken:
        botToken = args.botToken
    if args.botRoom:
        botRoom = args.botRoom

    # If any of the required settings arent set, throw error
    if apiKey == None or botToken == None or botRoom == None:
        if apiKey == None:
            print('Please include a Cisco Meraki Dashboard API Key!')
            exit()
        if botToken == None:
            print('Please include a Webex Teams bot token!')
            exit()
        if botRoom == None:
            print('Please include a Webex Teams room key for the bot to post in!')
            exit()

    meraki = Meraki(apiKey)
    webex = Webex(botToken=botToken, botRoom=botRoom)

    storage = {}

    notifyNew = False
    running = True

    # Iterates through all the organisations, then networks, then devices the user has access to and stores them in the storage variable as a dict,
    # with the MAC address of the device as the key to ensure uniqueness
    # If after the first iteration, a new device is detected, a message will be sent to the Webex Teams bot in the room supplied alerting of the new device
    # then, the script will wait for 5 minutes before checking again 

    while running:
        newDevice = {}
        orgs = meraki.getOrganisations()["data"]
        if len(orgs):
            for organisation in orgs:
                networks = meraki.getNetworks(organisation)["data"]
                if len(networks):
                    for network in networks:
                        time.sleep(1)
                        message = ''
                        for device in meraki.getDevices(network)["data"]:
                            if device["mac"] not in storage:
                                if notifyNew:
                                    if device["pxType"] not in newDevice:
                                        newDevice[device["pxType"]] = []
                                    newDevice[device["pxType"]].append(device)
                                    storage[device["mac"]] = device
                                else:
                                    storage[device["mac"]] = device
                            else:
                                pass
            notifyNew = True
            for key in newDevice:
                if key == 'firewall':
                    message += '**New Firewall(s) added:** \n'
                elif key == 'access-point':
                    message += '**New Access Point(s) added:** \n'
                elif key == 'switch':
                    message += '**New Switch(es) added:** \n'
                elif key == 'security-camera':
                    message += '**New Security Camera(s) added:** \n'
                elif key == 'wireless-wan':
                    message += '**New WAN Device(s) added:** \n'
                elif key == 'voip-phone':
                    message += '**New VOIP Phone(s) added:** \n'
                else:
                    message += '**New Unidentified Device(s) added:** \n'

                for device in newDevice[key]:
                    message += '- **Serial:** ' + str(device["serial"]) + ' **Address:** ' + str(device["lanIp"]) + '\n'
                message += '\n'
            if message:
                message += '\n'
                webex.sendMessage(message)
            time.sleep(300)
        else:
            print('No organisations found')
            running = False

if __name__ == '__main__':
    main()
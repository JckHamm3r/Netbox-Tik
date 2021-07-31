#Disclaimer
This tool was made specifically for the use of my company and I will not take responsibility for anything that this tool may break or improperly configure for personal or professional reasons. Use this tool at your own risk.

See License

# Netbox-Tik
This tool will create a .rsc file for all of your MikroTik devices that are in Netbox as well as a log file that shows the result for each attempt of pulling the backups.

# Prerequisites
Python 3.7 or greater

Python Modules: paramiko, os, requests, json, datetime, socket, pandas

The machine that you run this on needs to be able to reach your network and your netbox instance.

The devices in Netbox need to have an "Active" status, a "Role", a "Name", a "Manufacturer" of "mikrotik", and a "Primairy IP Address" set for each device.
If you know what you are doing, you can tweak the "Manufacturer" on line# 36 so that you dont have to change all of your device information.

# Setup
Line 10 --> Enter the directory that you want the files to be created in.

Line 13 --> Enter your netbox API token, make sure to include "Token" at the beginning of it.

Line 14 --> Enter your netbox URL, the only thing that should change here is "YOURNETBOXURL.COM".

Line 17 --> Enter the username for your MikroTik devices.

Line 18 --> Enter the password for your MikroTik devices.

Line 67 --> Change "30" to the number of days worth of backups that you want to keep.

# Customization
I can customize this for you to use within your organization or I can create another custom tool for you.

If interested, reach out, you can find me on the WISP Talk Facebook group. - Chris Josey



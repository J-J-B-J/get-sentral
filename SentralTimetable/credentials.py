"""Functions to get the credentials"""
from json import load
import json
import os

json_filename = "Sentral_Details.json"


def get_data_from_json(json_file):
    """Get the data from the JSON environment file"""
    try:
        with open(json_file, 'r') as f:
            return load(f)
    except:
        return {}


# TODO: Make timeout settable by credential methods
def get(debug, usr, pwd, url, timeout):
    """Get the credentials for the program"""
    # Use "is None" instead of "not" for debug because debug could be False
    if debug is None:
        debug = {"True": True, "False": False}.get(os.getenv("DEBUG"))
        if debug is None:
            debug = get_data_from_json(json_filename).get("DEBUG")
            if debug is None:
                while True:
                    debug = {"Y": True, "N": False}.get(
                        input("Debug? Y/N: ")[0].upper())
                    if debug is not None:
                        break
    if not usr:
        usr = os.getenv("USER_NAME")
        if not usr:
            usr = get_data_from_json(json_filename).get("USERNAME")
            if not usr:
                usr = input("Username: ").lower()
    if not pwd:
        pwd = os.getenv("PASSWORD")
        if not pwd:
            pwd = get_data_from_json(json_filename).get("PASSWORD")
            if not pwd:
                pwd = input("Password: ")
    if not url:
        url = os.getenv("URL")
        if not url:
            url = get_data_from_json(json_filename).get("URL")
            if not url:
                url = input("URL: ")
    if not timeout:
        try:
            timeout = int(os.getenv("TIMEOUT"))
        except ValueError:
            timeout = None
        if not timeout:
            timeout = get_data_from_json(json_filename).get("TIMEOUT")
            if not timeout:
                while True:
                    try:
                        timeout = int(input("Timeout: "))
                        if timeout < 5:
                            print("Timeout must not be less than 5")
                        else:
                            break
                    except ValueError:
                        print("Invalid timeout")

    return debug, usr, pwd, url, timeout

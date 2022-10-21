"""Functions to get the credentials"""
from json import load
import json
import os

JSON_FILENAME = "Sentral_Details.json"


def get_data_from_json(json_file: str) -> dict:
    """
    Get the data from a JSON file
    :param json_file: The name of the json file
    :return: The dictionary of the data
    """
    try:
        with open(json_file, 'r') as f:
            return load(f)
    except:
        return {}


def get_credentials(debug: bool, usr: str, pwd: str, url: str, timeout: int)\
        -> tuple:
    """
    Get the credentials
    :param debug: Weather or not to debug
    :param usr: The username
    :param pwd: The password
    :param url: The URL
    :param timeout: The timeout
    :return: The credentials as a tuple (debug, usr, pwd, url, timeout)
    """
    # Use "is None" instead of "not" for debug because debug could be False
    if debug is None:
        debug = {"True": True, "False": False}.get(os.getenv("DEBUG"))
        if debug is None:
            debug = get_data_from_json(JSON_FILENAME).get("DEBUG")
            if debug is None:
                while True:
                    debug = {"Y": True, "N": False}.get(
                        input("Debug? Y/N: ")[0].upper())
                    if debug is not None:
                        break
    if not usr:
        usr = os.getenv("USER_NAME")
        if not usr:
            usr = get_data_from_json(JSON_FILENAME).get("USERNAME")
            if not usr:
                usr = input("Username: ").lower()
    if not pwd:
        pwd = os.getenv("PASSWORD")
        if not pwd:
            pwd = get_data_from_json(JSON_FILENAME).get("PASSWORD")
            if not pwd:
                pwd = input("Password: ")
    if not url:
        url = os.getenv("URL")
        if not url:
            url = get_data_from_json(JSON_FILENAME).get("URL")
            if not url:
                url = input("URL: ")
    if not timeout:
        try:
            timeout = int(os.getenv("TIMEOUT"))
        except TypeError:
            timeout = None
        except ValueError:
            timeout = None
        if not timeout:
            timeout = get_data_from_json(JSON_FILENAME).get("TIMEOUT")
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

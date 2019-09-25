"""
Module to support identity info output
"""
import requests

def get_public_ip():
    return requests.get('https://api.ipify.org').text
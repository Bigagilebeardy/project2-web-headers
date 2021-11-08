#!/usr/bin/env python3
"""
NAME: check_webheader.py
VERSION: 1.0
AUTHOR: PH (Sgt. Hugo Stiglitz)
STATUS: Still building
DESCRIPTION:
TO-DO: Update as Required
COPYRIGHT © 2021 PH
"""
#Imports
import requests
import json
import socket
import urllib.parse
import argparse


# Added Variables
__author__ = "Sgt. Hugo Stiglitz"
__copyright__ = "COPYRIGHT © 2021 PH"
__license__ = "MIT License"
__version__ = "1.0"


#define argeparse
parser= argparse.ArgumentParser(description = 'Check web header of specific web site or list of urls and return if some headers are not present')
parser.add_argument('-u','--url',metavar=r'http://url.com/', type = str, help = 'put url in argument')
parser.add_argument('-l','--urllist', metavar = 'C:\ListIP.txt',type = str, help = 'give full path for file' )
args = parser.parse_args()

def readUrlFile(filepath):

    listUrls = []
    try:
        with open (filepath, 'r') as f:
            listUrls = f.read().splitlines()
    except FileNotFoundError:
        print("Wrong file or file path")
    finally:
        f.close
    
    return listUrls


def checkHeader(url):
    '''use url has input and return json objects headers'''
    reponse = requests.get(url)
    result = reponse.headers
    return result
        

def isHTTPS(url):
    result = url.split (':')
    
    if result[0] == 'https':
        return True
    else:
        return False

def getIPforURL (url):

    parsed_url = urllib.parse.urlparse(url)
    IPaddr = socket.gethostbyname(parsed_url.netloc)
    return IPaddr 

def printHeaders(arrayToCheck, jsonheader, url):
    print(f'the header for the website {url}\n')

    if arrayToCheck[0] not in jsonheader:
        ipaddr = getIPforURL(url)
        print(f'\tthe website {url} has the ip address: {ipaddr}\n')
    
    if 'Server' in jsonheader:
        print(f'\tthe value Server is {jsonheader["Server"]}\n')

    for i in arrayToCheck:

        if i not in jsonheader:
            #print(f'\tthe value of {i} is {jsonheader[i]} \n')
            print(f'\tthe value {i} is not present!\n')
        


headersToCheck = ['Strict-Transport-Security', 'Content-Security-Policy', 'X-Frame-Options']

if args.url:
    if isHTTPS(args.url):
        result = checkHeader(args.url)
        printHeaders(headersToCheck, result, args.url)

if args.urllist:
    listWebsites = readUrlFile(args.urllist)

    for website in listWebsites:
        if isHTTPS(website):
            result = checkHeader(website)
            printHeaders(headersToCheck, result, website)
        else:
            print(f'the website {website} is not in https! we go to the next website!\n')
    


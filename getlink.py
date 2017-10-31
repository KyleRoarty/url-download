#!/usr/bin/env python

import re
import wget
import validators
import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser


def parseArgs():
    parser = ArgumentParser(prog="download")
    parser.add_argument('url', type=str,
                        help='url to get files from')

    return parser.parse_args()

def loop(domain, url):
    response = requests.get(url)
    slop = BeautifulSoup(response.text, 'html.parser')

    ret_dls = list()

    while True:
        links = slop.findAll('a', rel='bookmark', href=True, text=True)
        for link in links:
            ret_dls += getFiles(domain, link.get('href'))

        if slop.find('link', rel='next', href=True) is None:
            print "None!"
            break
        else:
            print "Looping"
            url = slop.find('link', rel='next', href=True).get('href')
            response = requests.get(url)
            slop = BeautifulSoup(response.text, 'html.parser')

    return ret_dls

def getFiles(domain, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    selection = soup.findAll('a', href=True, target="_blank")

    dls = []

    for link in selection:
        if link.find('i', class_="fa fa-download"):
            l = link.get('href')
        #if not validators.url(l):
        #   dls.append(domain + l)
        #else:
            dls.append(l)

    return dls

def main():

    pargs = parseArgs()

    domain = re.match('^http(s*)://.*?(?=/)', pargs.url).group(0)


    if True:
        dls = loop(domain, pargs.url)
    else:
        dls = getFiles(domain, pargs.url)


    for dl in dls:
        print dl
        #wget.download(dl)

if __name__ == '__main__':
    main()

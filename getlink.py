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

def getFiles(domain, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    selection = soup.select('u a')

    dls = []

    for link in selection:
        l = link.get('href')
        if not validators.url(l):
            dls.append(domain + l)
        else:
            dls.append(l)

    return dls

def main():

    pargs = parseArgs()

    domain = re.match('^http(s*)://.*?(?=/)', pargs.url).group(0)

    dls = getFiles(domain, pargs.url)
    for dl in dls:
        wget.download(dl)

if __name__ == '__main__':
    main()

#!/usr/bin/env python

import re
import wget
import validators
import requests
import time
import concurrent.futures
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

        executor = concurrent.futures.ThreadPoolExecutor(10)
        ret_dls += [executor.submit(getFiles, domain, link.get('href')) for link in links]
        concurrent.futures.wait(ret_dls)

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
            dls += l

    return dls

def download(future):
    wget.download(''.join(future.result()))

def main():

    pargs = parseArgs()

    domain = re.match('^http(s*)://.*?(?=/)', pargs.url).group(0)


    if True:
        start = time.time()
        dls = loop(domain, pargs.url)
        end = time.time()
        diff_get_links = end-start
    else:
        dls = getFiles(domain, pargs.url)



    start = time.time()
    executor = concurrent.futures.ThreadPoolExecutor(len(dls))
    futures = [executor.submit(download, dl) for dl in dls]
    concurrent.futures.wait(futures)
    end = time.time()
    print diff_get_links
    print end-start
#    for dl in dls:
#        print ''.join(dl.result())
#        wget.download(dl)

if __name__ == '__main__':
    main()

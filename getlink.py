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

def parseFunc(domain, url):
    print url
    response = requests.get(url)
    sloop = BeautifulSoup(response.text, 'html.parser')
    links = sloop.findAll('a', rel='bookmark', href=True, text=True)

    futs = list()

    exc = concurrent.futures.ProcessPoolExecutor(10)
    futs += [exc.submit(getFiles, domain, link.get('href')) for link in links]
    concurrent.futures.wait(futs)


    exc.shutdown(True)
    return [fut.result() for fut in futs]

def loop(domain, url):
    response = requests.get(url)
    slop = BeautifulSoup(response.text, 'html.parser')
    i = 1
    ret_dls = list()

    urlList = [url]

    while True:
        if slop.find('link', rel='next', href=True) is None:
            break
        else:
            print i
            i += 1
            url = slop.find('link', rel='next', href=True).get('href')
            response = requests.get(url)
            slop = BeautifulSoup(response.text, 'html.parser')
            urlList += [url]
    futures = list()
    exc1 = concurrent.futures.ThreadPoolExecutor(10)
    futures += [exc1.submit(parseFunc, domain, url) for url in urlList]
    concurrent.futures.wait(futures)
    exc1.shutdown(True)
    return futures

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

def download(url):
    wget.download(''.join(url))

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


    print len(dls)
    start = time.time()
    dls = [dl.result() for dl in dls]
    dls = [url for dl in dls for url in dl]
    print len(dls)
    executor = concurrent.futures.ThreadPoolExecutor(100)
    futures = [executor.submit(download, dl) for dl in dls]
    concurrent.futures.wait(futures)
    end = time.time()
    print "\n"+str(diff_get_links)
    print end-start

if __name__ == '__main__':
    main()

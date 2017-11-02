#!/bin/bash

wget := venv/lib/python2.7/site-packages/wget.py
vals := venv/lib/python2.7/site-packages/validators/
requests := venv/lib/python2.7/site-packages/requests/
bs := venv/lib/python2.7/site-packages/bs4/
futures := venv/lib/python2.7/site-packages/futures/

work: $(wget) $(vals) $(requests) $(bs) $(futures)

venv:
		virtualenv venv; . venv/bin/activate; pip install --upgrade pip

$(wget): venv
		. venv/bin/activate; pip install wget

$(vals): venv
		. venv/bin/activate; pip install validators

$(requests): venv
		. venv/bin/activate; pip install requests

$(bs): venv
		. venv/bin/activate; pip install beautifulsoup4

$(futures): venv
		. venv/bin/activate; pip install futures

wget := venv/lib/python2.7/site-packages/wget.py
vals := venv/lib/python2.7/site-packages/validators/
requests := venv/lib/python2.7/site-packages/requests/
bs := venv/lib/python2.7/site-packages/bs4/
#Put 'futures' here
work: $(wget) $(vals) $(requests) $(bs)

venv:
		virtualenv $@

$(wget): venv
		. venv/bin/activate; pip install wget

$(vals): venv
		. venv/bin/activate; pip install validators

$(requests): venv
		. venv/bin/activate; pip install requests

$(bs): venv
		. venv/bin/activate; pip install beautifulsoup4

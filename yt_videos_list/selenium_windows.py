import re
import sys
import json
import subprocess


def firefox_exists(browser):
    return browser in subprocess.getoutput(r'dir "C:\Program Files"')

def opera_exists(browser):
    user = subprocess.getoutput("whoami").split('\\')[1]
    return browser in subprocess.getoutput(rf'dir C:\Users\{user}\AppData\Local\Programs')

def chrome_exists(browser):
    return browser in  subprocess.getoutput(rf'dir "C:\Program Files (x86)\Google"')

def browser_exists(browser):
    if   browser == 'Mozilla Firefox': return firefox_exists(browser)
    elif browser == 'Opera':           return opera_exists(browser)
    elif browser == 'Chrome':          return chrome_exists(browser)


def get_firefox_version():
    firefox = subprocess.getoutput(r'more "C:\Program Files\Mozilla Firefox\application.ini"')
    return re.search('MinVersion=(\d+\.[\d\.]*)', firefox)[1]

def get_opera_version():
    user = subprocess.getoutput("whoami").split('\\')[1]
    with open(rf'C:\Users\{user}\AppData\Local\Programs\Opera\installation_status.json', 'r') as f:
        opera = json.load(f)
    return opera['_subfolder']

def get_chrome_version():
    chrome = subprocess.getoutput(r'dir "C:\Program Files (x86)\Google\Chrome\Application"')
    return re.search('(\d\d\.[\d\.]*)', chrome)[1]

def get_browser_version(browser):
    if   browser == 'Mozilla Firefox': return get_firefox_version()
    elif browser == 'Opera':           return get_opera_version()
    elif browser == 'Chrome':          return get_chrome_version()

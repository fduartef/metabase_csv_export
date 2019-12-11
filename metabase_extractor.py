#!/usr/bin/python

import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import os
import glob

'''
Using selenium and Firefox Driver, this script finds a metabase question, logs in and downloads it's results as an CSV file. 

After that, it renames the last downloaded file on the destination folder to the question number.

Usage:

python3 metabase_extractor.py -q https://metabase.example.com/question/1010 -d ~/Documents/Dev/Folder -u your@email.com -p yourpasswd --timer 10  

'''

def parse_arguments():
    # initialize argumentparser and arguments
    parser = argparse.ArgumentParser(description='Takes a metabase question and downloads an csv')
    parser.add_argument('-q', '--question', dest='questionurl', help='URL of metabase question', required=True)
    parser.add_argument('-d', '--destination', dest='destination', help='Destination', required=True)
    parser.add_argument('-u', '--user', dest='user', help='Your metabase username', required=True)
    parser.add_argument('-p', '--password', dest='password', help='Your metabase username', required=True)
    parser.add_argument('-t', '--timer', dest='timer', help='How much time to wait to load and download file', required=True)

    # parse arguments
    args = parser.parse_args()
    return args

def rename_file(destination, questionurl):

    list_of_files = glob.glob(destination+'*.csv') 

    latest_file = max(list_of_files, key=os.path.getctime)
    
    questionnum = str(questionurl)

    questionnum = questionnum[questionnum.rfind("/")+1:len(questionnum)]

    if os.path.isfile(destination+questionnum+".csv"):
        os.remove(questionnum+".csv")
        os.rename(latest_file, destination+questionnum+".csv")
        print('File renamed to '+questionnum+".csv")

    else:
        os.rename(latest_file, destination+questionnum+".csv")
        print('File renamed to '+questionnum+".csv")
        

def main():
    # parse arguments
    args = parse_arguments()

    # To prevent download dialog
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2) # custom location
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', args.destination)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

    print('Destination folder set to '+args.destination)


    display = Display(visible=0, size=(1024, 768))
    display.start()

    print('Started virtual display')

    browser = webdriver.Firefox(profile)


    print('Browser initialized')

    browser.get(args.questionurl)


    print('Got question url: '+args.questionurl)

    element = browser.find_element_by_name("username")
    element.send_keys(args.user)
    element = browser.find_element_by_name("password")
    element.send_keys(args.password)
    element.send_keys(Keys.RETURN)

    print('Logged in. Loading question.')

    print('Loading timer:')

    for i in reversed(range(0, int(args.timer))):
        time.sleep(1)
        print(i)


    element = browser.find_elements_by_class_name("Icon-download")[0]
    element.click()
    element = browser.find_elements_by_class_name("Icon-csv")[0]
    element.click()

    print('Asked to download file...')
    print('Loading timer:')

    for i in reversed(range(0, int(args.timer))):
        time.sleep(1)
        print(i)


    print('Finished..')

    browser.quit()


    display.stop()


    rename_file(args.destination,args.questionurl)


if __name__ == "__main__":
    main()

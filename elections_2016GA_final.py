import urllib.request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import json
import time
import random
from urllib.request import urlopen
from zipfile import ZipFile
import os
from shutil import copyfile

prefix = 'https://results.enr.clarityelections.com/GA/'

def getPrecinctRequestStringFromCounty(county_name,eid_num):
   request_str = prefix + county_name + "/" + eid_num + "/current_ver.txt"
   return request_str

## Test that we are getting the right information.
#print(getPrecinctRequestStringFromCounty("Bryan","42293"))

def getPrecinctCurrentVersionFromCounty(county_name, eid_num):
   #Grab the URL request to get the current version
   url_request_str = getPrecinctRequestStringFromCounty(county_name,eid_num)
   #request, read, and strip out the file
   # In the case that we are being blocked by the website, put a mandatory delay
   # on our webfile retrieval.
#   time.sleep(10)
   webfile = urllib.request.urlopen(url_request_str)
   lines = webfile.readlines()
   current_precinct_num = lines[0].decode("UTF-8")
   return current_precinct_num

## Test that we are getting the right information.
#print(getPrecinctCurrentVersionFromCounty("Bryan","42293"))

def getPrecinctURLFromCounty(county_name, eid_num, cid_num):
   current_precinct_num = getPrecinctCurrentVersionFromCounty(county_name, 
                                                              eid_num)
   suffix = "/en/md_data.html?cid="
   precinct_url = prefix + county_name + "/" + eid_num + "/" + current_precinct_num + suffix + cid_num
   return precinct_url

## Test that we are getting the right information.
#print(getPrecinctURLFromCounty("Bryan","42293","15"))

def scrapePrecinctURLToDataFrame(precinct_URL,count):
    #create a webdriver that lets us wait out the Javascript
    #as it procedurally generates the HTML, then get
    #the HTML
    wd = webdriver.PhantomJS()
    wd.set_window_size(1120,550)
    WebDriverWait(wd,30)
#    time.sleep(random.random()*30)
    wd.get(precinct_URL)
    html_page = wd.page_source
    wd.quit()
    #use pandas built-in functionality to scrape all tables
    all_tables = pd.read_html(html_page)
    #in all the examples I looked at, the relevant table was the last one
    relevant_table = all_tables[-1]
    relevant_table.drop(relevant_table.columns[[0]], axis=1, inplace=True)
    relevant_table.drop(relevant_table.index[0], inplace = True)
#    relevant_table.drop(relevant_table.index[-1],inplace=True)
    relevant_table = relevant_table[~relevant_table[1].str.contains('Total:')]
#    if count!=0:
#        relevant_table = relevant_table[~relevant_table[1].str.contains('Precinct')]
    relevant_table = relevant_table[~relevant_table[1].str.contains('Precinct')]
    return relevant_table

#table_to_scrape = scrapePrecinctURLToDataFrame('https://results.enr.clarityelections.com/GA/Appling/63993/112231/en/md_data.html?cid=1',0)

#print(str(table_to_scrape))

def getAllPrecinctDataFrames(county_name_list, eid_num_list, cid_num_list):

   data_frames = []
   for i in range(len(county_name_list)):
       try:
           precinct_URL = getPrecinctURLFromCounty(county_name_list[i],
                                             eid_num_list[i],
                                             cid_num_list[i])
           precinct_data_frame = scrapePrecinctURLToDataFrame(precinct_URL,i)
           print(precinct_data_frame)
           data_frames.append(precinct_data_frame)
       except:
           print('oops') #in the future, print where the errors were located.
           with open("errors.txt","a+") as f:
               f.write(precinct_URL + '\n')
   return data_frames

f1 = open('sum2016.json','r')
f2 = open('details2016.json','r')

sum_data = json.load(f1)
details_data = json.load(f2)

the_contests = details_data['Contests']
#print(len(the_contests))

our_contest = the_contests[1]
our_county_name_list = our_contest['P']
our_eid_num_list = our_contest['Eid']
our_cid_num_list = our_contest['Cid']

## Test that we are getting the right information.
#print(getPrecinctRequestStringFromCounty(our_county_name_list,our_eid_num_list))
#print(our_county_name_list)
#print(our_eid_num_list)

suffix = 'reports/detailxls.zip'
for x in range(len(our_county_name_list)):
    if len(str.split(our_county_name_list[x]))>1:
        our_county_name_list[x] = '_'.join(str.split(our_county_name_list[x]))

    precinct_num = getPrecinctCurrentVersionFromCounty(our_county_name_list[x],our_eid_num_list[x])
    html_site = prefix + our_county_name_list[x] + '/' + our_eid_num_list[x] + '/' + precinct_num + '/' + suffix
    print(html_site)

    zipurl = html_site
    # Download the file from the URL
    zipresp = urlopen(zipurl)
    # Create a new file on the hard drive
    tempzip = open("/tmp/tempfile.zip", "wb")
    # Write the contents of the downloaded file into the new file
    tempzip.write(zipresp.read())
    # Close the newly-created file
    tempzip.close()
    # Re-open the newly-created file with ZipFile()
    zf = ZipFile("/tmp/tempfile.zip")
    # Extract its contents into destination folder
    # note that extractall will automatically create the path
    zf.extractall(path = 'C:\\Users\\jasplund\\Dropbox\\research\\gerry\\voting_data\\data\\2016')
    # close the ZipFile instance
    zf.close()

#    path =  'C:\\Users\\jasplund\\Dropbox\\research\\gerry\\voting_data\\data'
#    filenames = os.listdir(path)
    
    copyfile('C:\\Users\\jasplund\\Dropbox\\research\\gerry\\voting_data\\data\\2016\\'+'detail.xls', 
             'C:\\Users\\jasplund\\Dropbox\\research\\gerry\\voting_data\\data\\2016\\'+our_county_name_list[x]+'_precinct_data_2012.xls')


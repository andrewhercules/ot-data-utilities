#!/usr/bin/env python

"""
Generate Remove Outdated Content URL Reports
This script will search Google for a specific develoment branch of the Open Targets Platform, 
scrape the URLs from the first 100 results, and generate a list of URLs that can be submitted 
to Google's Remove Outdated Content tool.

To run the script, you will require:

1. A specific Platform branch that you want to remove from Google that has been incorrectly 
indexed (e.g. EFO3 or shipit)
2. An account with Zenserp (note: the free account with Zenserp is limited to 50 Google 
Search API calls per month - if the branch you want to remove from Google has more than 
100 results, increase the number_of_search_results_to_include value)

To find specific Platform branches that have been incorrectly indexed by Google, please 
run the following Google search:

site:*.targetvalidation.org -www -qa

This will search for any URLs that include .targetvalidation.org but will exclude 
www.targetvalidation.org and qa.targetvalidation.org - these are valid URLs for now, 
pending further review of the Platform architecture.
"""

# import relevant libraries
import requests
import csv
import datetime
import os

# set variables needed s for script to run
zenserp_api_key = '4f9da060-c970-11e9-9159-e767a8b965a3'
platform_branch = 'efo3.targetvalidation.org'
number_of_search_results_to_include = 100
csv_data = []

# set Zenserp API key
headers = {
    'apikey': zenserp_api_key,
}

# set Google search parameters
params = (
    ('q', 'site:' + platform_branch),
    ('location', 'United States'),
    ('search_engine', 'google.com'),
    ('gl', 'US'),
    ('hl', 'en'),
    ('num', number_of_search_results_to_include)
)

# run Google search and store results
response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params)
search_data = response.json()
print('There are %i results from this query' % (len(search_data['organic'])))

# generate list of URLs from Google search results
for result in search_data['organic']:
    csv_data.append(result['url'])

# set date and file name and directory
today_date = datetime.datetime.now().strftime('%Y-%m-%d')
full_report_filename = os.path.join('reports/', today_date + '_' + platform_branch + '_report.csv')

# generate and save CSV with URLs to be removed from Google
with open(full_report_filename, 'w') as myfile:
    wr = csv.writer(myfile, delimiter='\n')
    wr.writerow(csv_data)
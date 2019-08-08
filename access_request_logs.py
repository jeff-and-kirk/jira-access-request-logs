""" 
Automate the running of access request logs for each month and write a 
report into an S3 bucket serving as an artifact for auditing.
"""
import csv
from jira import JIRA
import json
import datetime
import urllib
import botocore
import datetime
from pandas import DataFrame # may be missing some of Pandas modules to make this run effectively
import re

jira_server = (os.getenv(server_location))
user_id = (os.getenv(username))
user_pass = (os.getenv(password))
options = {'server' : jira_server}
# for auth and pass, will need to create secrets, env var or something secure in AWS
# I validated the response and auth via a successful search in CLI
jira = JIRA(options, basic_auth=(user_id, user_pass))

jira_access_report = jira.search_issues('filter=17648', maxResults=500)

# creating lists, iterating through json response of monthly access request query via Rest API service
# below will be CSV columns - each list will be a line row within the column
key_id = []
summaries = []
reporter_list = []
user_needing_access = []
systems_access = []
assignee = []
secops_verified_manager = []
reporting_manager = []
fixed_time_period = []
start_access_on = []
revoke_access_on = []
description = []
access_resolved_on = []


for issue in jira_access_report:
    jira_key = issue.key
    summary = issue.fields.summary
    reporter = issue.fields.reporter
    # r = re.compile("displayName=\\b")
    # reported_by = re.findall(r'displayName=[^\b]+', str(reporter))
    needed_for = issue.fields.customfield_14903
    systems = []
    tempsystems = issue.fields.customfield_14905
    if tempsystems:
        for system in tempsystems:
            systems.append(str(system))
    assignees = issue.fields.assignee
    date_of_verification = issue.fields.customfield_14910
    authorizing_agent = issue.fields.customfield_14904
    fixed = issue.fields.customfield_14906
    start_on = issue.fields.customfield_14301
    revoke_on = issue.fields.customfield_14908
    descriptions = issue.fields.description
    resolved = issue.fields.resolutiondate
    key_id.append(jira_key)
    summaries.append(summary)
    reporter_list.append(reporter) # Need to come back and determine just how to print the display name only - will need to parse this, need to look up parsing response
    user_needing_access.append(needed_for)
    systems_access.append(', '.join(systems))
    assignee.append(assignees)
    secops_verified_manager.append(date_of_verification)
    reporting_manager.append(authorizing_agent)
    fixed_time_period.append(fixed)
    start_access_on.append(start_on)
    revoke_access_on.append(revoke_on)
    description.append(descriptions)
    access_resolved_on.append(resolved)

# reporter_string = ''.join(reporter_list)
# reporters = re.findall(r"displayName=\'[^]+\'", str(reporter_list))
# name = [i for i, item in reporter_list if re.search('displayName', item)]

# print(name)

# issue_detail = (key_id[0], ":", systems_access[0])

# for items in jira_access_report:
#     print(issue_detail)

# below is the command to take above data and create a CSV file
table_file = {'JIRA Key ID': key_id,
        'Summary': summaries,
        'Person Filing The Request': reporter_list,
        'Person Needing Access': user_needing_access,
        'Systems Need Access To': systems_access,
        'SecOps Operator Expediting': assignee,
        'Time of Access Verification': secops_verified_manager,
        'Mgr of Person Needing Access': reporting_manager,
        'Need for Fixed Time Period': fixed_time_period,
        'Access Starts On': start_access_on,
        'Must Revoke On': revoke_access_on,
        'Details of Access Need': description,
        'Access Request Closed On': access_resolved_on
    }
date = str(datetime.date.today())
filename = date +'_access_request_log'
df = DataFrame(table_file, columns= ['JIRA Key ID', 'Summary', 'Person Filing The Request', 'Person Needing Access', 'Systems Need Access To', 'SecOps Operater Expediting', 'Time of Access Verification', 'Mgr of Person Needing Access', 'Needed for Fixed Time Period', 'Access Starts On', 'Must Revoke On', 'Details of Access Need', 'Access Request Closed On'])
export_csv = df.to_csv (f'/Users/jeffkoors/Documents/Git/csv_processor/{filename}.csv', index = None, header=True) # need to find path or write to S3 bucket
print (df)


# table_set = 
# print(fields)
# for issue in jira_access_report:
    

# print(jira_access_report)


#         self.key = issue.key
#         self.summary = issue.fields.summary
#         self.reporter = issue.fields.reporter
#         self.needed_for = 'id': 'customfield_14903'
#         self.assignee = issue.fields.assignee
#         self.provided_by = 'id': 'customfield_14911',
#         self.date_verified = 'id': 'customfield_14910'
#         self.authorize_agent = 'id': 'customfield_14904'
#         self.systems = 'id': 'customfield_14905'
#         self.permissions = 'id': 'customfield_14907'
#         self.fixed = 'id': 'customfield_14906
#         self.start = 'id': 'customfield_14301'
#         self.revoke = 'id': 'customfield_14908'
#         self.description = issue.fields.description
#         self.resolved = issue.fields.resolved

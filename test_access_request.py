"""
Testing creating 1 Access Request via REST API
"""

import csv
from jira import JIRA
import json
import datetime

jira_server = "https://jira.corp.phishme.com"
user_id = 'Jeff.Koors@cofense.com'
user_pass = 'GavHeartLacKel1977!'
options = {'server' : jira_server}
jira = JIRA(options, basic_auth=(user_id, user_pass))

email = "Mark.Zigadlo@cofense.com"
issue_dict = {
    'project': {'key': 'PRODENG'},
    'priority': {'name': '2 - High'},
    'summary': 'JEFFREY TEST AGAIN',
    'description': 'JEFFREY TESTING ONE MORE TIME',
    'issuetype': {'name': 'Access Request'},       
    'customfield_14904': {'name': email},
    'customfield_14905': [{'value': 'Other'}],
    'customfield_14907' : [{'value': 'Other'}],
}

new_issue = jira.create_issue(fields=issue_dict)

for issue in issues:
    print(issue)
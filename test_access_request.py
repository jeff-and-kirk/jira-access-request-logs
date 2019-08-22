"""
Testing creating 1 Access Request via REST API
"""

import csv
from jira import JIRA
import json
import datetime

jira_server = (os.getenv(server_location))
user_id = (os.getenv(username))
user_pass = (os.getenv(password))
options = {'server' : jira_server}
jira = JIRA(options, basic_auth=(user_id, user_pass))

email = "John.Doe@cofense.com"
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

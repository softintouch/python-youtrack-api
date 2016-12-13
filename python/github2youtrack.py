#! /usr/bin/env python

import csv
import sys

import requests

import csv2youtrack
import csvClient
from youtrack.importHelper import utf8encode

csvClient.FIELD_NAMES = {
    "Project Name" : "project_name",
    "Project Id"   : "project_id",
    "Summary"      : "summary",
    "State"        : "State",
    "Id"           : "numberInProject",
    "Created"      : "created",
    "Updated"      : "updated",
    "Resolved"     : "resolved",
    "Assignee"     : "Assignee",
    "Description"  : "description",
    "Labels"       : "Labels",
    "Author"       : "reporterName",
    "Milestone"    : "Fix versions"
}

csvClient.FIELD_TYPES = {
    "State"        : "state[1]",
    "Assignee"     : "user[1]",
    "Labels"       : "enum[*]",
    "Fix versions" : "version[*]",
    "Type"         : "enum[1]"
}

csvClient.DATE_FORMAT_STRING = "%Y-%m-%dT%H:%M:%SZ"
csvClient.VALUE_DELIMITER = "|"

CSV_FILE = "github2youtrack-{repo}-{data}.csv"


def main():
    github_user, github_password, github_repo, youtrack_url, youtrack_login, youtrack_password = sys.argv[1:8]
    issues_csv_file = CSV_FILE.format(repo=github_repo, data='issues')
    comments_csv_file = CSV_FILE.format(repo=github_repo, data='comments')
    github2csv(issues_csv_file, comments_csv_file, github_user, github_password, github_repo)
    csv2youtrack.csv2youtrack(issues_csv_file, youtrack_url, youtrack_login, youtrack_password, comments_csv_file)

def get_last_part_of_url(url_string):
    return url_string.split('/').pop()

# based on https://gist.github.com/unbracketed/3380407
def write_issues(r, issues_csvout, comments_csvout, repo, auth):
    "output a list of issues to csv"
    if not r.status_code == 200:
        raise Exception(r.status_code)
    for issue in r.json():
        labels = []
        labels_lowercase = []
        for label in issue['labels']:
            label_name = label.get('name')
            if not label_name:
                continue
            labels.append(label_name)
            labels_lowercase.append(label_name)

        # TODO: Join writerow
        #labels = csvClient.VALUE_DELIMITER.join([str(x) for x in labels])

        assignee = issue['assignee']
        if assignee:
            assignee = assignee.get('login')
        else:
            assignee = ""

        created = issue['created_at']
        updated = issue.get('updated_at', '')
        resolved = issue.get('closed_at', '')

        author = issue['user'].get('login')
        if not author:
            author = get_last_part_of_url(issue['user'].get('url'))

        project = get_last_part_of_url(repo)

        milestone = issue.get('milestone')
        if milestone:
            milestone = milestone['title']
        else:
            milestone = ''

        state = issue['state'].lower()
        if state == 'closed':
            if 'wontfix' in labels_lowercase or 'invalid' in labels_lowercase:
                state = "Won't fix"
            else:
                state = "Fixed"

        issue_type = 'Task'
        if 'bug' in labels_lowercase:
            issue_type = 'Bug'

        issue_row = [project, project, issue['number'], state, issue['title'],
                     issue['body'], created, updated, resolved, author or 'guest',
                     assignee, csvClient.VALUE_DELIMITER.join(labels),
                     issue_type, milestone]
        issues_csvout.writerow([utf8encode(e) for e in issue_row])
        
        if int(issue.get('comments', 0)) > 0 and 'comments_url' in issue:
            rc = requests.get(issue['comments_url'], auth=auth)
            if not rc.status_code == 200:
                raise Exception(r.status_code)
            for comment in rc.json():
                author = comment['user'].get('login')
                if not author:
                    author = get_last_part_of_url(comment['user'].get(u'url'))
                comment_row = [project, issue['number'], author or 'guest',
                               comment['created_at'], comment['body']]
                comments_csvout.writerow([utf8encode(e) for e in comment_row])


def github2csv(issues_csv_file, comments_csv_file, github_user, github_password, github_repo):
    issues_url = 'https://api.github.com/repos/%s/%s/issues?state=all' % (github_user, github_repo)
    AUTH = (github_user, github_password)

    r = requests.get(issues_url, auth=AUTH)
    issues_csvout = csv.writer(open(issues_csv_file, 'wb'))
    issues_csvout.writerow(
        ('Project Name', 'Project Id', 'Id', 'State', 'Summary', 'Description',
         'Created', 'Updated', 'Resolved', 'Author', 'Assignee', 'Labels',
         'Type', 'Milestone'))
    comments_csvout = csv.writer(open(comments_csv_file, 'wb'))
    write_issues(r, issues_csvout, comments_csvout, github_repo, AUTH)

    #more pages? examine the 'link' header returned
    if 'link' in r.headers:
        pages = dict(
            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])
        while 'last' in pages and 'next' in pages:
            r = requests.get(pages['next'], auth=AUTH)
            write_issues(r, issues_csvout, github_repo)
            if pages['next'] == pages['last']:
                break


if __name__ == "__main__":
    main()

from setuptools import setup, find_packages

# from distutils.core import setup

setup(
    name='python-youtrack-api',
    version='1.0.0',
    description='Python client for JetBrains\' YouTrack REST API',
    packages=[
    'agilezen', 'agilezen2youtrack.py', 'bitbucket-broker.py', 'bugzilla', 'bugzilla2youtrack.py', 'build.xml',
    'copyOneIssue.py', 'csv2youtrack.py', 'csvClient', 'deleteAllUsers.py', 'fb2youtrack.py', 'fbugz',
    'getAllEmailsFromProject.py', 'github2youtrack.py', 'googleCode', 'googleCode2youtrack.py', 'httplib2', 'jira',
    'jira2youtrack.py', 'jiraSOAP2youtrack.py', 'mantis', 'mantis2youtrack.py', 'moveIssue.py', 'out',
    'pyactiveresource', 'Python.iml', 'redmine', 'redmine2youtrack.py', 'socks.py', 'sync', 'syncYtWithYt.py',
    'sync_config', 'test.py', 'tests', 'trac2youtrack.py', 'tracLib', 'urllib2_file.py', 'userTool.py', 'youtrack',
    'youtrack2youtrack.py', 'youtrackImporter.py', 'youtrackRestSamples.py', 'zendesk', 'zendesk2youtrack.py']
)

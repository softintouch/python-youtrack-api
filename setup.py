from setuptools import setup, find_packages

# from distutils.core import setup

setup(
    name='python-youtrack-api',
    version='1.0.0',
    description='Python client for JetBrains\' YouTrack REST API',
    packages=[
        'sit-youtrack', 'sit-youtrack.agilezen',
        'sit-youtrack.bugzilla', 'sit-youtrack.csvClient',
        'sit-youtrack.fbugz', 'sit-youtrack.googleCode', 'sit-youtrack.httplib2', 'sit-youtrack.jira',
        'sit-youtrack.mantis',
        'sit-youtrack.out', 'sit-youtrack.pyactiveresource', 'sit-youtrack.redmine', 'sit-youtrack.sync',
        'sit-youtrack.tests',
        'sit-youtrack.tracLib', 'sit-youtrack.youtrack', 'sit-youtrack.zendesk'
    ],
)

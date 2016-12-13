from setuptools import setup, find_packages

# from distutils.core import setup

setup(
    name='python-youtrack-api',
    version='1.0.0',
    description='Python client for JetBrains\' YouTrack REST API',
    packages=[
        'python', 'python.agilezen',
        'python.bugzilla', 'python.csvClient',
        'python.fbugz', 'python.googleCode', 'python.httplib2', 'python.jira', 'python.mantis',
        'python.out', 'python.pyactiveresource', 'python.redmine', 'python.sync', 'python.tests',
        'python.tracLib', 'python.youtrack', 'python.zendesk'
    ],
)

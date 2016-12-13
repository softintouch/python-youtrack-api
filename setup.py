from setuptools import setup, find_packages

# from distutils.core import setup

setup(
    name='python-youtrack-api',
    version='1.0.0',
    description='Python client for JetBrains\' YouTrack REST API',
    packages=[
        'sit_youtrack', 'sit_youtrack.agilezen',
        'sit_youtrack.bugzilla', 'sit_youtrack.csvClient',
        'sit_youtrack.fbugz', 'sit_youtrack.googleCode', 'sit_youtrack.httplib2', 'sit_youtrack.jira',
        'sit_youtrack.mantis',
        'sit_youtrack.out', 'sit_youtrack.pyactiveresource', 'sit_youtrack.redmine', 'sit_youtrack.sync',
        'sit_youtrack.tests',
        'sit_youtrack.tracLib', 'sit_youtrack.youtrack', 'sit_youtrack.zendesk'
    ],
    namespace_packages = ['sit_youtrack']
)

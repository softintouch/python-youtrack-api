from setuptools import setup, find_packages

# from distutils.core import setup

setup(
    name='python-youtrack-api',
    version='1.0.0',
    description='Python client for JetBrains\' YouTrack REST API',
    packages=[
        'python-youtrack-api', 'python-youtrack-api.python', 'python-youtrack-api.python.agilezen',
        'python-youtrack-api.python.bugzilla', 'python-youtrack-api.python.csvClient',
        'python-youtrack-api.python.fbugz', 'python-youtrack-api.python.googleCode'
    ],
)

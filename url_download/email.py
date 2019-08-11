"""
@author: shishir bondre

This is general email settings file.
Here you customize your subject line and body
"""


def email_subject():
    return "List of downloaded URLS"


def email_body():
    return "Hi," \
           "Your request for downloading url is successfully completed. " \
           "We have attached zip files of your requested list of urls." \
           "Regards"

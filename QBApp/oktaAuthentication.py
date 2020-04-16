# QBApp/oktaAuthentication.py
"""
Created on Wed Feb 3 10:16:40 2020

Functions to authenticate and atuhorize user through Okta

@author: jaimeHMol
"""
# TODO: Implement the requests as objects (classes)

import requests
import json
import logging


def userLogin(email, password):
    """ Calling Okta API to get the authentication of the user is accessing
        and retrieve their first and last name
    """

    domain = email.split('@')[1].split('.')[0]
    endpoint = "https://" + domain + ".okta.com/api/v1/authn"
    authenticated = False
    userFullName = email.split('@')[0]


    data = """
    {
      "username": \"""" + email + """\",
      "password": \"""" + password + """\",
      "options": {
        "multiOptionalFactorEnroll": true,
        "warnBeforePasswordExpired": true
      }
    }"""

    headers = {
        'accept': "application/json",
        'content-type': "application/json"
    }

    response = requests.post(endpoint, headers= headers, data= data)
    if (response.status_code == 200):
        authenticated = True

        responseJSON = json.loads(response.text)
        userFirstName = responseJSON["_embedded"]["user"]["profile"]["firstName"]
        userLastName = responseJSON["_embedded"]["user"]["profile"]["lastName"]
        userFullName = userFirstName + ' ' + userLastName

        logging.info(" ")
        logging.info(" ")
        logging.info("*** [Debug]: " + email + " succesfully authenticated by okta.")
    else:
        logging.info(" ")
        logging.info(" ")
        logging.info("*** [Debug]: " + email + " haven't been authenticated through okta.")

    return authenticated, userFullName

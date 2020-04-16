# QBApp/QBSession.py
"""
Created on Tue Mar 10 10:26:40 2020

Definition of the QB Session object, an interface to interact with the http Django
session in the way needed and structured for the QB.

@author: jaimeHMol
"""

# HINT: Not implmented yet
import logging


class QBSession:
    """ Object with the specific attributes and methods needed by the QB
        behavior.
    """

    # Create a QB Session with the basic data
    def __init__(self, request):
        self.identity = {"user": "",
                         "email": "",
                         "enterprise": "",
                         "key": "",
                         "userFullName": "",
                         "boomiAccountId": "",
                         "boomiToken": ""}

        self.inputFilters = {"atom": "",
                             "process": ""}

        self.dataCached = {"processName2": "",
                     "atomName": "",
                     "cadence": "",
                     "enable": "",
                     "lastExec": "",
                     "durAvg":"",
                     "deployed": "",
                     "atomID": "",
                     "processId":"",
                     "scheduleId": ""}

        # All the variables cached for the UI
        self.cache = {"re": [],
                      "atomEnvironmentList": [],
                      "processesCount": "",
                      "resultsCount": "", # TODO: Change to schedulesCount
                      "resultsDeployments": "", # TODO: Change to deploymentsCount
                      "showError":""}

        self.metadata = {"id": "1234",
                         "lastLoginDate": "",
                         "extent": "",
                         "location": "",
                         "customer": "",
                         "dataProvider": ""}

        logging.info("Session id: " + self.metadata["id"] + " created")


    def read(self, request):
        logging.info("Checking the session id: " + self.metadata["id"])


    def renew(self, request):
        logging.info("Renewing the session id: " + self.metadata["id"])


    def destroy(self, request):
        redirectPage = "index.html"
        logging.info("Destroying the session id: " + self.metadata["id"])
        return redirectPage

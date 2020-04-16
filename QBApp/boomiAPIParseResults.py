# QBApp/boomiAPIParseResults.py
"""
Created on Wed Jan 8 10:16:40 2020

Functions to parse all the boomi atomspnere API calls, retrieving always the fields:
    * count: (Integer).
    * error: (Bolean).
    * results: List of tuples of (id, name, other fields), usually sort by name (index 1)
    * additional info (List).
    * query token (String) used when Boomi Atomsphere API paginates a query (more than 100 rows on th results).

@author: jaimeHMol
"""
# TODO: REFACTOR: Implement the parse and error handling as methods of every object
#                 created on the requests.
# TODO: Improve performance of the recursion implemented for the pagination
# TODO: Unify XML Name Spaces

from . import boomiAPIBuildRequests

import xml.etree.ElementTree as ET
import logging

XMLNAMESPACES = {"xsi": "http://www.w3.org/2001/XMLSchema-instance",
                 "bns": "http://api.platform.boomi.com/"}

def environmentList(environmentsResponse):
    """ Parsing the list of environments received on the response input obtained from Boomi Atompshere API.
    """
    count = 0            # Mandatory
    error = False        # Mandatory
    results = []         # Mandatory
    additional = []      # Optional
    queryToken = ''      # Optional

    environmentsResponseXML = ET.fromstring(environmentsResponse)

    if environmentsResponseXML.tag != "error":

        count = environmentsResponseXML.get("numberOfResults")
        logging.info("*** [Info] total number of results (environments): " + count)

        i = 0
        for child in environmentsResponseXML:
            if child.tag == "{http://api.platform.boomi.com/}result":
                i = i + 1
                results.append((i, child.get("name")))
            elif child.tag == "{http://api.platform.boomi.com/}queryToken":
                queryToken = child.text

        results.sort(key = lambda tup: tup[1])
        results.insert(0,("","Choose..."))

    else:
        error = True
        raise Exception("There is an error on the Boomi atomsphere API response: " + environmentsResponseXML[0].text)

    return count, error, results, additional, queryToken


def atomList(atomsResponse):
    """ Parsing the list of atoms received on the response input obtained from Boomi Atompshere API.
    """
    count = 0       # Mandatory
    error = False   # Mandatory
    results = []    # Mandatory
    additional = [] # Optional
    queryToken = '' # Optional

    atomsResponseXML = ET.fromstring(atomsResponse)

    # logging.info(atomsResponseXML.tag)
    if atomsResponseXML.tag != "error":

        count = atomsResponseXML.get('numberOfResults')
        logging.info("*** [Info] total number of results (atoms): " + count)

        i = 0
        for child in atomsResponseXML:
            if child.tag == "{http://api.platform.boomi.com/}result":
                i = i + 1
                results.append((child.get("id"), child.get("name")))
            elif child.tag == "{http://api.platform.boomi.com/}queryToken":
                queryToken = child.text

        results.sort(key = lambda tup: tup[1])
        logging.info("result: " + str(results))
        results.insert(0,("","Choose..."))

    else:
        error = True
        raise Exception("There is an error on the Boomi atomsphere API response: " + atomsResponseXML[0].text)


    return count, error, results, additional, queryToken


def processList(request, processesResponse):
    """ Parsing the list of processes received on the response input obtained from Boomi Atompshere API.
    """
    count = 0            # Mandatory
    error = False        # Mandatory
    results = []         # Mandatory
    additional = []      # Optional
    queryToken = ''      # Optional
    accResults = []

    processesResponseXML = ET.fromstring(processesResponse)

    if processesResponseXML.tag != "error":

        count = processesResponseXML.get("numberOfResults")
        logging.info("*** [Info] total number of results (processes): " + count)

        i = 0
        for child in processesResponseXML:
            if child.tag == "{http://api.platform.boomi.com/}result": #HINT: Be carefull with the name spaces
                i = i + 1
                results.append((child.get("id"), child.get("name")))
            elif child.tag == "{http://api.platform.boomi.com/}queryToken":
                queryToken = child.text

        # Recursive block to retrieve all the results (using the queryToken)
        # and the pagination used by the Boomi Atomsphere API
        accResults = accResults + results
        if queryToken != '':
            # accResults.append(results)
            processesResponse = boomiAPIBuildRequests.queryPagination(request, "Process", queryToken)
            _, _, newResult, _, _ = processList(request, processesResponse)

            return count, error, accResults + newResult, additional, queryToken
        else:

            accResults.sort(key = lambda tup: tup[1])
            return count, error, accResults, additional, queryToken

        # logging.info("result: " + str(results))
    else:
        error = True
        raise Exception("There is an error on the Boomi atomsphere API response: " + processesResponseXML[0].text)

    return count, error, results, additional, queryToken


def scheduleList(scheduleResponse):
    """ Parsing the list of schedules received on the response input obtained from Boomi Atompshere API.
    """
    count = 0            # Mandatory
    error = False        # Mandatory
    results = []         # Mandatory
    additional = []      # Optional
    queryToken = ''      # Optional

    schedulesResponseXML = ET.fromstring(scheduleResponse)
    if schedulesResponseXML.tag != "error":

        count = schedulesResponseXML.get("numberOfResults")

        i = 0
        for child in schedulesResponseXML:
            if child.tag == "{http://api.platform.boomi.com/}result":
                i = i + 1
                if child.find("bns:Schedule", XMLNAMESPACES) is not None:
                    cadence = child.find("bns:Schedule", XMLNAMESPACES).get("minutes")
                else:
                    cadence = "NA"
                results.append((child.get("atomId"), child.get("processId"), cadence, child.get("id")))
            elif child.tag == "{http://api.platform.boomi.com/}queryToken":
                queryToken = child.text

        results.sort(key = lambda tup: tup[1])

    else:
        error = True
        raise Exception("There is an error on the Boomi atomsphere API response: " + schedulesResponseXML[0].text)

    return count, error, results, additional, queryToken


def scheduleStatusGet(scheduleGetResponse):
    """ Parsing the schedule status received on the response input obtained from Boomi Atompshere API.
    """
    error = False        # Mandatory
    result = ''          # Mandatory

    scheduleGetResponseXML = ET.fromstring(scheduleGetResponse)
    if scheduleGetResponseXML.tag != "error":
        if scheduleGetResponseXML.get("enabled") == "true":
            result = "Yes"
        elif scheduleGetResponseXML.get("enabled") == "false":
            result = "No"
    else:
        error = True
        raise Exception("There is an error on the Boomi atomsphere API response: " + scheduleGetResponseXML[0].text)

    return error, result


def executionRecordList(executionResponse):
    """ Parsing the list of executions received on the response input obtained from Boomi Atompshere API.
    """
    count = 0             # Mandatory
    error = False         # Mandatory
    results = []           # Mandatory
    additional = []       # Optional
    queryToken = ''       # Optional

    executionsResponseXML = ET.fromstring(executionResponse)
    if executionsResponseXML.tag != "error":

        count = executionsResponseXML.get("numberOfResults")
        logging.info("*** [Info] total number of results (executions): " + count)


    else:
        error = True
        raise Exception("There is an error on the Boomi atomsphere API response: " + executionsResponseXML[0].text)
    pass


def deploymentList(deploymentResponse):
    """ Parsing the list of deployments received on the response input obtained from Boomi Atompshere API.
    """
    count = 0            # Mandatory
    error = False        # Mandatory
    results = []          # Mandatory
    additional = []      # Optional
    queryToken = ''      # Optional

    deploymentResponseXML = ET.fromstring(deploymentResponse)
    if deploymentResponseXML.tag != "error":

        count = deploymentResponseXML.get("numberOfResults")

        i = 0
        for child in deploymentResponseXML:
            if child.tag == "{http://api.platform.boomi.com/}result":
                i = i + 1
                if child.find("bns:processId", XMLNAMESPACES) is not None:
                    procId = child.find("bns:processId", XMLNAMESPACES).text
                if child.find("bns:environmentId", XMLNAMESPACES) is not None:
                    environmentId = child.find("bns:environmentId", XMLNAMESPACES).text

                results.append((procId, environmentId))
            elif child.tag == "{http://api.platform.boomi.com/}queryToken":
                queryToken = child.text

        results.sort(key = lambda tup: tup[1])
        # logging.info("deploymentResult: " + str(results))

    else:
        error = True
        raise Exception("There is an error on the Boomi atomsphere API response: " + deploymentResponseXML[0].text)

    return count, error, results, additional, queryToken


def environmentAtomList(environmentAtomsResponse):
    """ Parsing the list of atoms and their related environments received on the response input obtained from Boomi Atompshere API.
    """
    count = 0       # Mandatory
    error = False   # Mandatory
    results = {}    # Mandatory
    additional = [] # Optional
    queryToken = '' # Optional

    environmentAtomsResponseXML = ET.fromstring(environmentAtomsResponse)

    # logging.info(atomsResponseXML.tag)
    if environmentAtomsResponseXML.tag != "error":

        count = environmentAtomsResponseXML.get('numberOfResults')
        logging.info("*** [Info] total number of results (environment-atoms): " + count)

        i = 0
        for child in environmentAtomsResponseXML:
            if child.tag == "{http://api.platform.boomi.com/}result":
                i = i + 1
                #Devolver un diccionario
                v_atomId, v_environmentId = child.get("atomId"), child.get("environmentId")
                results[v_atomId] = v_environmentId

            elif child.tag == "{http://api.platform.boomi.com/}queryToken":
                queryToken = child.text

        # results.sort(key = lambda tup: tup[1])

    else:
        error = True
        raise Exception("There is an error on the Boomi atomsphere API response: " + environmentAtomsResponseXML[0].text)


    return count, error, results, additional, queryToken


def ProcessEnvironmentAttachment(processEnvironmentAttachmentResponse):
    """ Parsing the Process-Environment attachment information received on the response input obtained from Boomi Atompshere API.
    """
    count = 0       # Mandatory
    error = False   # Mandatory
    results = ''    # Mandatory
    additional = [] # Optional
    queryToken = '' # Optional

    processEnvironmentAttachmentResponseXML = ET.fromstring(processEnvironmentAttachmentResponse)

    # logging.info(atomsResponseXML.tag)
    if processEnvironmentAttachmentResponseXML.tag != "error":

        count = processEnvironmentAttachmentResponseXML.get('numberOfResults')

        i = 0
        for child in processEnvironmentAttachmentResponseXML:
            if child.tag == "{http://api.platform.boomi.com/}result":
                i = i + 1
                results = child.get("id")

            elif child.tag == "{http://api.platform.boomi.com/}queryToken":
                queryToken = child.text

        # results.sort(key = lambda tup: tup[1])
    else:
        error = True
        raise Exception("There is an error on the Boomi atomsphere API response: " + processEnvironmentAttachmentResponseXML[0].text)


    return count, error, results, additional, queryToken

# QBApp/boomiAPIBuildRequests.py
"""
Created on Wed Jan 8 10:16:40 2020

# TODO: Implement the requests as objects (classes)
Functions with all the Boomi Atompshere API raw calls.

@author: jaimeHMol
"""

import requests
import logging

# TODO: REFACTOR: Implement as class or at least improve the concatenation of the
#                 body of the requests.

def buildRequestKeys (request):
    # SESSIONID = request.session.get("sessionId", "Session error")
    baseUrl = "https://api.boomi.com/api/rest/v1"
    accountId = request.session.get("accountId", "Session error")

    # TODO: Decrypt this:
    # request.session.get("key", "Session error, user not logged in.")
    headers = {"Content-Type": "text/xml", "Authorization": "Basic " +
               request.session.get("key", "Session error, user not logged in.")}

    return baseUrl, accountId, headers


def userLogin(request):
    """ Calling Boomi Athomsphere API to get the authentication of the user is accessing
    """
    OBJECT = "Account"
    OPERATION = "query"
    baseUrl, accountId, headers = buildRequestKeys(request)

    endpoint = baseUrl + "/" + accountId + "/" + OBJECT + "/" + OPERATION
    data = ''
    authenticated = False
    errorMessage = "Not authenticated"

    accountResponse = requests.post(endpoint, headers=headers, data=data)

    if (accountResponse.status_code == 200):
        authenticated = True
        errorMessage = ""
        logging.info(" ")
        logging.info(" ")
        logging.info("*** [Info]: " + "" + " succesfully authenticated by Boomi Atomsphere API.")
    else:
        authenticated = False
        errorMessage = accountResponse.text.split("<Data>")[1].split("</Data>")[0]
        logging.info(" ")
        logging.info(" ")
        logging.info("*** [Info]: " + "" + " haven't been authenticated by Boomi Atomsphere API.")

    return authenticated, errorMessage


def environmentList(request):
    """ Calling Boomi atomsphere API to retrieve all the envorinments information available
    """
    OBJECT = "Environment"
    OPERATION = "query"
    baseUrl, accountId, headers = buildRequestKeys(request)

    endpoint = baseUrl + "/" + accountId + "/" + OBJECT + "/" + OPERATION
    data = '''
    <QueryConfig xmlns="http://api.platform.boomi.com/">
        <QueryFilter>
            <expression operator="or" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="GroupingExpression">
                <nestedExpression operator="EQUALS" property="classification" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="SimpleExpression">
                    <argument>TEST</argument>
                </nestedExpression>
                <nestedExpression operator="EQUALS" property="classification" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="SimpleExpression">
                    <argument>PROD</argument>
                </nestedExpression>
            </expression>
        </QueryFilter>
    </QueryConfig>
    '''
    environmentsResponse = requests.post(endpoint, headers=headers, data=data).text

    logging.info(" ")
    logging.info(" ")
    logging.info("*** [Debug] environmentsResponse: " + environmentsResponse)
    return environmentsResponse


def atomList(request):
    """ Calling Boomi atomsphere API to retrive all the atoms information available
    """
    OBJECT = "Atom"
    OPERATION = "query"
    baseUrl, accountId, headers = buildRequestKeys(request)

    endpoint = baseUrl + "/" + accountId + "/" + OBJECT + "/" + OPERATION
    data = '''
    <QueryConfig xmlns="http://api.platform.boomi.com/">
        <QueryFilter>
            <expression operator="or" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="GroupingExpression">
                <nestedExpression operator="EQUALS" property="type" xsi:type="SimpleExpression">
                    <argument>MOLECULE</argument>
                </nestedExpression>
                <nestedExpression operator="EQUALS" property="type" xsi:type="SimpleExpression">
                    <argument>ATOM</argument>
                </nestedExpression>
                <nestedExpression operator="EQUALS" property="type" xsi:type="SimpleExpression">
                    <argument>CLOUD</argument>
                </nestedExpression>
            </expression>
        </QueryFilter>
    </QueryConfig>
    '''

    atomsResponse = requests.post(endpoint, headers=headers, data=data).text

    logging.info(" ")
    logging.info(" ")
    logging.info("*** [Debug] atomsResponse: " + atomsResponse)
    return atomsResponse

# TODO: Improve! big bottle neck. Change LIKE for EQUAL when not wildcard detected
def processList(request, processNameFilter):
    """ Calling Boomi atomsphere API to retrive the process information
        according the filter entered
    """
    # Calling Boomi atomsphere to load the envorinments available
    OBJECT = "Process"
    OPERATION = "query"
    baseUrl, accountId, headers = buildRequestKeys(request)
    WILDCARD = "%"

    comparisonOp = "LIKE" if WILDCARD in processNameFilter else "EQUALS"
    endpoint = baseUrl + "/" + accountId + "/" + OBJECT + "/" + OPERATION

    data = '''
    <QueryConfig xmlns="http://api.platform.boomi.com/">
        <QueryFilter>
            <expression xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" operator="''' + comparisonOp + '''" property="name" xsi:type="SimpleExpression">
                <argument>''' + processNameFilter + '''</argument>
            </expression>
        </QueryFilter>
    </QueryConfig>
    '''
    logging.info("*** [Debug] processesRequest.Data: " + data)

    processesResponse = requests.post(endpoint, headers=headers, data=data).text

    logging.info(" ")
    logging.info(" ")
    logging.info("*** [Debug] processesResponse: " + processesResponse)
    return processesResponse


def scheduleList(request, atomID, processID):
    """ Calling Boomi atomsphere API to retrive the schedules information
        according the filter entered
    """
    # Calling Boomi atomsphere to load the envorinments available
    OBJECT = "ProcessSchedules"
    OPERATION = "query"
    baseUrl, accountId, headers = buildRequestKeys(request)

    endpoint = baseUrl + "/" + accountId + "/" + OBJECT + "/" + OPERATION
    data = '''
    <QueryConfig xmlns="http://api.platform.boomi.com/">
        <QueryFilter>
            <expression operator="and" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="GroupingExpression">
                <nestedExpression operator="EQUALS" property="atomId" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="SimpleExpression">
                    <argument>''' + atomID + '''</argument>
                </nestedExpression>
                <nestedExpression operator="EQUALS" property="processId" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="SimpleExpression">
                    <argument>''' + processID + '''</argument>
                </nestedExpression>
            </expression>
      </QueryFilter>
    </QueryConfig>
    '''
    schedulesResponse = requests.post(endpoint, headers=headers, data=data).text

    logging.info(" ")
    logging.info(" ")
    logging.info("*** [Debug] schedulesResponse: " + schedulesResponse)
    return schedulesResponse


def scheduleStatusGet(request, scheduleID):
    """ Calling Boomi atomsphere API to get the status (enable or disable) of an existing schedule.
    """
    # Calling Boomi atomsphere to load the envorinments available
    OBJECT = "ProcessScheduleStatus"
    ID = scheduleID
    baseUrl, accountId, headers = buildRequestKeys(request)

    endpoint = baseUrl + "/" + accountId + "/" + OBJECT + "/" + ID
    data = ''

    scheduleStatusGetResponse = requests.get(endpoint, headers=headers, data=data).text

    logging.info(" ")
    logging.info(" ")
    logging.info("*** [Debug] scheduleStatusGetResponse: " + scheduleStatusGetResponse)
    return scheduleStatusGetResponse


def scheduleStatusUpdate(request, scheduleID, atomID, processID, enable):
    """ Calling Boomi atomsphere API to update the status (enable or disable) of an existing schedule.
    """
    # Calling Boomi atomsphere to load the envorinments available
    OBJECT = "ProcessScheduleStatus"
    OPERATION = "update"
    ID = scheduleID
    baseUrl, accountId, headers = buildRequestKeys(request)
    if enable:
        newStatus = "true"
    else:
        newStatus = "false"

    endpoint = baseUrl + "/" + accountId + "/" + OBJECT + "/" + ID + "/" + OPERATION

    data = '''
    <bns:ProcessScheduleStatus enabled="''' + newStatus + '''"  id="''' + scheduleID + '''"     atomId="''' + atomID + '''" processId="''' + processID + '''" xmlns:bns="http://api.platform.boomi.com/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
    '''

    scheduleStatusUpdateResponse = requests.post(endpoint, headers=headers, data=data).text

    logging.info(" ")
    logging.info(" ")
    logging.info("*** [Debug] scheduleStatusUpdateResponse: " + scheduleStatusUpdateResponse)
    return scheduleStatusUpdateResponse


def queryPagination(request, objectType, queryToken):
    """ Calling Boomi atomsphere API to retrive the next page of a query
        with more than 100 results
    """
    # Calling Boomi atomsphere to load the envorinments available
    OBJECT = objectType
    OPERATION = "queryMore"
    baseUrl, accountId, headers = buildRequestKeys(request)

    endpoint = baseUrl + "/" + accountId + "/" + OBJECT + "/" + OPERATION
    data = queryToken
    queryPaginationResponse = requests.post(endpoint, headers=headers, data=data).text

    logging.info(" ")
    logging.info(" ")
    logging.info("*** [Debug] queryPaginationResponse: " + queryPaginationResponse)
    return queryPaginationResponse

def deploymentList(request, processID, environmentId):
    """ Calling Boomi atomsphere API to retrive the deployment information
        according the filter entered
    """
    # Calling Boomi atomsphere to load the envorinments available
    OBJECT = "Deployment"
    OPERATION = "query"
    baseUrl, accountId, headers = buildRequestKeys(request)

    endpoint = baseUrl + "/" + accountId + "/" + OBJECT + "/" + OPERATION
    data = '''
    <QueryConfig xmlns="http://api.platform.boomi.com/">
    	<QueryFilter>
    		<expression operator="and" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="GroupingExpression">
    			<nestedExpression operator="EQUALS" property="processId" xsi:type="SimpleExpression">
    		        <argument>''' + processID + '''</argument>
    		    </nestedExpression>
    			<nestedExpression operator="EQUALS" property="environmentId" xsi:type="SimpleExpression">
    		        <argument>''' + environmentId + '''</argument>
    		    </nestedExpression>
    		    <nestedExpression operator="EQUALS" property="current" xsi:type="SimpleExpression">
    		        <argument>true</argument>
    		    </nestedExpression>
    		</expression>
    	</QueryFilter>
    </QueryConfig>
    '''
    deploymentResponse = requests.post(endpoint, headers=headers, data=data).text

    logging.info(" ")
    logging.info(" ")
    logging.info("*** [Debug] deploymentResponse: " + deploymentResponse)
    return deploymentResponse

def environmentAtomList(request):
    """ Calling Boomi atomsphere API to retrive all the environment-atoms information available
    """
    OBJECT = "EnvironmentAtomAttachment"
    OPERATION = "query"
    baseUrl, accountId, headers = buildRequestKeys(request)

    endpoint = baseUrl + "/" + accountId + "/" + OBJECT + "/" + OPERATION
    data = ""

    environmentAtomResponse = requests.post(endpoint, headers=headers, data=data).text

    logging.info(" ")
    logging.info(" ")
    logging.info("*** [Debug] EnvironmentAtomsResponse: " + environmentAtomResponse)
    return environmentAtomResponse

def ProcessEnvironmentAttachment(request, processID, environmentId):
    """ Calling Boomi atomsphere API to retrive the Process-Environment attachment information according the filter entered
    """
    # Calling Boomi atomsphere to load the envorinments available
    OBJECT = "ProcessEnvironmentAttachment"
    OPERATION = "query"
    baseUrl, accountId, headers = buildRequestKeys(request)

    endpoint = baseUrl + "/" + accountId + "/" + OBJECT + "/" + OPERATION
    data = '''
    <QueryConfig xmlns="http://api.platform.boomi.com/">
      <QueryFilter>
        <expression operator="and" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="GroupingExpression">
    	    <nestedExpression operator="EQUALS" property="processId" xsi:type="SimpleExpression">
    	        <argument>''' + processID + '''</argument>
    	    </nestedExpression>
    	    <nestedExpression operator="EQUALS" property="environmentId" xsi:type="SimpleExpression">
    	        <argument>''' + environmentId + '''</argument>
    	    </nestedExpression>
    	</expression>
      </QueryFilter>
    </QueryConfig>
    '''
    processEnvironmentAttachmentResponse = requests.post(endpoint, headers=headers, data=data).text

    logging.info(" ")
    logging.info(" ")
    logging.info("*** [Debug] processEnvironmentAttachmentResponse: " + processEnvironmentAttachmentResponse)
    return processEnvironmentAttachmentResponse

def deleteDeployment(request, id):
    """ Calling Boomi atomsphere API to delete a deployment (detach process from environment)
    """
    OBJECT = "ProcessEnvironmentAttachment"
    OPERATION = "query"
    baseUrl, accountId, headers = buildRequestKeys(request)

    endpoint = baseUrl + "/" + accountId + "/" + OBJECT + "/" + id
    data = ""

    deleteDeploymentResponse = requests.delete(endpoint, headers=headers, data=data).text

    logging.info(" ")
    logging.info(" ")
    logging.info("*** [Debug] deleteDeploymentResponse: " + deleteDeploymentResponse)
    return deleteDeploymentResponse



def executionRecordList(request, processID,atomID, dateIni, dateEnd):
    baseUrl, accountId, headers = buildRequestKeys(request)
    pass

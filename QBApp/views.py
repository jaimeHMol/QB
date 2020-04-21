# QBApp/views.py
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse
from django.conf import settings

from .tables import qresultsTable
# Test for result table
from .models import Person
from .tables import PersonTable

from . import boomiAPIBuildRequests
from . import boomiAPIParseResults
from . import oktaAuthentication
from . import forms
from .generic import qbInterceptor

from django_tables2 import SingleTableView
from django_tables2 import RequestConfig
import time
import random
import base64
import csv
import os
from datetime import datetime
import logging

# TODO: Issue the data store in the session is being shared between different
#       searchs done in tabs of the same browser


# URLs - Template pages classes ------------------------------------------------
class HomeView(TemplateView):

    @qbInterceptor
    def get(self, request, **kwargs):

        # Initial values load --------------------------------------------------
        atomsLoV = request.session.get("atomsLoV", "notFound")
        environmentAtomList = request.session.get("environmentAtomList", "notFound")

        if atomsLoV == "notFound" or environmentAtomList == "notFound":
            # Retrieving Boomi atoms available
            atomsResponse = boomiAPIBuildRequests.atomList(request)
            atomsCount, atomsError, atomsLoV, atomsAdditional, atomsQueryToken = boomiAPIParseResults.atomList(atomsResponse)

            if atomsError == True or int(atomsCount) <= 0:
                # atomsLoV.append(("notFound","Error loading atoms"))
                raise Exception("There isn't any atom available on this Boomi account.")
            request.session["atomsLoV"] = atomsLoV

            # Retrieving relation between Boomi atoms and environments
            environmentAtomsResponse = boomiAPIBuildRequests.environmentAtomList(request)
            environmentAtomCount, environmentAtomError, environmentAtomList, environmentAtomAdditional, environmentAtomQueryToken = boomiAPIParseResults.environmentAtomList(environmentAtomsResponse)

            if environmentAtomError == True or int(environmentAtomCount) <= 0:
                raise Exception("There isn't any environment attached to atoms.")
            request.session["environmentAtomList"] = environmentAtomList
        # ----------------------------------------------------------------------

        form = forms.SearchForm(atomsLoV)
        # HINT: just commented below line, TEST!!!!
        # request.session["resultTableLoaded"] = False
        userFullName = request.session.get("userFullName", "User not found")

        return render(request, "search.html", {"form": form, "userFullName": userFullName})


# Q results table
# TODO: refactor using Functions
class QResults2View(SingleTableView):

    @qbInterceptor
    def get(self, request, **kwargs):
        resultsCached = False
        # Initial values load --------------------------------------------------
        alreadyLoaded = request.session.get("resultTableLoaded", False)
        atomsLoV = request.session.get("atomsLoV", [("1", "Error")])
        environmentAtomList = request.session.get("environmentAtomList", "notFound")
        userFullName = request.session.get("userFullName", "User not found")

        form = forms.SearchForm(atomsLoV, request.GET)

        if form.is_valid() and form.cleaned_data["environment"] != "notFound":
            atomIdFilter = form.cleaned_data["environment"]
            atomNameFilter = dict(form.fields["environment"].choices)[atomIdFilter]
            processesFilter = form.cleaned_data["processesToFind"]

            atomIdFilterCached = request.session.get("atomIdFilter", "notFound")
            processesFilterCached = request.session.get("processesFilter", "notFound")

            resultsCached = atomIdFilter.upper() == atomIdFilterCached.upper()\
                            and processesFilter.upper() == processesFilterCached.upper()\
                            and alreadyLoaded

        else:
            request.session["errorTrace"] = "Validation error on the search filters form."
            request.session["errorCode"] = 1
            raise Exception("Validation errorn on search form.")
            # return redirect("/error/")
            # return render(request, "error.html")
        # ----------------------------------------------------------------------

        if not resultsCached:
            request.session["resultTableLoaded"] = False
            request.session["resultTableCached"] = None
            resultsCount = 0
            resultsDeployments = 0
            data2 = []

            # Calling Boomi Atomsphere API to retrieve process id matching with the
            # search creteria
            processesResponse = boomiAPIBuildRequests.processList(request, processesFilter)
            processesCount, processesError, processesResults, processesAdditional, processesQueryToken = boomiAPIParseResults.processList(request, processesResponse)
            # logging.info("*** Processes queryToken: " + processesQueryToken)

            if int(processesCount) > 0:

                for process in processesResults:
                    #Initialization of process parameters
                    atomId = atomIdFilter
                    atomName = atomNameFilter
                    environmentId = environmentAtomList.get(atomId)
                    processId = process[0]
                    processName = process[1]
                    cadenceInfo = "---"
                    lastExecInfo = "---"
                    enableInfo = "No"
                    durAvgInfo = "---"
                    deployedInfo = "No"
                    scheduleId = ""

                    procEnvAttachResponse = boomiAPIBuildRequests.ProcessEnvironmentAttachment(request, processId, environmentId)

                    procEnvAttachCount, procEnvAttachError, procEnvAttachResults, procEnvAttachAdditional, procEnvAttachQueryToken = boomiAPIParseResults.ProcessEnvironmentAttachment(procEnvAttachResponse)

                    if int(procEnvAttachCount) == 1:
                        resultsDeployments = resultsDeployments + 1
                        deployedInfo = "Yes"

                        # Calling schedule query of the Boomi Atompshere API
                        schedulesResponse = boomiAPIBuildRequests.scheduleList(request, atomId, processId)
                        schedulesCount, schedulesError, schedulesResults, schedulesAdditional, schedulesQueryToken = boomiAPIParseResults.scheduleList(schedulesResponse)
                        logging.info("schedulesResults: "+str(schedulesResults))

                        if int(schedulesCount) > 0 and schedulesResults[0][0] == atomId:
                            resultsCount = resultsCount + 1
                            # Calling schedule status query of the Boomi Atompshere API
                            scheduleStatusResponse = boomiAPIBuildRequests.scheduleStatusGet(request, schedulesResults[0][3])
                            scheduleStatusError, scheduleStatusResult = boomiAPIParseResults.scheduleStatusGet(scheduleStatusResponse)

                            if schedulesResults[0][2] != "NA":
                                cadenceInfo = schedulesResults[0][2]
                                enableInfo = scheduleStatusResult
                                scheduleId = schedulesResults[0][3]

                            else:
                                enableInfo = scheduleStatusResult
                        else:
                            enableInfo = "No"
                    else:
                        if int(procEnvAttachCount) > 1 :
                            logging.warning("*** Shouldn't be more than one enviroment attached to process with the current filters")

                        deployedInfo = "No"
                        atomName = "---"
                        lastExecInfo = "---"
                        durAvgInfo = "---"

                    data2.append({"processName": processName, "atomName": atomName,"cadence": cadenceInfo, "enable": enableInfo, "lastExec": lastExecInfo, "durAvg":durAvgInfo, "deployed": deployedInfo, "atomID": atomId, "processId":processId, "scheduleId": scheduleId })



                outTable = qresultsTable(data2)
                # Needed to be able to use the sort and pagination of the table
                RequestConfig(request).configure(outTable)

                # TODO: this flag can be avoided.
                request.session["resultTableLoaded"] = True
                request.session["resultTableCached"] = data2
                request.session["processesCount"] = processesCount
                request.session["resultsCount"] = resultsCount
                request.session["resultsDeployments"] = resultsDeployments
                # TODO Add the warningCount
                request.session["atomIdFilter"] = atomIdFilter
                request.session["processesFilter"] = processesFilter


                return render(request, "qresults.html", {"table":outTable, "processesCount":processesCount, "resultsCount":resultsCount, "resultsDeployments": resultsDeployments, "userFullName": userFullName})
            else:
                return redirect("/noresults/")
                # return render(request, "noresults.html")

        else:
            # Search results already cached
            dataCached = request.session.get("resultTableCached", False)

            resultTableCached = qresultsTable(dataCached)

            processesCount = request.session.get("processesCount", False)
            resultsCount = request.session.get("resultsCount", False)
            resultsDeployments = request.session.get("resultsDeployments", False)
            # TODO Add the warningCount
            # Needed to be able to use the sort and pagination of the table
            RequestConfig(request).configure(resultTableCached)

            return render(request, "qresults.html", {"table":resultTableCached, "processesCount":processesCount, "resultsCount":resultsCount, "resultsDeployments": resultsDeployments, "userFullName": userFullName})


class LoginView(TemplateView):

    @qbInterceptor
    def get(self, request, **kwargs):

        redirected = request.session.get("redirected", False)
        errorCode = request.session.get("errorCode", 0)
        errorMessage = request.session.get("errorTrace", '')
        accountId = request.session.get("accountId", '')
        email = request.session.get("email", '')
        # template_name = "index.html"

        request.session["errorCode"] = 0
        request.session["errorTrace"] = ''
        request.session["email"] = ''
        request.session["accountId"] = ''
        request.session["redirected"] = False

        redirected = "block" if redirected else "none"

        formLogin = forms.LoginForm(initial={"accountId": accountId,
                                             "email":email,
                                             "accountId":""})

        showError = "block" if errorCode == 1 else "none"

        return render(request, "index.html", {"formLogin": formLogin, "showError": showError, "errorMessage": errorMessage, "redirected": redirected})


class ErrorView(TemplateView):

    @qbInterceptor
    def get(self, request, **kwargs):
        errorTrace = request.session.get("errorTrace", "Unknown")
        request.session["errorCode"] = 0
        request.session["errorTrace"] = ''

        return render(request, "error.html", {"errorTrace": errorTrace})


class AboutView(TemplateView):
    # template_name = "about.html"
    @qbInterceptor
    def get(self, request, **kwargs):
        return render(request, "about.html")


class NoResultsView(TemplateView):
    # template_name = "noresults.html"
    @qbInterceptor
    def get(self, request, **kwargs):
        return render(request, "noresults.html")
# ------------------------------------------------------------------------------


# URLs - Caller classes --------------------------------------------------------
# TODO: Handle case when there is nothing to offboard!
class OffboardCall(TemplateView):

    @qbInterceptor
    def get(self, request, **kwargs):

        dataCached = request.session.get("resultTableCached", False)
        request.session["resultTableLoaded"] = False
        #dataCached: [{'processName': 'Z_R9_BASF_SVTranspro_ce_V1', 'atomName': 'Stage-Molecule', 'cadence': '0-59/30', 'enable': 'Yes', 'lastExec': '---', 'durAvg': '---', 'deployed': 'Yes'}]
        logging.info("############################")
        logging.info("dataCached: "+str(dataCached))
        logging.info("############################")
        environmentAtomList = request.session.get("environmentAtomList", [("1", "Error")])

        for dataInfo in dataCached:

            # if has schedule => deschedule Process (schedule = Yes)
            logging.info(str(dataInfo))
            if dataInfo["enable"] == 'Yes':
                logging.info("***** Descheduling process "+dataInfo["processName"]+"...")

                # scheduleStatusUpdate(request, scheduleID, atomID, processID, enable)
                scheduleOffResponse = boomiAPIBuildRequests.scheduleStatusUpdate(request, dataInfo["scheduleId"], dataInfo["atomID"], dataInfo["processId"], False)
            # if it was deplyoed => deattach process (deployed = Yes)
            if dataInfo["deployed"] == 'Yes':
                logging.info("***** undeploying process: "+dataInfo["processName"]+"...")
                environmentId = environmentAtomList.get(dataInfo["atomID"])

                procEnvAttachResponse = boomiAPIBuildRequests.ProcessEnvironmentAttachment(request, dataInfo["processId"], environmentId)

                procEnvAttachCount, procEnvAttachError, procEnvAttachResults, procEnvAttachAdditional, procEnvAttachQueryToken = boomiAPIParseResults.ProcessEnvironmentAttachment(procEnvAttachResponse)

                undeployProcess = boomiAPIBuildRequests.deleteDeployment(request, procEnvAttachResults)

                logging.info("undeployProcess: "+str(undeployProcess))

        # TODO: Review this render. Should be redirect
        return render(request, "actionDone.html", {"actionStatus": "Offboard sucessfully"})


class LoginUserCall(ListView):

    @qbInterceptor
    def post(self, request, **kwargs):

        formLogin = forms.LoginForm(request.POST)
        validForm = formLogin.is_valid()
        user = formLogin.cleaned_data["email"]
        userFullName = user.split('@')[0].replace("BOOMI_TOKEN.","")
        password = formLogin.cleaned_data["password"]
        accountId = formLogin.cleaned_data["accountId"]

        request.session["email"] = user
        request.session["accountId"] = accountId

        key = user + ":" + password
        request.session["key"] = base64.b64encode(key.encode("utf-8")).decode("utf-8")
        # TODO: Encrypt this:
        # request.session["key"] = encrypt (SESSIONID, base64.b64encode(key.encode("utf-8")))

        userBoomiAuthenticated, errorMessage = boomiAPIBuildRequests.userLogin(request)
        if userBoomiAuthenticated:
            request.session["userFullName"] = userFullName
            # Generates session id
            sessionId = random.uniform(0,7777777)
            request.session["sessionId"] = sessionId
            page = "/search/"
        else:
            request.session["errorCode"] = 1
            request.session["errorTrace"] = errorMessage
            page = "/"
            # return render(request, '../', {'formLogin': formLogin})

        return redirect(page)


class LogoutCall(TemplateView):
    def get(self, request, **kwargs):
        request.session.flush()
        request.session["redirected"] = True
        return redirect("/")


class ExportToCSVCall(TemplateView):

    @qbInterceptor
    def get(self, request, **kwargs):
        data = request.session.get("resultTableCached", [("1", "Error")])
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d_%H%M%S")
        #output filename
        configuration = 'attachment; filename=QBResult_'+dt_string+'.csv'
        # deleting value of atomID, process ID and Schedule Id because from each dictionary of the list.
        # those values are intern
        for dict in data:
            del dict['atomID']
            del dict['processId']
            del dict['scheduleId']

        filename = '../data.txt'

        with open(filename, "w") as infile:
            writer = csv.DictWriter(infile, fieldnames=data[0].keys())
            writer.writeheader()
            for row in data:
                writer.writerow(row)

        with open(filename, 'rb') as infile:
            response = HttpResponse(infile, content_type='text/csv')
            response['Content-Disposition'] = configuration

        # Removing temporal file
        if os.path.exists(filename):
            os.remove(filename)

        return response


class RedirectCall(TemplateView):
    def get(self, request, **kwargs):
        request.session["redirected"] = True
        return redirect("/")
# ------------------------------------------------------------------------------



# To check and delete ----------------------------------------------------------
class QResultsView(TemplateView):
    template_name = "qresults.html"


class ScheduleQuery(ListView):
    model = Person
    template_name = 'people.html'


class PersonListView(SingleTableView):
    model = Person
    table_class = PersonTable
    template_name = 'people.html'

# QBApp/generic.py
"""
Created on Wed Apr 7 20:11:32 2020

Generic functions, wrappers and decorators.

@author: jaimeHMol
"""

from django.shortcuts import render, redirect
import sys
import traceback
import logging
from functools import wraps


def qbInterceptor(func):

    @wraps(func)
    def _wrapper(classCaller, request, **kwargs):
        try:

            # Session validation
            sessionId = request.session.get("sessionId", 0)
            url = request.path
            classCallerName = classCaller.__class__.__name__
            logging.warning(">>> QB Interceptor begins. Class caller: " +
                            classCallerName + ". URL: " + url +
                            ". SessionId: " + str(sessionId))

            if sessionId == 0 and url not in ("/", "/loginuser/", "/error/", "/about/"):
                logging.warning(">>> Redirecting...")
                value = redirect("/redirecting/")

            # Executing the function caller
            else:
                value = func(classCaller, request, **kwargs)

                logging.warning(">>> QB Interceptor end steps...")

            return value

        # Handle the return
        except Exception as exc:
            excType, excValue, excTraceback = sys.exc_info()

            logging.error('>>> There was an error....')

            errorTrace = traceback.format_exception(excType, excValue,
                                                    excTraceback)
            errorTrace = "".join(errorTrace)
            logging.error(errorTrace)

            request.session["errorTrace"] = errorTrace
            request.session["errorCode"] = 1

            return redirect("/error/")

    return _wrapper

# QBApp/urls.py
from django.urls import path
from django.urls import re_path
from QBApp import views

from django.views.generic.base import RedirectView

urlpatterns = [

    # URLs - Template pages classes --------------------------------------------
    path("", views.LoginView.as_view()),
    path("search/", views.HomeView.as_view()),
    path("search/qresults2/", views.QResults2View.as_view()),

    path("noresults/", views.NoResultsView.as_view()),
    path("error/", views.ErrorView.as_view()),
    re_path(r'^.*about/', views.AboutView.as_view()),
    # --------------------------------------------------------------------------


    # URLs - Caller classes ----------------------------------------------------
    path("search/qresults2/offboard/", views.OffboardCall.as_view()),
    path("search/qresults2/exportocsv/", views.ExportToCSVCall.as_view()),
    path("loginuser/", views.LoginUserCall.as_view()),
    re_path(r'^.*logout/', views.LogoutCall.as_view()),
    # --------------------------------------------------------------------------


    # Statics and other calls --------------------------------------------------
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico")),

    # Whatever other url redirects to login page.
    re_path(r'^.*$', views.RedirectCall.as_view())
    # --------------------------------------------------------------------------
]

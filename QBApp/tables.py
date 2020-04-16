# QBApp/tables.py
import django_tables2 as tables
from .models import Person
# from .nameTable import NameTable

import logging


class PersonTable(tables.Table):
    class Meta:
        model = Person

        template_name = "django_tables2/bootstrap.html"
        fields = ("Full name", )


class qresultsTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-hover table-sm"}

        # HINT: Define the template used to build the html structure of the
        #       table.
        # template_name = "django_tables2/bootstrap.html" # Generic django_tables2
        template_name = "customtable.html" # Custom template for the table

    processName = tables.Column(verbose_name="Process Name",order_by="processName")
    deployed = tables.Column(verbose_name="Deployed")
    atomName = tables.Column(verbose_name="Atom Name")
    cadence = tables.Column(verbose_name="ScheduleConfig")
    enable = tables.Column(verbose_name="ScheduleEnable")
    lastExec = tables.Column(verbose_name="Last Execution")
    durAvg = tables.Column(verbose_name="Average Duration")

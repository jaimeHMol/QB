# QB
Web application to execute repetitive and analytical actions over the Boomi's metadata, using the Boomi Atomsphere API.


# What is?
A productivity tool for every Boomi developer who wants to do repetitive and booring activities in a automated way. In addition for thouse 


# Why?
To resolve quickly and automatically questions like:
* What was deployed since Jan 2020?
* Which are the processes built, deployed and/or scheduled for a customer or data provider?
* Why is a process scheduled to run each minute if usually it takes 10 minutes to finish?
* Who is deploying more processes?
* Why do I have to do so many repetitive tasks when I have to offboard a customer. 
* Why does the molecule run so slow?
* Why don't the schedules run on time? 


# What can you currently do?
* Retrieve the atoms and environments available.
* Retrieve the process list from the Build repository, using filters.
* Retrieve the schedule information of each process, using filters.
* Deactivate schedules for the processes found. 
* Detach processes from the selected molecule.


# Additional specs
* Sharp and responsive design.
* Validated forms, paginated and ordered tables.
* Easy to deploy and maintain. It is built using Model View Template methodology.
* Doesn’t have any additional cost, as Dell state [here](https://community.boomi.com/s/article/understandingconnectionusageandlicensing), there isn’t any charge for use their API.


# Technological stack
* Dell Boomi
* Python
* Django
* SQLite (Coming soon)
* Bootstrap


# Requirements
Python 3.6:
* Django==2.1.3
* django-tables2==2.2.1
* django-widget-tweaks==1.4.3
* certifi==2019.11.28
* chardet==3.0.4
* idna==2.8
* pytz==2018.7
* requests==2.22.0
* urllib3==1.25.7


# How to run it locally
You should install and create Python virtual environment
```shell
virtualenv venv
```
Activate the virtual environment
```shell
source venv/bin/activate
```

Then install the requirements file (included on the root folder) executing:
```shell
pip3 install -r requirements.txt
```

Finally, run the Django server
```shell
python3 manage.py runserver <ipaddress>:<port>
```


# Contributors
* Christian Higa 

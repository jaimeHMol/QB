from django.db import models

from django.contrib.auth import get_user_model

# TODO: Implement here the data model to support and persist all the actions done through the QB app.

# Create your models here.



# Test for result table
# import django_tables2 as tables
#
# data = [
#     {"name": "Kepler"},
#     {"name": "Galileo"},
# ]
#
# class NameTable(tables.Table):
#     name = tables.Column()
#
# table = NameTable(data)

# Test for result table
class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name="full name")
    # first_name = models.CharField(max_length=200)
    # last_name = models.CharField(max_length=200)
    # user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    # birth_date = models.DateField()

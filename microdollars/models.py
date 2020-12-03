from django.db import models

from django.contrib.auth.models import User


class OrganizationModel(models.Model):
    organization_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="myimages",
                              default="/static/microdollars/missing.png")
    about_me = models.TextField(
        max_length=1000, default='INFO ON THIS ORGANIZATION')

    def __str__(self):
        return self.organization_name


# {% comment %}
# /***************************************************************************************
# *  REFERENCES
# *  Title: How to Implement Dependent/Chained Dropdown List with Django
# *  Author: Vitor Freitas
# *  Date: 1/29/18
# *  Code version: N/A
# *  URL: https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
# *  Software License: Part of a tutorial
# *
# ***************************************************************************************/
# {% endcomment %}


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, related_name='usernames', default=None)
    donateto = models.ForeignKey(
        OrganizationModel, on_delete=models.SET_NULL, null=True, verbose_name="Organization")
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    comment = models.CharField(max_length=350, blank=True)
    models.CharField(max_length=350, blank=True)

    def convertToTuple(self, info):
        obj = info.objects.all()


class Search(models.Model):
    user_search = models.CharField(max_length=350, default="")

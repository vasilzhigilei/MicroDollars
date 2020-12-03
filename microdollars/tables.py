import django_tables2 as tables
from .models import Donation


class DonationTable(tables.Table):
    class Meta:
        model = Donation
        attrs = {"class": "table"}
        exclude = ("user", "id")

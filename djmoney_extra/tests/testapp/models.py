from django.db import models
from djmoney.models.fields import MoneyField

class MoneyModel(models.Model):
    price = MoneyField(max_digits=6, decimal_places=5)

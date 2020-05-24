from decimal import Decimal

from django.test import TestCase

from djmoney.money import Money
from djmoney_extra import graphene


class MoneyFloatTest(TestCase):
    def setUp(self):
        self.func = graphene.MoneyFloat.coerce_float

    def test_money(self):
        value = Money(10, 'EUR')
        output = self.func(value)
        self.assertEqual(10, output)

    def test_float(self):
        output = self.func(10.00)
        self.assertEqual(10, output)

    def test_int(self):
        output = self.func(10)
        self.assertEqual(10, output)

    def test_decimal(self):
        output = self.func(Decimal(10))
        self.assertEqual(10, output)

    def test_str(self):
        output = self.func('10')
        self.assertEqual(10, output)


class MoneyStringTest(TestCase):
    def setUp(self):
        self.func = graphene.MoneyString.coerce_string

    def test_money(self):
        value = Money(10, 'EUR')
        output = self.func(value)
        self.assertEqual('10.00 €', output)

    def test_float(self):
        output = self.func(10.00)
        self.assertEqual('10.0', output)

    def test_int(self):
        output = self.func(10)
        self.assertEqual('10', output)

    def test_decimal(self):
        output = self.func(Decimal(10))
        self.assertEqual('10', output)

    def test_str(self):
        output = self.func('10')
        self.assertEqual('10', output)

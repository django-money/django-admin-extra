from decimal import Decimal

from django.test import TestCase

from djmoney.money import Money
from djmoney_extra import tables

from testapp import models


class MoneyColumnTest(TestCase):
    def test_money_field(self):
        # Setup
        record = models.MoneyModel(price=Money(10, 'EUR'))
        self.column = tables.MoneyColumn()
        # Test
        text = self.column.render(record.price, record)
        self.assertIsInstance(text, str)
        self.assertEqual('10.00000 €', text)

    def test_float_annotation(self):
        # Setup
        record = models.MoneyModel(price=Money(10, 'EUR'))
        record.as_float = 10.
        self.column = tables.MoneyColumn(
            currency_field='price_currency',
            decimals=5,
        )
        # Test
        text = self.column.render(record.as_float, record)
        self.assertIsInstance(text, str)
        self.assertEqual('10.00000 €', text)

    def test_str_annotation(self):
        # Setup
        record = models.MoneyModel(price=Money(10, 'EUR'))
        record.as_str = "10"
        self.column = tables.MoneyColumn(
            currency_field='price_currency',
            decimals=5,
        )
        # Test
        text = self.column.render(record.as_str, record)
        self.assertIsInstance(text, str)
        self.assertEqual('10.00000 €', text)

    def test_int_annotation(self):
        # Setup
        record = models.MoneyModel(price=Money(10, 'EUR'))
        record.as_int = 10
        self.column = tables.MoneyColumn(
            currency_field='price_currency',
            decimals=5,
        )
        # Test
        text = self.column.render(record.as_int, record)
        self.assertIsInstance(text, str)
        self.assertEqual('10.00000 €', text)

    def test_decimal_annotation(self):
        # Setup
        record = models.MoneyModel(price=Money(10, 'EUR'))
        record.as_decimal = Decimal('10')
        self.column = tables.MoneyColumn(
            currency_field='price_currency',
            decimals=5,
        )
        # Test
        text = self.column.render(record.as_decimal, record)
        self.assertIsInstance(text, str)
        self.assertEqual('10.00000 €', text)

    def test_force_decimal_places(self):
        # Setup
        record = models.MoneyModel(price=Money(10, 'EUR'))
        column = tables.MoneyColumn(
            decimals=1,
        )
        # Test
        text = column.render(record.price, record)
        self.assertIsInstance(text, str)
        self.assertEqual('10.0 €', text)

    def test_force_decimal_places_annotation(self):
        # Setup
        record = models.MoneyModel(price=Money(10, 'EUR'))
        record.as_int = 10
        column = tables.MoneyColumn(
            decimals=1,
            currency_field='price_currency',
        )
        # Test
        text = column.render(record.as_int, record)
        self.assertIsInstance(text, str)
        self.assertEqual('10.0 €', text)

    def test_force_locale(self):
        # Setup
        record = models.MoneyModel(price=Money(10, 'EUR'))
        column = tables.MoneyColumn(
            locale='fr_FR',
        )
        # Test
        text = column.render(record.price, record)
        self.assertIsInstance(text, str)
        self.assertEqual('10,00000 €', text)

    def test_force_locale_annotation(self):
        # Setup
        record = models.MoneyModel(price=Money(10, 'EUR'))
        record.as_int = 10
        column = tables.MoneyColumn(
            locale='fr_FR',
            currency_field='price_currency',
        )
        # Test
        text = column.render(record.as_int, record)
        self.assertIsInstance(text, str)
        self.assertEqual('10,00 €', text)

    def test_money_field_use_symbol(self):
        # Setup
        record = models.MoneyModel(price=Money(10, 'EUR'))
        self.column = tables.MoneyColumn(
            include_symbol=True,
        )
        # Test
        text = self.column.render(record.price, record)
        self.assertIsInstance(text, str)
        self.assertEqual('10.00000 €', text)

    def test_money_field_not_use_symbol(self):
        # Setup
        record = models.MoneyModel(price=Money(10, 'EUR'))
        self.column = tables.MoneyColumn(
            include_symbol=False,
        )
        # Test
        text = self.column.render(record.price, record)
        self.assertIsInstance(text, str)
        self.assertEqual('10.00000', text)

    def test_target_rate_and_currency(self):
        # Setup
        record = models.MoneyModel(price=Money(10, 'EUR'))
        self.column = tables.MoneyColumn(
            target_rate=2,
            target_currency='USD',
        )
        # Test
        text = self.column.render(record.price, record)
        self.assertIsInstance(text, str)
        self.assertEqual('$20.00000', text)

    def test_target_rate_and_not_currency(self):
        # Setup
        record = models.MoneyModel(price=Money(10, 'EUR'))
        self.column = tables.MoneyColumn(
            target_rate=2,
        )
        # Test
        text = self.column.render(record.price, record)
        self.assertIsInstance(text, str)
        self.assertEqual('10.00000 €', text)

    def test_target_currency_and_not_rate(self):
        # Setup
        record = models.MoneyModel(price=Money(10, 'EUR'))
        self.column = tables.MoneyColumn(
            target_currency='USD',
        )
        # Test
        text = self.column.render(record.price, record)
        self.assertIsInstance(text, str)
        self.assertEqual('10.00000 €', text)

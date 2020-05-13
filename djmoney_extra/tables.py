from decimal import Decimal
from django_tables2 import columns
from djmoney.money import Money, format_money, get_current_locale


class MoneyColumn(columns.Column):
    money_class = Money
    currency_field = None
    target_rate = None
    target_currency = None

    def __init__(self, decimals=None, verbose=False, money_class=None,
                 format_kwargs=None, currency_field=None, locale=None,
                 include_symbol=True, target_rate=None, target_currency=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.decimals = decimals
        self.verbose = verbose
        self.money_class = money_class or self.money_class
        self.format_kwargs = format_kwargs or {}
        self.currency_field = currency_field or self.currency_field
        self.locale = locale or get_current_locale()
        self.include_symbol = include_symbol
        self.target_rate = target_rate or self.target_rate
        self.target_currency = target_currency or self.target_currency

    def _get_decimals(self, value, record):
        return self.decimals

    def _get_currency(self, value, record):
        if self.currency_field:
            return getattr(record, self.currency_field)

    def _get_target_rate(self, value, record):
        if self.target_rate:
            return self.target_rate

    def _get_target_currency(self, value, record):
        if self.target_currency:
            return self.target_currency

    def render(self, value, record, **kwargs):

        decimals = self._get_decimals(value, record)

        if not isinstance(value, Money):
            value = Decimal(value)
            value = Money(
                value, self._get_currency(value, record),
                decimal_places=decimals,
            )

        if decimals is None:
            decimals = value.decimal_places

        target_rate = self._get_target_rate(value, record)
        target_currrency = self._get_target_currency(value, record)
        if target_rate and target_currrency:
            value = Money(
                value.amount * target_rate,
                target_currrency,
                decimal_places=decimals,
            )

        text = format_money(
            money=value,
            include_symbol=self.include_symbol,
            decimal_places=decimals,
            locale=self.locale,
        )
        return text

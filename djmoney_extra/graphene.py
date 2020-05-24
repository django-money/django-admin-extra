from decimal import Decimal
import graphene
from djmoney.money import Money, format_money, get_current_locale


class MoneyFloat(graphene.Float):
    @staticmethod
    def coerce_float(value):
        # Ensure we have a Money obj
        if isinstance(value, Money):
            value = value.amount
        return graphene.Float.coerce_float(value)

    serialize = coerce_float
    parse_value = coerce_float


class MoneyString(graphene.String):
    @staticmethod
    def coerce_string(value):
        if isinstance(value, Money):
            locale = get_current_locale()
            text = format_money(
                money=value,
                decimal_places=value.decimal_places,
                locale=locale,
            )
            return text
        return graphene.String.coerce_string(value)

    serialize = coerce_string
    parse_value = coerce_string

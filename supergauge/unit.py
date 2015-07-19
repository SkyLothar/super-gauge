from collections import namedtuple


__support_units__ = (
    "percent",
    "sec",
    "ms",
    "millsec",
    "byte",
    "kb",
    "mb",
    "gb",
    "tb",
    "count",
    "bps",
    "cps"
)

Unit = namedtuple(
    "Unit",
    __support_units__
)

unit = Unit(*__support_units__)

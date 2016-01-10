# coding:utf-8
from django import template
from mysite2.utils import Json

register = template.Library()


@register.filter
def lower(value):
    return value.lower()

@register.filter
def upper(value):
    return value.upper()

@register.filter
def json(value):
    return Json.encode(value)
# _*_ coding:utf-8 _*_
# __auth__: LJ

from django import template
import ast
import json

register = template.Library()


@register.filter(name='get_cpu_model')
def get_cpu_model(value):
    try:
        dict_data = json.loads(value)
        first_cpu_dict = dict_data['cpu'][0]
        return first_cpu_dict['model']
    except Exception, e:
        print e.message
    return None


@register.filter(name='get_cpu_count')
def get_cpu_count(value):
    try:
        dict_data = json.loads(value)
        cpu_list = dict_data['cpu']
        return len(cpu_list)
    except Exception, e:
        print e.message
    return None


@register.filter(name='get_cpu_core_count')
def get_cpu_core_count(value):
    try:
        dict_data = json.loads(value)
        cpu_list = dict_data['cpu']
        return sum([cpu['cpu_core_count'] for cpu in cpu_list])
    except Exception, e:
        print e.message
    return None


@register.filter(name='sum_cpu_count')
def sum_cpu_count(value):
     return len(value)


@register.filter(name='sum_cpu_core_count')
def sum_cpu_core_count(value):
     return sum([cpu.cpu_core_count for cpu in value])


@register.filter(name='sum_size')
def sum_size(value):
    return sum([item.capacity if item.capacity else 0 for item in value])


@register.filter(name='sum_count')
def sum_count(queryset):
    return len(queryset)
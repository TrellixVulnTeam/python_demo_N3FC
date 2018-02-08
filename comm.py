#!/bin/usr/python3

def money_format(value): #金额格式化
    value = "%.2f" % float(value)
    components = str(value).split('.')
    if len(components) > 1:
        left, right = components
        right = '.' + right
    else:
        left, right = components[0], ''

    result = ''
    while left:
        result = left[-3:] + ',' + result
        left = left[:-3]
    return result.strip(',') + right


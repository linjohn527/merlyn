# _*_ coding:utf-8 _*_
# __auth__: LJ


def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.strftime('%Y-%m-%d')


def json_datetime_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
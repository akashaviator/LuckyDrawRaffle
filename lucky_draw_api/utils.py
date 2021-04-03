from dateutil.parser import parse

def parse_datetime(date):
    dt = parse(date)
    return dt.strftime("%d/%m/%Y, %H:%M:%S")
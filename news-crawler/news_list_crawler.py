import datetime as dt
from dateutil.relativedelta import relativedelta

def fetch_news_list_for_date(date):
    datestr = date.strftime('%Y%m%d')
    
    print(datestr)

if __name__ == '__main__':
    base_date = dt.datetime(2023, 8, 1)

    for d in range(40):
        date = base_date + relativedelta(days=d)

        fetch_news_list_for_date(date);
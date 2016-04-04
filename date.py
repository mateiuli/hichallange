from datetime import timedelta, date
import calendar, locale

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)

start_date = date(2016, 1, 1)
end_date = date(2016, 12, 31)



for single_date in daterange(start_date, end_date):
    print single_date.strftime("%Y-%B-%d")


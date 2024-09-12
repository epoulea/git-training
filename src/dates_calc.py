import datetime
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


start_of_year = datetime(2024, 1, 1)
start_of_previous_year = datetime(2023, 1, 1) 

# Get today's date
today = datetime.now()
one_year_ago = today - timedelta(days=365)
print(one_year_ago)
yesterday = today - timedelta(days=1)
#one_year_ago = yesterday - timedelta(days=365)

# Calculate the difference in days
ytd_days = (today - start_of_year).days
ytd_days_prv = (one_year_ago - start_of_previous_year).days
print(ytd_days_prv)
ytd_days_before = (yesterday - start_of_year).days
print(ytd_days_before)

formatted_date = (start_of_year + timedelta(days=ytd_days)).strftime("%d-%b-%y")
formatted_date_prv = (start_of_previous_year + timedelta(days=ytd_days_prv)).strftime("%d-%b-%y")
formated_date_prv_form = (start_of_previous_year + timedelta(days=ytd_days_before)).strftime("%d-%b-%y")
formatted_date_before = (start_of_year + timedelta(days=ytd_days_before)).strftime("%d-%b-%y")
print(formatted_date_before)

# Print the year-to-date in days
print(f"The year to date from 1 January 2024 until today is {ytd_days} days.")
print(f"The year to date from 1 January 2023 until today is {ytd_days_prv} days.")
print(f"The year to date from 1 January 2023 until today is {ytd_days_before} days.")
print(f"Formatted date for {ytd_days} days ago: {formatted_date}")
print(f"Formatted date for {ytd_days_prv} days ago: {formatted_date_prv}")
#print(f"Formatted date for {ytd_days_before} days ago: {formatted_date_before}")
print(f"Formatted date for test {ytd_days_before} days ago: {formated_date_prv_form}")

def is_working_day(check_date):
    # Assuming weekends (Saturday and Sunday) are not working days
    return check_date.weekday() < 5

def get_past_date(str_days_ago):
    TODAY = date.today()
    splitted = str_days_ago.split()

    def subtract_working_days(skip_date, days_to_subtract):
        while days_to_subtract > 0:
            skip_date -= relativedelta(days=1)
            if is_working_day(skip_date):
                days_to_subtract -= 1
        return skip_date

    if len(splitted) == 1 and splitted[0].lower() == 'today':
        if is_working_day(TODAY):
            return TODAY.strftime("%d-%b-%y")
        else:
            return subtract_working_days(TODAY, 1).strftime("%d-%b-%y")
    elif len(splitted) == 1 and splitted[0].lower() == 'yesterday':
        return subtract_working_days(TODAY, 1).strftime("%d-%b-%y")
    elif splitted[1].lower() in ['day', 'days', 'd']:
        return subtract_working_days(TODAY, int(splitted[0])).strftime("%d-%b-%y")
    elif splitted[1].lower() in ['wk', 'wks', 'week', 'weeks', 'w']:
        return subtract_working_days(TODAY, int(splitted[0]) * 5).strftime("%d-%b-%y")
    elif splitted[1].lower() in ['mon', 'mons', 'month', 'months', 'm']:
        # For months, we approximate 4 weeks per month
        return subtract_working_days(TODAY, int(splitted[0]) * 20).strftime("%d-%b-%y")
    elif splitted[1].lower() in ['yrs', 'yr', 'years', 'year', 'y']:
        # For years, we approximate 52 weeks per year
        return subtract_working_days(TODAY, int(splitted[0]) * 260).strftime("%d-%b-%y")
    else:
        return "Wrong Argument format"

# Test the function
# print(get_past_date('today'))    
# print(get_past_date('yesterday'))
# print(get_past_date('7 days ago'))
#print(get_past_date('20 days ago'))
#print(get_past_date('69 days ago'))










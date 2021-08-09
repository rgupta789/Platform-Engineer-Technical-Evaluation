import json
import pandas
from datetime import date as dt
import datetime
from dateutil.relativedelta import relativedelta
import os
import urllib3
import calendar

sheet_id = '1rXXWQdneb0d4dDQw4LOeLpa8YDTOwvlQl0Ad2xzswXc'
webhook_url = "https://webhook.site/5e9857a0-a82c-4ef6-9590-274e27661285"

def check_date(date, comparator):
    if date > comparator:
        return True
    else:
        return False

def get_first_name(customer):
    return customer[0]

def get_last_name(customer):
    return customer[1]

def get_email(customer):
    return customer[2]

def get_ticket(customer):
    return customer[3]

def get_ticket_status(customer):
    return customer[4]

def get_date(customer):
    return customer[5]


def lambda_handler(event, context):
    df = pandas.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
    customer_list = df.values.tolist()
    eighteen_months = datetime.datetime.today() + relativedelta(months=-18)

    http = urllib3.PoolManager()

    customers_with_closed_tickets = []

    if os.environ["First_run"] == "True":
        os.environ["First_run"] = "False"
        os.environ["Last_run_date"] = datetime.datetime.today().strftime('%d/%m/%Y')
        for customer in customer_list:
            date = get_date(customer)
            ticket_status = get_ticket_status(customer)
            first_name = get_first_name(customer)
            last_name = get_last_name(customer)
            email = get_email(customer)
            ticket = get_ticket(customer)

            date_obj = (datetime.datetime.strptime(date, '%d/%m/%Y'))
            within_eighteen_months = check_date(date_obj, eighteen_months)

            if get_ticket_status(customer) == 'Closed' and within_eighteen_months:
                split_date = date.split('/')
                date_day = split_date[0]
                if date_day[0] == "0":
                    date_day = date_day[-1]
                date_month = split_date[1]
                date_year = split_date[2]

                month_name = calendar.month_name[int(date_month)]

                suffix = ""
                if date_day[-1] == "1":
                    suffix = "st"
                elif date_day[-1] == "2":
                    suffix = "nd"
                elif date_day[-1] == "3":
                    suffix = "rd"
                else:
                    suffix = "th"

                unambiguous_date = date_day + suffix + " of " + month_name + " " + date_year

                payload = {
                    "full_name": first_name + " " + last_name.upper(),
                    "email_address": email,
                    "ready_to_send": "true",
                    "email" : {
                        "subject": "Ticket: " + ticket + "- Closed" ,
                        "to_address": [email],
                        "cc_address": [""],
                        "body": "Hello " + first_name + ",\\n\\nYour ticket " + ticket + " was closed on the " + unambiguous_date + "\\n\\nRegards,\\n"
                    }
                }

                print(payload)
                r = http.request('POST', webhook_url, headers = {'Content-Type': 'application/json'}, body = json.dumps(payload))


    elif os.environ["First_run"] == "False":
        for customer in customer_list:
            date = get_date(customer)
            ticket_status = get_ticket_status(customer)
            first_name = get_first_name(customer)
            last_name = get_last_name(customer)
            email = get_email(customer)
            ticket = get_ticket(customer)

            last_run_date = (datetime.datetime.strptime(os.environ["Last_run_date"], '%d/%m/%Y')).dt()
            date_object = (datetime.datetime.strptime(date, '%d/%m/%Y')).dt()

            # Check if the customer is a new entry by comparing date against last run date
            new_entry = check_date(date, last_run_date)

            # If the ticket has been closed since the last run date, then send an email
            if get_ticket_status(customer) == 'Closed' and new_entry:
                print(date)
                split_date = date.split('/')
                date_day = split_date[0]
                if date_day[0] == "0":
                    date_day = date_day[-1]
                date_month = split_date[1]
                date_year = split_date[2]

                month_name = calendar.month_name[int(date_month)]

                suffix = ""
                if date_day[-1] == "1":
                    suffix = "st"
                elif date_day[-1] == "2":
                    suffix = "nd"
                elif date_day[-1] == "3":
                    suffix = "rd"
                else:
                    suffix = "th"

                unambiguous_date = date_day + suffix + " of " + month_name + " " + date_year

                payload = {
                    "full_name": first_name + " " + last_name.upper(),
                    "email_address": email,
                    "ready_to_send": "true",
                    "email" : {
                        "subject": "Ticket: " + ticket + "- Closed" ,
                        "to_address": [email],
                        "cc_address": [""],
                        "body": "Hello " + first_name + ",\\n\\nYour ticket " + ticket + " was closed on the " + unambiguous_date + "\\n\\nRegards,\\n"
                    }
                }

                #print(payload)
                r = http.request('POST', webhook_url, headers = {'Content-Type': 'application/json'}, body = json.dumps(payload))

        os.environ["Last_run_date"] = datetime.today().strftime('%d/%m/%Y')
# Platform-Engineer-Technical-Evaluation
This repository contains the code I have written for my lambda function as part of my solution for my technical evaluation.

## Solution
My solution for this task is an AWS Lambda function which contains the code written in Python. This function is triggered once a week at 1am on Monday mornings by a CloudWatch event.
My program uses the pandas library to read the Google sheet as csv, and then converts this into a list format. It then iterates through each customer in the list, and if their ticket has been closed within the last eighteen months (if this is the first run) or is a new entry (for all consecutive runs) then it will submit an email to the WebHook. It uses an environment variable to check whether it is the first time the program is being run and also to check the date on which it was last run.

## Assumptions
There are a couple of assumptions I have made when designing this solution:
1. New entries: I was not completely clear on what can be defined as a "new entry" in all consecutive runs after the first run. I have defined a new entry to be either a new customer/ticket that has been appended to the end of the sheet and closed since the last run, or an existing customer/ticket that has had it's ticket's status changed to 'Closed' since the last run.
2. Customers should not receive more than one email a week: This leads me to believe that one customer may have multiple tickets, and that if they have multiple tickets that have been detected as 'Closed' within the same week then they should only receive one email detailing all of the tickets that have been closed, rather than an email per closed ticket. However, I was unable to implement this solution on time so my code only caters to the case where customers may only have one ticket.

## Improvements
1. I think a preferable method of reading the sheet would be to use the Google Sheets API. This would handle the case where the sheet is not public
2. In regards to Assumption #2 (above), I would have liked to handle the situation where a customer can have multiple tickets since realistically this is a very likely scenario

## AWS Account Access
1. Logon to the console as an IAM user. The account number is '757293290839' and the username is 'Evaluator'. The password has been sent to the hiring manager for this role
2. Navigate to the Lambda service
3. Test the function to run it. The logs will print the payload for each closed ticket

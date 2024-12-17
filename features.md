
# Needs/Pain Points

Need to select specific sections/answers in the IRS 990 form.

Need to be able to reliably convert information in XML to relevant and accurate
data types for the database

Need to provide ability to connect to database to send/modify data as necessary

Need a reference list of college names to filter irrelevant IRS 990 forms. Recall
IRS 990 covers most non-profit organizations, which colleges in the United States
are a subset of.

Need to encapsulate IRS 990 data from other tables but provide a way to allow
for cohesion between different tables

# Features

Ability to select specific sections/answers in the IRS 990 form.

Ability to derive a reference list of colleges via IPEDS.

Ability to automate the process of sending data to the database and update
tables with minimal manual intervention.

Provide a separate table for IRS data, which will also assist with encapsulation

Current extracted datapoints:

- Section B, question 13
- Section B, questions 15a and 15b
- Part VII, Section A, 1a

# Constraints

Assumes all IRS forms will be of the following structure: <https://www.irs.gov/forms-pubs/about-form-990>

Assumes all names of collegs to pull will use IPEDS as a reference point.

# Process

1. Specify the range of years to pull data from
2. Repeat the following for each year:
    1. Download the ZIP file corresponding to each month
    2. Repeat the following for each month:
        1. Repeat the following for each form:
            1. Retrieve the following information:

            - Organization name
            - Section A, Part I, question 15
            - Section A, Part V, 2a
            - Section B, question 13
            - Section B, question 15
            - Part VII, Section A, 1a

            2. Guess the gender of each stakeholder
            3. Calculate the average wage as follows:
                1. Find the total funds spent on salaries
                2. Deduct the sum of the salaries from Part VII, Section A, 1a
                3. Divide the result by the number of employees
                4. Calculate the ratio between the salary of the highest-paid stakeholder
                and the result from step 3

    3. Delete the directory containing the unzipped files

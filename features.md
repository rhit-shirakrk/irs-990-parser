
# Needs/Pain Points

Need to select specific sections/answers in the IRS 990 form.

Need to be able to reliably convert information in XML to relevant and accurate
data types for the database

Need to provide ability to connect to database to send/modify data as necessary

Need to encapsulate IRS 990 data from other tables but provide a way to allow
for cohesion between different tables

# Features

Ability to select specific sections/answers in the IRS 990 form.

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

1. Parse the XML file
2. Get the name of the organization
3. If the name is not a recognized institution, then skip the file. Otherwise,
continue.
4. Get the required datapoints listed above.
5. For each name in Part VII, Section A, 1a, guess the gender of the person and
record the result.

- Assume the only two genders are male and female
- Store the total number of male and female stakeholders

6. Calculate the percentage of male/female stakeholders and record this
information.

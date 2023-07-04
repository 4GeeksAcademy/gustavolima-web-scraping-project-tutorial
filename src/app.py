import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

# Parse with BeautifulSoup to interpert the data
soup = BeautifulSoup(open('/workspaces/gustavolima-web-scraping-project-tutorial/src/list.html'), "html")
tables = soup.find_all("table")

# Convert the table element to a string
table_html = str(tables)

# Read the HTML content using pandas
tesla_revenue = pd.read_html(table_html)[0]

# Remove the "Unnamed" column if present
tesla_revenue = tesla_revenue.loc[:, ~tesla_revenue.columns.str.startswith('Unnamed')]

# Rename the columns
tesla_revenue = tesla_revenue.rename(columns={"Tesla Quarterly Revenue(Millions of US $)": "Date", "Tesla Quarterly Revenue(Millions of US $).1": "Revenue"})
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].replace(",", '').replace('$', '')

# Drop rows with NaN values
tesla_revenue = tesla_revenue.dropna()

# Convert the Revenue int64 column to a String
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].astype(str)

# Import SQLite and convert the DF to a Tuples List
import sqlite3

records = tesla_revenue.to_records(index=False)
datatuples = list(records)
datatuples

# Connect to the SQLite DB and create the db, table, and insert
con = sqlite3.connect('Tesla.db')

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Tesla (Date, Revenue)")

cur.executemany("INSERT INTO Tesla VALUES (?, ?)", datatuples)

con.commit()

# Query the Table in SQL

for row in cur.execute('SELECT * FROM Tesla'):
    print(row)
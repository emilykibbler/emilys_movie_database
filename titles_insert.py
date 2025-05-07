__author__ = 'silvianittel'
__copyright__ = "Copyright 2025, SIE557"
__version__ = "1.0"
__date__ = "03/18/2025"

import pymysql.cursors
import final_db_config
import pandas as pd
import numpy as np

# Connect to the database
try:
    conn = pymysql.connect(host=final_db_config.DB_SERVER,
                      user=final_db_config.DB_USER,
                      password=final_db_config.DB_PASS,
                      database=final_db_config.DB)
    print("successfully connected to database")

except (Exception) as error:
    print("Error while connecting to MYSQL", error)
    exit()

test_dat = pd.read_csv('/Users/emilykibbler/Documents/Classes/SIE_557 database/final_project/data/title.basics.tsv',
                       sep="\t",
                       na_values="\\N",
                       # nrows=1000000,
                       low_memory=False)


# Don't need this column, just drop to avoid confusion
test_dat.drop("genres", axis="columns", inplace=True)
# Titles that got messed up in the tsv and have "\t" in the middle of the name, drop them
test_dat = test_dat[~test_dat['primaryTitle'].str.contains("\t", na=False)]
# These should be NULL but it was going in as "NULL" which doesn't work, 0 works.
# Could fix later if needed with an update-where command in SQL
test_dat["endYear"] = test_dat["endYear"].fillna(0).astype(int)
test_dat["startYear"] = test_dat["startYear"].fillna(0).astype(int)
test_dat["runtimeMinutes"] = test_dat["runtimeMinutes"].fillna(0).astype(int)

# foreign keys that cause an error, I'll go back and update these manually in SQL
problems = (
'tt0072308',
'tt0027125',
'tt0050419',
'tt0049189',
'tt0053137',
'tt0054452',
'tt0056404',
'tt0057345',
'tt0072308',
'tt0027125',
'tt0050419',
'tt0027125',
'tt0049189',
'tt0050419',
'tt0053137',
'tt0056404',
'tt0057345',
'tt0053137',
'tt0072308')

test_dat = test_dat[~test_dat.tconst.isin(problems)]
test_dat.dropna(subset=["primaryTitle"], inplace=True)

# create insert statement

try:
    with conn.cursor() as cursor:
        # Create a new record as a test example
        for i in range(len(test_dat)):
            sql = ("replace INTO `movie_db`.`titles` " +
                   "(`tconst`, `titleType`, `primaryTitle`, `originalTitle`, isAdult, startYear, endYear, runtimeMinutes) " +
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            cursor.execute(sql, (list(test_dat.iloc[i,0:8])))
            conn.commit()
            # print("Successfully inserted record")

except (Exception) as error:
    print("Error while inserting data to MYSQL", error)
    exit()

finally:
    cursor.close()
    conn.close()



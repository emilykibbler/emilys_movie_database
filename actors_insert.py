
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


dat = pd.read_csv('/Users/emilykibbler/Documents/Classes/SIE_557 database/final_project/data/name.basics.tsv',
                       sep="\t",
                       na_values="\\N",
                       # nrows=5000,
                       low_memory=False)

dat.dropna(subset=["primaryName"], inplace=True)
dat.dropna(subset=["nconst"], inplace=True)
dat["birthYear"] = dat["birthYear"].fillna(0).astype(int)

try:
    with conn.cursor() as cursor:

        for i in range(len(dat)):
            if pd.isna(dat.iloc[i, 3]):
                # I used insert ignore so it would skip any actors I already did in my manual load
                sql = ("insert ignore INTO `movie_db`.`actors` (`nconst`, `primaryName`, `birthYear`) VALUES (%s, %s, %s)")
                cursor.execute(sql, (list(dat.iloc[i,0:3])))
                conn.commit()
            else:
                sql = ("insert ignore INTO `movie_db`.`actors` (`nconst`, `primaryName`, `birthYear`, deathYear) VALUES (%s, %s, %s, %s)")
                cursor.execute(sql, (list(dat.iloc[i,0:4])))
                conn.commit()
            if type(dat.iloc[i, 5]) is str:
                temp = dat.iloc[i, 5].split(",")
                for j in range(len(temp)):
                    sql = ("insert ignore INTO `movie_db`.`knownFor` (`nconst`, `tconst`) VALUES (%s, %s)")
                    cursor.execute(sql, (list([dat.iloc[i, 0], temp[j]])))
                    conn.commit()

except (Exception) as error:
    print("Error while inserting data to MYSQL", error)
    exit()


finally:
    cursor.close()
    conn.close()

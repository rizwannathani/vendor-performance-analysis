import pandas as pd 
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename="vendorlogs/injestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s", 
    filemode="a"
)



#first we will create a database with the help of engine 
engine = create_engine('sqlite:///vendorinventory.db')


def injest_db(df, table_name, engine): 
    # this function will injest the data into databse
    df.to_sql(table_name, con = engine, if_exists = 'replace', index=False)



def load_raw_date():  
    # this function will read the files and injest the data into database
        start = time.time()
        for files in os.listdir("C:/datasets/vendor_performance/data"):
            if '.csv' in files:
                df = pd.read_csv("C:/datasets/vendor_performance/data/"+files)
                # we are using injest_db function to injest the data into db
                injest_db(df,files[:-4],engine)
                logging.info(f"Injesting {files} in db")


                
        end = time.time()
        total_time = (end -start)/60
        logging.info("Injestion complete")
        logging.info(f"Total time taken {total_time} minutes")


if __name__ == '__main__':
    load_raw_date()

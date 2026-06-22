import pandas as pd 
import os 
from sqlalchemy import create_engine
import logging
import time
from injestion_db import injest_db
import sqlite3 
import importlib

importlib.reload(logging)

logging.basicConfig(
    filename="vendorlogs/get_vendor_performance_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s", 
    filemode="a"
) 

def create_vendor_performance_summary(conn):

    # '''This function will create one table by merging different tables '''
        
            ## this query is taking too much time to execute we need to optimize this query 
        
        vender_sale_summary = pd.read_sql_query("""WITH Freightsummary AS(
             SELECT 
                VendorNumber,
                SUM(Freight) AS FreightCost
             FROM vendor_invoice
             GROUP BY VendorNumber
             
        ),
        
        PurchaseSummary AS (
              SELECT
                  p.VendorNumber, 
                  p.VendorName, 
                  p.Brand,
                  p.Description, 
                  p.PurchasePrice, 
                  pp.Volume,
                  pp.Price AS Actualprice,
                  SUM(p.Quantity) AS TotalPurchaseQuantity, 
                  SUM(p.Dollars) AS TotalPurchaseDollar
              FROM purchases AS p 
              JOIN purchase_prices AS pp ON p.Brand = pp.Brand
              WHERE p.PurchasePrice > 0
              GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume           
              
        ),
        
        SaleSummary AS (
            SELECT
              VendorNo,
              Brand, 
              SUM(SalesQuantity) AS TotalSalesQuantity,
              SUM(SalesDollars) AS TotalSaleDollar, 
              SUM(SalesPrice) AS TotalSalePrice, 
              SUM(ExciseTax) AS TotalExciseTax
            FROM sales
            GROUP BY VendorNo, Brand
        )
        
        SELECT 
           ps.VendorNumber, 
           ps.VendorName, 
           ps.Brand,
           ps.Description, 
           ps.PurchasePrice, 
           ps.Actualprice,
           ps.Volume,
           ps.TotalPurchaseQuantity, 
           ps.TotalPurchaseDollar,
           ss.TotalSalesQuantity,
           ss.TotalSaleDollar, 
           ss.TotalSalePrice, 
           ss.TotalExciseTax,
           fs.FreightCost
        FROM PurchaseSummary AS ps
        LEFT JOIN SaleSummary AS ss ON ps.VendorNumber = ss.VendorNo AND ps.Brand = ss.Brand
        LEFT JOIN Freightsummary AS fs ON ps.VendorNumber = fs.VendorNumber
        ORDER BY ps.TotalPurchaseDollar DESC
        
        """,conn)
        
        return vender_sale_summary

def clean_data(df):
    # '''This function will clean the data'''
    #changing the datatype to float
    df['Volume'] = df['Volume'].astype('float64')

    #filling missing values with 0
    df.fillna(0, inplace=True)

    #removing extra spaces from categorical data
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    #creating columns for better understanding 
    df['GrossProfit'] = df['TotalSaleDollar'] - df['TotalPurchaseDollar']
    df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSaleDollar'])*100
    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    df['SalesToPurchaseRation'] = df['TotalSaleDollar']/df['TotalPurchaseDollar']


    return df


 
if __name__ == '__main__':
    #creating database connection
    conn = sqlite3.connect('vendorinventory.db')

    logging.info("creating vender summary table.....")
    summary_df = create_vendor_performance_summary(conn)
    logging.info(summary_df.head())

    
    logging.info("cleaning data.....")
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info("injesting data.....")
    injest_db(clean_df,'vender_sale_summary',conn)
    logging.info("completed.")















import pandas as pd
import sqlite3
import logging
from ingestion_db import ingest_db
logging.basicConfig(    
    filename = "logs/get_vendor_summary.log",
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    filemode = "a",
    force= True
    )

def create_vendor_summary(conn):
    '''this function will merge the different tables to get the overall vendor summary and adding new columns in the resultant area'''
    vendor_sales_summary = pd.read_sql_query("""WITH FreightSummary AS (
               SELECT
                  VendorNumber,
                  SUM(Freight) AS FreightCost
               FROM vendor_invoice
               GROUP BY VendorNumber ),
                                        
               PurchasePrice AS (
               SELECT
                  p.VendorNumber,
                  p.VendorName,
                  p.Brand,
                  p.Description,
                  p.PurchasePrice,
                  pp.Price as ActualPrice,
                  pp.Volume,
                 SUM(p.Quantity) as TotalPurchaseQuantity,
                 SUM(p.Dollars) as TotalPurchaseDollars
                 FROM purchases p
                 JOIN purchase_prices pp
                     ON p.Brand = pp.Brand
                  WHERE p.PurchasePrice > 0
                GROUP BY p.VendorNumber,p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
                  ),

               SalesSummary AS (
                  SELECT
                     VendorNo,
                     Brand,
                     sum(SalesQuantity) as TotalSalesQuantity,
                     sum(SalesDollars) as TotalSalesDollars,
                     sum(SalesPrice) as TotalSalesPrice,
                     sum(ExciseTax) as TotalExciseTax
                  FROM sales
                  GROUP BY VendorNo, Brand
               )
               SELECT
                          ps.VendorNumber,
                          ps.VendorName,
                          ps.Brand,
                          ps.Description,
                          ps.PurchasePrice,
                          ps.ActualPrice,
                          ps.Volume,
                          ps.TotalPurchaseQuantity,
                          ps.TotalPurchaseDollars,
                          ss.TotalSalesQuantity,
                          ss.TotalSalesDollars,
                          ss.TotalSalesPrice,
                          ss.TotalExciseTax,
                          fs.FreightCost
                                         FROM PurchasePrice ps
                                         LEFT JOIN SalesSummary ss
                                          ON ps.VendorNumber = ss.VendorNo
                                          AND ps.Brand = ss.Brand
                                         LEFT JOIN FreightSummary fs
                                          ON ps.VendorNumber = fs.VendorNumber
                                         ORDER BY ps.TotalPurchaseDollars DESC""",conn)
    return vendor_sales_summary

def clean_data(df):
    '''this fucntion will clean the data'''
    #changing datatype to float
    df['Volume'] = df['Volume'].astype('float')

    #filling missing values with na
    df.fillna(0,inplace = True)

    #removing spaces from categorical columns]
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    #creating new coloumns for better analysis
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit']/df['TotalSalesDollars'])*100
    df['StockTurnover'] = (df['TotalSalesQuantity']/df['TotalPurchaseQuantity'])
    df['SalestoPurchaseRatio'] = df['TotalSalesDollars']/df['TotalPurchaseDollars']

    return df

if __name__ == '__main__':
    #creating database connection
    conn = sqlite3.connect('inventory.db')

    logging.info('Creating Vendor Summary Table....')
    summary_df = create_vendor_summary(conn)
    logging.info(summary_df.head())

    logging.info('Cleaing Data')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info('Ingesting data...')
    ingest_db(clean_df,'vendor_sales_summary',conn)
    logging.info('Completetd')
import openpyxl
import pymysql
import dbconfig as cfg


# creates the database connection from python dictionary file
con = pymysql.connect(host=cfg.mysql['host'], user=cfg.mysql['user'],password=cfg.mysql['password'], db=cfg.mysql['db'])
cur = con.cursor()
sql = """update People
       SET playerImage=%s
       WHERE playerId= %s;"""

# Define variable to load the dataframe
dataframe = openpyxl.load_workbook("PlayerAndImages.xlsx")
 
# Define variable to read sheet
dataframe1 = dataframe.active
 
# Iterate the loop to read the cell values
for row in dataframe1.iter_rows(min_row=1, max_col=3, values_only=True):
    if row[1] is not None:
        param = [row[1],row[0]]
        cur.execute(sql,param)
        con.commit()
        
        
cur.close()
con.close()


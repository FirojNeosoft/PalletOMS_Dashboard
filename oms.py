import pyodbc
server = '132.148.132.59'
database = 'PalletOMS_Test'
username = 'firoj'
password = 'November@2018'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

print ('sucessfully connected')

cursor.execute("SELECT AVG(INVOICEAMOUNT) FROM TBLTSALESINVOICE WHERE CUSTOMERID=2290 AND INVOICEDATE BETWEEN '2018-10-16' AND '2018-11-13';")
row = cursor.fetchone()
print("AVG Sales= "+str(row[0]))

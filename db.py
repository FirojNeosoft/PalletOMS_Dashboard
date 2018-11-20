import pymssql, datetime


class DatabaseConnection:

    def __init__(self):
        conn = pymssql.connect(server='132.148.132.59', user='firoj', password='November@2018', database='PalletOMS_Test')
        self.cursor = conn.cursor()

    # yearly
    def calculate_cy_ytd(self, company_id):
        self.cursor.execute(
            "SELECT SUM(INVOICEAMOUNT) AS SALES FROM TBLTSALESINVOICE WHERE COMPANYID="+str(company_id)+" AND INVOICEDATE <= GetDate() and YEAR(INVOICEDATE) = YEAR(GetDate()) GROUP BY COMPANYID")
        row = self.cursor.fetchone()
        if row:
            return float(row[0])
        else:
            return 0

    # quaterly
    def calculate_cy_quaterly_ytd(self, company_id, quater_no):
        now = datetime.datetime.now()
        if quater_no == 1:
            start_date= str(now.year)+'-01-01'
            end_date=str(now.year)+'-03-31'
        elif quater_no == 2:
            start_date= str(now.year)+'-04-01'
            end_date=str(now.year)+'-06-30'
        elif quater_no == 3:
            start_date= str(now.year)+'-07-01'
            end_date=str(now.year)+'-09-30'
        else:
            start_date= str(now.year)+'-10-01'
            end_date=str(now.year)+'-12-31'
        self.cursor.execute(
            "SELECT SUM(INVOICEAMOUNT) AS SALES FROM TBLTSALESINVOICE WHERE COMPANYID=" + str(
                company_id) + " AND INVOICEDATE BETWEEN '"+str(start_date)+"' and '"+str(end_date)+"' GROUP BY COMPANYID")
        row = self.cursor.fetchone()
        if row:
            return float(row[0])
        else:
            return 0

    # yearly
    def calculate_ly_ytd(self, company_id):
        self.cursor.execute(
            "SELECT SUM(INVOICEAMOUNT) AS SALES FROM TBLTSALESINVOICE WHERE COMPANYID="+str(company_id)+" AND INVOICEDATE < DATEADD(DAY, 1, DATEADD(YEAR, -1, DATEDIFF(DAY, '19000101', GETDATE())))")
        row = self.cursor.fetchone()
        if row and row[0]:
            return float(row[0])
        else:
            return 0

    # quaterly
    def calculate_ly_quaterly_ytd(self, company_id, quater_no):
        now = datetime.datetime.now()
        if quater_no == 1:
            start_date= str(now.year-1)+'-01-01'
            end_date=str(now.year-1)+'-03-31'
        elif quater_no == 2:
            start_date= str(now.year-1)+'-04-01'
            end_date=str(now.year-1)+'-06-30'
        elif quater_no == 3:
            start_date= str(now.year-1)+'-07-01'
            end_date=str(now.year-1)+'-09-30'
        else:
            start_date= str(now.year-1)+'-10-01'
            end_date=str(now.year-1)+'-12-31'

        self.cursor.execute(
            "SELECT SUM(INVOICEAMOUNT) AS SALES FROM TBLTSALESINVOICE WHERE COMPANYID=" + str(
                company_id) + " AND INVOICEDATE BETWEEN '"+str(start_date)+"' and '"+str(end_date)+"' GROUP BY COMPANYID")
        row = self.cursor.fetchone()
        if row and row[0]:
            return float(row[0])
        else:
            return 0

    def get_customer_name(self, customer_id):
        self.cursor.execute(
            "SELECT CUSTOMERNAME FROM TBLTCUSTOMER WHERE CUSTOMERID="+str(customer_id)
        )
        row = self.cursor.fetchone()
        if row[0]:
            return str(row[0])
        else:
            return ''

    def get_companies(self):
        self.cursor.execute(
            "SELECT COMPANYID, COMPANYNAME FROM TBLMCOMPANY")
        companies = []
        for row in self.cursor:
            companies.append({
                'id': int(row[0]),
                'name': str(row[1]),
            })
        return companies

    def get_top_customers(self, company_id):
        self.cursor.execute(
            "SELECT TOP 20 CUSTOMERID, SUM(INVOICEAMOUNT) AS SALE FROM TBLTSALESINVOICE WHERE COMPANYID="+str(company_id)+"GROUP BY CUSTOMERID ORDER BY SALE DESC")
        companies = []
        for row in self.cursor:
            companies.append({
                'name': self.get_customer_name(row[0]),
                # 'ly': self.calculate_ly_ytd(row[0]),
                # 'cy': self.calculate_cy_ytd(row[0])
            })
        return companies

    def calculate_category_cy_ytd(self, company_id):
        self.cursor.execute(
            "SELECT TBLMITEMCATEGORY.CATEGORYNAME, SUM(TBLTSALESINVOICEDETAIL.CALCULATEDAMOUNT) FROM(((TBLMITEMCATEGORY INNER JOIN TBLTITEM ON TBLMITEMCATEGORY.ITEMCATEGORYID = TBLTITEM.ITEMCATEGORYID)\
            INNER JOIN TBLTSALESINVOICEDETAIL ON TBLTITEM.ITEMID = TBLTSALESINVOICEDETAIL.ITEMID) INNER JOIN TBLTSALESINVOICE ON TBLTSALESINVOICEDETAIL.INVOICEID = TBLTSALESINVOICE.INVOICEID) WHERE\
            TBLMITEMCATEGORY.COMPANYID ="+str(company_id)+"AND YEAR(TBLTSALESINVOICE.INVOICEDATE) = YEAR(GetDate()) GROUP BY TBLMITEMCATEGORY.CATEGORYNAME"
        )
        sales = [float(row[1]) for row in self.cursor]
        if sales == []:
            return [0]
        return sales

    def calculate_category_ly_ytd(self, company_id):
        self.cursor.execute(
            "SELECT TBLMITEMCATEGORY.CATEGORYNAME, SUM(TBLTSALESINVOICEDETAIL.CALCULATEDAMOUNT) FROM(((TBLMITEMCATEGORY INNER JOIN TBLTITEM ON TBLMITEMCATEGORY.ITEMCATEGORYID = TBLTITEM.ITEMCATEGORYID)\
            INNER JOIN TBLTSALESINVOICEDETAIL ON TBLTITEM.ITEMID = TBLTSALESINVOICEDETAIL.ITEMID) INNER JOIN TBLTSALESINVOICE ON TBLTSALESINVOICEDETAIL.INVOICEID = TBLTSALESINVOICE.INVOICEID) WHERE\
            TBLMITEMCATEGORY.COMPANYID ="+str(company_id)+"AND YEAR(TBLTSALESINVOICE.INVOICEDATE) = YEAR(GetDate())-1 GROUP BY TBLMITEMCATEGORY.CATEGORYNAME"
        )
        sales = [float(row[1]) for row in self.cursor]
        if sales == []:
            return [0]
        return sales

    def get_top_categories(self, company_id):
        self.cursor.execute(
            "SELECT TOP 20 TBLMITEMCATEGORY.CATEGORYNAME, (SUM(TBLTSALESINVOICEDETAIL.CALCULATEDAMOUNT)) FROM(((TBLMITEMCATEGORY INNER JOIN TBLTITEM ON TBLMITEMCATEGORY.ITEMCATEGORYID = TBLTITEM.ITEMCATEGORYID)\
            INNER JOIN TBLTSALESINVOICEDETAIL ON TBLTITEM.ITEMID = TBLTSALESINVOICEDETAIL.ITEMID) INNER JOIN TBLTSALESINVOICE ON TBLTSALESINVOICEDETAIL.INVOICEID = TBLTSALESINVOICE.INVOICEID) WHERE\
            TBLMITEMCATEGORY.COMPANYID ="+str(company_id)+"AND YEAR(TBLTSALESINVOICE.INVOICEDATE) = YEAR(GetDate()) GROUP BY TBLMITEMCATEGORY.CATEGORYNAME"
        )
        sales = [{'name':row[0] , 'cy':float(row[1])} for row in self.cursor]
        categories = [row[0] for row in self.cursor]
        return categories

    def calculate_category_cy_ytd_pie(self, company_id):
        total_amount=1
        self.cursor.execute(
            "SELECT SUM(TBLTSALESINVOICEDETAIL.CALCULATEDAMOUNT) FROM(((TBLMITEMCATEGORY INNER JOIN TBLTITEM ON TBLMITEMCATEGORY.ITEMCATEGORYID = TBLTITEM.ITEMCATEGORYID)\
            INNER JOIN TBLTSALESINVOICEDETAIL ON TBLTITEM.ITEMID = TBLTSALESINVOICEDETAIL.ITEMID) INNER JOIN TBLTSALESINVOICE ON TBLTSALESINVOICEDETAIL.INVOICEID = TBLTSALESINVOICE.INVOICEID) WHERE\
            TBLMITEMCATEGORY.COMPANYID ="+str(company_id)+"AND YEAR(TBLTSALESINVOICE.INVOICEDATE) = YEAR(GetDate())"
        )
        total_amount = self.cursor.fetchone()
        if total_amount and total_amount[0]>0:
            total_amount=total_amount[0]
        elif total_amount and total_amount[0] == 0:
            total_amount = 1
        else:
            total_amount = 1
        self.cursor.execute(
            "SELECT TBLMITEMCATEGORY.CATEGORYNAME, (SUM(TBLTSALESINVOICEDETAIL.CALCULATEDAMOUNT)/"+str(total_amount)+")*100 FROM(((TBLMITEMCATEGORY INNER JOIN TBLTITEM ON TBLMITEMCATEGORY.ITEMCATEGORYID = TBLTITEM.ITEMCATEGORYID)\
            INNER JOIN TBLTSALESINVOICEDETAIL ON TBLTITEM.ITEMID = TBLTSALESINVOICEDETAIL.ITEMID) INNER JOIN TBLTSALESINVOICE ON TBLTSALESINVOICEDETAIL.INVOICEID = TBLTSALESINVOICE.INVOICEID) WHERE\
            TBLMITEMCATEGORY.COMPANYID ="+str(company_id)+"AND YEAR(TBLTSALESINVOICE.INVOICEDATE) = YEAR(GetDate()) GROUP BY TBLMITEMCATEGORY.CATEGORYNAME"
        )
        sales = [{'name':row[0] , 'y':float(row[1])} for row in self.cursor]
        if sales == []:
            return [{'name':'', 'y':0}]
        return sales

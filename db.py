import pymssql


class DatabaseConnection:

    def __init__(self):
        conn = pymssql.connect(server='132.148.132.59', user='firoj', password='November@2018', database='PalletOMS_Test')
        self.cursor = conn.cursor()

    def calculate_cy_ytd(self, company_id):
        self.cursor.execute(
            "SELECT SUM(INVOICEAMOUNT) AS SALES FROM TBLTSALESINVOICE WHERE COMPANYID="+str(company_id)+" AND INVOICEDATE <= GetDate() and YEAR(INVOICEDATE) = YEAR(GetDate()) GROUP BY COMPANYID")
        row = self.cursor.fetchone()
        if row[0]:
            return float(row[0])
        else:
            return 0

    def calculate_ly_ytd(self, company_id):
        self.cursor.execute(
            "SELECT SUM(INVOICEAMOUNT) AS SALES FROM TBLTSALESINVOICE WHERE COMPANYID="+str(company_id)+" AND INVOICEDATE < DATEADD(DAY, 1, DATEADD(YEAR, -1, DATEDIFF(DAY, '19000101', GETDATE())))")
        row = self.cursor.fetchone()
        if row[0]:
            return float(row[0])
        else:
            return 0

    def get_company_name(self, company_id):
        self.cursor.execute(
            "SELECT COMPANYNAME FROM TBLMCOMPANY WHERE COMPANYID="+str(company_id)
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

    def get_top_companies(self):
        self.cursor.execute(
            "SELECT TOP 20 COMPANYID, SUM(INVOICEAMOUNT) AS SALE FROM TBLTSALESINVOICE GROUP BY COMPANYID ORDER BY SALE DESC")
        companies = []
        for row in self.cursor:
            companies.append({
                'name': self.get_company_name(row[0]),
                'ly': self.calculate_ly_ytd(row[0]),
                'cy': self.calculate_cy_ytd(row[0])
            })
        return companies

    def calculate_category_cy_ytd(self, company_id):
        self.cursor.execute(
            "SELECT TBLMITEMCATEGORY.CATEGORYNAME, SUM(TBLTSALESINVOICEDETAIL.CALCULATEDAMOUNT) FROM(((TBLMITEMCATEGORY INNER JOIN TBLTITEM ON TBLMITEMCATEGORY.ITEMCATEGORYID = TBLTITEM.ITEMCATEGORYID)\
            INNER JOIN TBLTSALESINVOICEDETAIL ON TBLTITEM.ITEMID = TBLTSALESINVOICEDETAIL.ITEMID) INNER JOIN TBLTSALESINVOICE ON TBLTSALESINVOICEDETAIL.INVOICEID = TBLTSALESINVOICE.INVOICEID) WHERE\
            TBLMITEMCATEGORY.COMPANYID ="+str(company_id)+"AND YEAR(TBLTSALESINVOICE.INVOICEDATE) = YEAR(GetDate()) GROUP BY TBLMITEMCATEGORY.CATEGORYNAME"
        )
        import pdb; pdb.set_trace()
        sales = [float(row[1]) for row in self.cursor]
        return sales

    def calculate_category_ly_ytd(self, company_id):
        self.cursor.execute(
            "SELECT TBLMITEMCATEGORY.CATEGORYNAME, SUM(TBLTSALESINVOICEDETAIL.CALCULATEDAMOUNT) FROM(((TBLMITEMCATEGORY INNER JOIN TBLTITEM ON TBLMITEMCATEGORY.ITEMCATEGORYID = TBLTITEM.ITEMCATEGORYID)\
            INNER JOIN TBLTSALESINVOICEDETAIL ON TBLTITEM.ITEMID = TBLTSALESINVOICEDETAIL.ITEMID) INNER JOIN TBLTSALESINVOICE ON TBLTSALESINVOICEDETAIL.INVOICEID = TBLTSALESINVOICE.INVOICEID) WHERE\
            TBLMITEMCATEGORY.COMPANYID ="+str(company_id)+"AND YEAR(TBLTSALESINVOICE.INVOICEDATE) = YEAR(GetDate())-1 GROUP BY TBLMITEMCATEGORY.CATEGORYNAME"
        )
        sales = [float(row[1]) for row in self.cursor]
        return sales

    def get_top_categories(self, company_id):
        self.cursor.execute(
            "SELECT TBLMITEMCATEGORY.CATEGORYNAME FROM(((TBLMITEMCATEGORY INNER JOIN TBLTITEM ON TBLMITEMCATEGORY.ITEMCATEGORYID = TBLTITEM.ITEMCATEGORYID)\
            INNER JOIN TBLTSALESINVOICEDETAIL ON TBLTITEM.ITEMID = TBLTSALESINVOICEDETAIL.ITEMID) INNER JOIN TBLTSALESINVOICE ON TBLTSALESINVOICEDETAIL.INVOICEID = TBLTSALESINVOICE.INVOICEID) WHERE\
            TBLMITEMCATEGORY.COMPANYID ="+str(company_id)+"AND YEAR(TBLTSALESINVOICE.INVOICEDATE) = YEAR(GetDate()) GROUP BY TBLMITEMCATEGORY.CATEGORYNAME"
        )
        categories = [row[0] for row in self.cursor]
        return categories

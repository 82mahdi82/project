import mysql.connector
import time

def creat_product_table(brand,name,size, price,code):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor()
    cursor.execute("insert into product (brand,name,size, price,code) values (%s, %s, %s, %s,%s)",(brand,name,size, price,code))
    cursor.close()
    cnx.commit()

def insert_sales_row_table(inv_id,product_id,qty):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor()
    cursor.execute("insert into sales_row (inv_id,product_id,qty) values (%s,%s,%s)",(inv_id,product_id,qty))
    cnx.commit()
def insert_sales_table(cid,inv_id):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor(dictionary=True)    
    cursor.execute("insert into sales (cid,inv_id) values (%s,%s)",(cid,inv_id))
    cnx.commit()
    # cursor.execute(f"select inv_id from sales where cid={cid}")
    # res = cursor.fetchall()
    # inv_id=res[-1]["inv_id"]
    cursor.close()
    # return inv_id

def insert_shopping_cart_table(cid,product_id,qty):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor()
    cursor.execute("insert into shoppingcart (cid,product_id,qty) values (%s, %s,%s)",(cid,product_id,qty))
    cursor.close()
    cnx.commit()


def delete_shopping_cart_table_cid(cid):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor()
    cursor.execute(f"delete from shoppingcart where cid={cid}")
    cursor.close()
    cnx.commit()


def delete_shopping_cart_table(cid,product_id):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor()
    cursor.execute(f"delete from shoppingcart where cid={cid} and product_id={product_id}")
    cursor.close()
    cnx.commit()

def update_shopping_cart_table(cid,product_id,qty):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor()
    cursor.execute(f"update shoppingcart set qty={qty} where cid={cid} and product_id={product_id}")
    cursor.close()
    cnx.commit()

def use_sales_table(cid):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"select * from sales where cid={cid}")
    dict_product=cursor.fetchall()
    return dict_product

def use_sales_row_table(inv_id):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"select * from sales_row where inv_id={inv_id}")
    dict_product=cursor.fetchall()
    return dict_product


def use_shopping_cart_table(cid,prodoct_id):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"select * from shoppingcart where cid={cid} and product_id={prodoct_id}")
    dict_product=cursor.fetchall()
    return dict_product

def use_shopping_cart_table_where(where):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"select * from shoppingcart where {where}")
    dict_product=cursor.fetchall()
    return dict_product



def creat_sales_table(inv_id,cid):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor()
    cursor.execute("insert into sales (inv_id,cid) values (%s, %s)",(inv_id,cid))
    cursor.close()
    cnx.commit()

def creat_sales_row_table(inv_id,product_id,qty):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor()
    cursor.execute("insert into sales_row (inv_id,product_id,qty) values (%s, %s,%s)",(inv_id,product_id,qty))
    cursor.close()
    cnx.commit()


def creat_store_database():
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost')
    cursor = cnx.cursor()
    cursor.execute("DROP database IF EXISTS store")
    cursor.execute("create database if not exists store")
    cursor.execute("use store")
    cursor.execute("""CREATE TABLE if not exists customer (cid bigint PRIMARY KEY,
                    name VARCHAR(25) not null,
                   phone VARCHAR(15) ,
                   email VARCHAR(100),
                    address text)""")
    
    cursor.execute("""CREATE TABLE if not exists product (product_id bigint AUTO_INCREMENT PRIMARY KEY,
                   brand VARCHAR(25) not null, 
                   name VARCHAR(25) not null,
                   size float not null,
                   price float(10,2),
                   code int)""")
    
    cursor.execute("""CREATE TABLE if not exists sales (inv_id bigint PRIMARY KEY,
                   cid bigint not null,
                   date datetime not null default current_timestamp,
                   constraint fk_cid foreign key(cid) references customer(cid))""")
    
    cursor.execute("""CREATE TABLE if not exists sales_row (inv_id bigint not null, 
                   product_id bigint not null,
                   qty INT,
                   file_id VARCHAR(250),
                   constraint fk_inv foreign key(inv_id) references sales(inv_id),
                   constraint fk_product foreign key(product_id) references product(product_id))""")
    
    cursor.execute("""CREATE TABLE if not exists shoppingcart (cart_id INT AUTO_INCREMENT PRIMARY KEY,
                   cid bigint,
                   product_id bigint,
                   qty INT,
                   FOREIGN KEY (cid) REFERENCES customer(cid),
                   FOREIGN KEY (product_id) REFERENCES product(product_id));""")
    
    print("created")
    cursor.close()
    cnx.commit()
def creat_customer_table(cid,name,phone, email,address):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor()
    cursor.execute("select * from customer where cid=%s",(cid,))
    ll=cursor.fetchall()
    if len(ll)==1:
        cursor.execute("update customer set name=%s,phone=%s,email=%s,address=%s where cid=%s",(name,phone,email,address,cid))
        cnx.commit()
        cursor.close()
        print("update")
    else:
        cursor.execute("insert into customer (cid,name,phone, email, address) values (%s, %s, %s, %s, %s)", (cid,name,phone, email,address))
        cursor.close()
        cnx.commit()
        print("user created")


def create_one_customer(cid,key,value):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor()
    cursor.execute(f"insert ignore into customer (cid,{key}) values ({cid},'{value}')")
    print("PK")
    cnx.commit()
    cursor.close()
def update_customer_table(cid,set,set_q):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor()
    cursor.execute(f"update customer set {set}='{set_q}' where cid={cid}")
    print("ok")
    cnx.commit()
    cursor.close()

def use_product_table():
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("select * from product")
    dict_product=cursor.fetchall()
    return dict_product

def use_shoppingcart_table_where(cid):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"select * from shoppingcart where cid={cid}")
    dict_product=cursor.fetchall()
    return dict_product

def use_product_table_where(where):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"select * from product where {where}")
    dict_product=cursor.fetchall()
    return dict_product

def use_customer_table_where(where):
    cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"select * from customer where {where}")
    dict_customer=cursor.fetchall()
    for i in dict_customer:
        return i


def start_creat():
    creat_store_database()


    #drill granite
    code=2
    siz=[3,4,5,6,7,8,10,12,14]
    pr=[155000,175000,195000,245000,265000,300000,415000,555000,665000]
    for size,price in zip(siz,pr):
        creat_product_table("FORCE","granite",size, price,code)


    #drill HSS-CO 5%
    code=3
    siz1=[1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16]
    pr1=[49000,61000,75000,95000,128000,185000,215000,235000,258000,320000,365000,450000,530000,600000,680000,850000,980000,1150000,1230000,1280000,1650000,1850000,2050000,2350000,2500000,2750000,2950000,3300000,3450000,3850000,3950000,4300000]
    for size,price in zip(siz1,pr1):
        creat_product_table("FORCE","HSS-CO 5%",size, price,code)


    #drill HSS-CO
    code=4
    siz2=[1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16]
    pr2=[32000,38000,57000,70000,78000,90000,95000,110000,120000,138000,160000,190000,220000,240000,260000,380000,410000,450000,480000,495000,570000,650000,700000,840000,910000,950000,990000,1680000,1,1800000,1,2150000]
    for size,price in zip(siz2,pr2):
        creat_product_table("TALENT","HSS-CO",size, price,code)
        # cnx = mysql.connector.connect(user='root', password='ma8h2dii',host='localhost',database="store")
        # cursor = cnx.cursor()
        # cursor.execute(f"update product set brand='TALENT',name='HSS-CO' where size={size} and price={price}")
        # cnx.commit()
        # cursor.close()

    #drill all work
    code=5
    siz3=[3,4,5,6,7,8,10,12]
    pr3=[280000,300000,330000,380000,450000,500000,600000,680000]
    for size,price in zip(siz3,pr3):
        creat_product_table("FORCE","all work",size, price,code)

    # wood hold saw
    code=6
    siz4=[16,20,22,25,30,35,40,50,60]
    pr4=[450000,550000,600000,690000,820000,820000,1000000,1350000,1600000]
    for size,price in zip(siz4,pr4):
        creat_product_table("FORCETECH","gas drill",size, price,code)

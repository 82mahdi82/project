import time
import database
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import random

database.start_creat()

TOKEN = '6317356905:AAGQ2p8Lo0Kc4mkChTmE7ZbI2p1bzw9cIO8'

new_size_product={"name":"","brand":"","code":0}
mid_new_product=0
shopping_cart_stop={} #{cid:{tracking_code:[{},{}]}}
userStep = {}
ch_id = -1002046803532
admin = 748626808
products = {}
edit_deerails_admin={}
sssss = 0
check = {}  # cid:[[2222 , 2224] , 1]
block = {}



def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        userStep[uid] = 0
        return 0



def unblock(cid):
    if cid in block:
        if block[cid] < time.time():
            block.pop(cid)


def checking(cid):
    if cid in block:
        return
    check.setdefault(cid, {})
    check[cid].setdefault("time1", 0)
    check[cid].setdefault("time2", 0)
    check[cid].setdefault("score", 0)
    if check[cid]["time1"] == 0:
        check[cid]["time1"] = time.time()
    elif check[cid]["time2"] == 0:
        check[cid]["time2"] = time.time()
        timespam = check[cid]["time2"]-check[cid]["time1"]
        if int(timespam) < 3:
            check[cid]["score"] += 1
    else:
        check[cid]["time1"] = check[cid]["time2"]
        check[cid]["time2"] = time.time()
        timespam = check[cid]["time2"]-check[cid]["time1"]
        if int(timespam) < 3:
            check[cid]["score"] += 1
            if check[cid]["score"] == 20:
                bot.send_message(cid,"شما به دلیل اسپم زیاد به مدت 1 ساعت بن شدید")
                check[cid]["score"] = 0
                block[cid] = time.time()+10
        elif int(timespam) > 3:
            if check[cid]["score"] == 0:
                pass
            else:
                check[cid]["score"] -= 1

# def listener(messages):
#     """
#     When new messages arrive TeleBot will call this function.
#     """
#     for m in messages:
#         cid = m.chat.id
#         if m.content_type == 'text':
#             print(str(m.chat.first_name) +
#                   " [" + str(m.chat.id) + "]: " + m.text)
#         elif m.content_type == 'photo':
#             print(str(m.chat.first_name) +
#                   " [" + str(m.chat.id) + "]: " + "New photo recieved")
#         elif m.content_type == 'document':
#             print(str(m.chat.first_name) +
#                   " [" + str(m.chat.id) + "]: " + 'New Document recieved')


bot = telebot.TeleBot(TOKEN)
# bot.set_update_listener(listener)

def gen_product_markup_admin(code, size, qty):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('➖', callback_data=f'updqtystock_edit_{code}_{size}_{max(qty-1, 1)}'),
               InlineKeyboardButton(f'{qty}', callback_data='updqtystock_nothing'),
               InlineKeyboardButton('➕', callback_data=f'updqtystock_edit_{code}_{size}_{qty+1}'))
    markup.add(InlineKeyboardButton('✅ ذخیره کردن تغییرات',
               callback_data=f'updqtystock_add_{code}_{size}_{qty}'))
    markup.add(InlineKeyboardButton(
        "برگشت", callback_data=f"sshow_the_deetails_{code}"))
    return markup

def gen_product_markup(code, size, qty):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('➖', callback_data=f'product_edit_{code}_{size}_{max(qty-1, 1)}'),
               InlineKeyboardButton(f'{qty}', callback_data='product_nothing'),
               InlineKeyboardButton('➕', callback_data=f'product_edit_{code}_{size}_{qty+1}'))
    markup.add(InlineKeyboardButton('✅ افزودن به سبد خرید',
               callback_data=f'product_add_{code}_{size}_{qty}'))
    markup.add(InlineKeyboardButton(
        "برگشت", callback_data=f"size_{code}_back"))
    return markup


def gen_cart_markup(code, size, qty):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('➖', callback_data=f'cart_edit_{code}_{size}_{max(qty-1, 1)}'),
               InlineKeyboardButton(f'{qty}', callback_data='cart_nothing'),
               InlineKeyboardButton('➕', callback_data=f'cart_edit_{code}_{size}_{qty+1}'))
    markup.add(InlineKeyboardButton('❌ حذف از سبد خرید',callback_data=f'cart_delete_{code}_{size}'))
    return markup



def show_cart(cid):
    list_shoppingcart=database.use_shopping_cart_table_where(f"cid={cid}")
    price_total=0
    for b in list_shoppingcart:
        list_price=database.use_product_table_where(f"product_id={b['product_id']}")
        for i in list_price:
            price_total+=i["price"]*b["qty"]
    if price_total==0:
        return bot.edit_message_text("سبد خرید شما خالی است", cid,sssss)
    markup2 = InlineKeyboardMarkup()
    markup2.add(InlineKeyboardButton(
                "خرید و ثبت نهایی", callback_data="shop_cart"))
    return bot.edit_message_text(f"قیمت کل سبد خرید شما برابر است با :{price_total}", cid, sssss, reply_markup=markup2)


@bot.message_handler(func=lambda m: m.text == "برگشت به منو ادمین")
def command_start(m):
    cid = m.chat.id
    if cid==admin:
        userStep[cid]=0
        markup=ReplyKeyboardRemove()
        bot.send_message(cid,"پنل ادمین",reply_markup=markup)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(" افزودن محصول جدید",callback_data="admin_add"), InlineKeyboardButton("حذف محصول",callback_data="admin_delete"))
        markup.add(InlineKeyboardButton("ویرایش محصولات",callback_data="admin_edit"))
        markup.add(InlineKeyboardButton("استفاده از ربات به عنوان کاربر",callback_data="use_as_user"))
        bot.send_message(cid,"برای انجام تنظیمات از دکمه های زیر استفاده کنید",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==11)
def name_custom(m):
    global mid_new_product
    cid = m.chat.id
    text=m.text
    try:
        list_text=text.split("\n")
        brand=list_text[0]
        name=list_text[1]
        list_size=[]
        list_price=[]
        list_qty_stock=[]
        for i in list_text[2:]:
            i=i.split("@")
            list_size.append(i[0])
            list_price.append(i[1])
            list_qty_stock.append(i[2])
        mid=mid_new_product
        database.add_product(brand,name,list_size,list_price,list_qty_stock,mid)
        bot.send_message(cid,"اطلاعات ذخیره شد")
        userStep[cid]=0
    except:
        bot.send_message(cid,"لطفا اطلاعات را مانند نمونه ارسال کنید")
@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==15)
def name_custom(m):
    global new_size_product
    cid = m.chat.id
    text=m.text
    try:
        list_text=text.split("\n")
        list_size=[]
        list_price=[]
        list_qty_stock=[]
        for i in list_text:
            i=i.split("@")
            list_size.append(i[0])
            list_price.append(i[1])
            list_qty_stock.append(i[2])
        database.add_product(new_size_product["brand"],new_size_product["name"],list_size,list_price,list_qty_stock,new_size_product["code"])
        bot.send_message(cid,"اطلاعات ذخیره شد")
        userStep[cid]=0
    except:
        bot.send_message(cid,"لطفا اطلاعات را مانند نمونه ارسال کنید")
@bot.message_handler(content_types=["photo"])
def name_custom(m):
    global mid_new_product
    cid = m.chat.id
    mid = m.message_id
    if get_user_step(cid)==10:
        userStep[cid]=11
        info_pro=bot.copy_message(ch_id,cid,mid)
        mid_new_product=info_pro.message_id
        bot.send_message(cid,"لطفا در این مرحله نام , برند , سایز و قیمت محصول را مانند مثال ارسال کنید")
        bot.copy_message(cid,ch_id,14)
        
    if get_user_step(cid)==100:
        unblock(cid)
        checking(cid)
        if cid in block:
            return
        tracking_code=random.randint(100000,999999)
        list_shopp=database.use_shoppingcart_table_where(cid)
        shopping_cart_stop.setdefault(cid,{})
        shopping_cart_stop[cid].setdefault(tracking_code,[])
        for i in list_shopp:
            shopping_cart_stop[cid][tracking_code].append({"product_id":i["product_id"],"qty":i["qty"]})
        database.delete_shopping_cart_table_cid(cid)
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("تایید رسید",callback_data="admin_confirm"),InlineKeyboardButton("رد رسید",callback_data="admin_reject"))
        bot.copy_message(admin,cid,mid,reply_markup=markup,caption=f"{cid}**{tracking_code}")
        bot.send_message(admin,"وضعیت رسید را مشخص کنید")
        bot.send_message(cid,f"رسید شما برای تایید ارسال شد شماره پیگیری سفارش شما {tracking_code} است میتوتنید در بخش پیگیری سفارش سفارش خود را پیگیری کنید")
        # database.delete_shopping_cart_table()
        userStep[cid]=0


@bot.callback_query_handler(func=lambda call: call.data.startswith("new_size"))
def call_callback_data(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data=call.data.split("_")
    new_size_product["code"]=data[2]
    new_size_product["brand"]=data[3]
    new_size_product["name"]=data[4]
    bot.send_message(cid,f"""
محصول انتخاب شده
برند : {data[3]}
اسم محصول : {data[4]}
""")
    bot.copy_message(cid,ch_id,50)
    userStep[cid]=15


@bot.callback_query_handler(func=lambda call: call.data.startswith("show_the_deetails"))
def call_callback_data(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data=call.data
    code = data.split("_")[3]
    list_product=database.use_product_table_where(f"code={int(code)}")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("سایز ها و تعداد در انبار", callback_data="nothing"))
    brand=""
    name=""
    for i in list_product:
        brand=i["brand"]
        name=i["name"]
        markup.add(InlineKeyboardButton(f'سایز:{i["size"]}  تعداد:{i["qty_stock"]}', callback_data=f"changedqty_{code}_{i['size']}"))
    markup.add(InlineKeyboardButton("افزودن سایز جدید",callback_data=f"new_size_{code}_{brand}_{name}"))
    markup.add(InlineKeyboardButton("برگشت", callback_data=f"adback_{code}"))
    bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data.startswith("use_as_user"))
def call_callback_data(call):
    cid = call.message.chat.id
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("محصولات"))
    markup.add(KeyboardButton(" سبد خرید 🛒"), KeyboardButton(" حساب کاربری 👤"))
    markup.add(KeyboardButton("ارتباط با ما 📞"), KeyboardButton("سوابق خرید📝"))
    markup.add("برگشت به منو ادمین")
    bot.send_message(cid, "سلام به فروشگاه فورس خوش آمدید")
    bot.send_message(
        cid, "برای استفاده از ربات از گزینه های زیر استفاده کنید", reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data.startswith("wait"))
def call_callback_data(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")[1]
    code=call.data.split("_")[2]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("حذف",callback_data=f"all_delete_{code}"),InlineKeyboardButton("لغو",callback_data=f"all_back_{code}"))
    bot.edit_message_reply_markup(cid,mid,reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("all"))
def call_callback_data(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")[1]
    code=call.data.split("_")[2]
    if data=="delete":
        bot.delete_message(ch_id,code)
        database.delete_product_table_code(code)
        bot.delete_message(cid,mid)
        bot.answer_callback_query(call.id,"محصول حذف شد")
    elif data=="back":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("حذف سایز مشخص",callback_data=f"delsize_{code}"))
        markup.add(InlineKeyboardButton("حذف کامل محصول", callback_data=f"wait_delete_{code}"))
        bot.edit_message_reply_markup(cid,mid,reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("restart"))
def call_callback_data(call):
    cid = call.message.chat.id
    data = call.data.split("_")[1]
    if data=="cart":
        cart(call.message)
@bot.callback_query_handler(func=lambda call: call.data.startswith("delsize"))
def call_callback_data(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    if len(call.data.split("_"))==2:
        code = call.data.split("_")[1]
        list_product=database.use_product_table_where(f"code={int(code)}")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("سایز ها", callback_data="nothing"))
        for i in list_product:
            markup.add(InlineKeyboardButton(f"حذف سایز:{i['size']}", callback_data=f"delsize_{code}_{i['size']}"))
        markup.add(InlineKeyboardButton("برگشت",callback_data=f"delsize_back_{code}"))
        bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
    elif len(call.data.split("_"))==3:
        if call.data.split("_")[1]=="back":
            code = call.data.split("_")[2]
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("حذف سایز مشخص",callback_data=f"delsize_{code}"))
            markup.add(InlineKeyboardButton("حذف کامل محصول", callback_data=f"wait_delete_{code}"))
            bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
        else:
            code = call.data.split("_")[1]
            size=call.data.split("_")[2]
            database.delete_product_table_code_size(int(code),float(size))
            bot.answer_callback_query(call.id,f"محصول با کد {code} و سایز {size} حذف شد")
            list_product=database.use_product_table_where(f"code={int(code)}")
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("سایز ها", callback_data="nothing"))
            for i in list_product:
                markup.add(InlineKeyboardButton(f"حذف سایز:{i['size']}", callback_data=f"delsize_{code}_{i['size']}"))
            markup.add(InlineKeyboardButton("برگشت",callback_data=f"delsize_back_{code}"))
            bot.edit_message_reply_markup(cid,mid,reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("admin"))
def call_callback_data(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")[-1]
    if data =="delete":
        set_code=set()
        list_product=database.use_product_table()
        for i in list_product:
            set_code.add(i["code"])
        for i in set_code:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("حذف سایز مشخص",callback_data=f"delsize_{i}"))
            markup.add(InlineKeyboardButton("حذف کامل محصول", callback_data=f"wait_delete_{i}"))
            bot.copy_message(cid, -1002046803532, i,reply_markup=markup)
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("برگشت به منو ادمین")
        bot.send_message(cid,"برای حذف محصول مورد نظر از دکمه های زیر محصولات استفاده کنید",reply_markup=markup)
    elif data=="edit":
        set_code=set()
        list_product=database.use_product_table()
        for i in list_product:
            set_code.add(i["code"])
        for i in set_code:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("مشاهده جزئیات",callback_data=f"show_the_deetails_{i}"))
            mid_p=bot.copy_message(cid, -1002046803532, i,reply_markup=markup)
            edit_deerails_admin.setdefault(cid,{})
            edit_deerails_admin[cid].setdefault(i, {})
            edit_deerails_admin[cid][i]["mid"] = mid_p.message_id
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("برگشت به منو ادمین")
        bot.send_message(cid,"برای مشاهده و تغییر تعداد محصولات در انبار از دکمه های زیر هر محصول استفاده کنید",reply_markup=markup)
    elif data == "add":
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("برگشت به منو ادمین")
        bot.send_message(cid,"لطفا برای افزودن محصول عکس محصول و توضیحات آن را در کپشن عکس نوشته و ارسال کنید(مانند نمونه) ",reply_markup=markup)
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("نمونه ارسال پیام درست"))
        userStep[cid]=10
        bot.copy_message(int(cid),-1002046803532,5)
        userStep[cid]=10
    elif data =="confirm":
        uid=int(call.message.caption.split("**")[0])
        tracking_code=int(call.message.caption.split("**")[-1])
        database.insert_sales_table(uid,tracking_code)
        list_shop=shopping_cart_stop[uid][tracking_code]
        for i in list_shop:
            database.insert_sales_row_table(tracking_code,i["product_id"],i["qty"])
            qty_in_stock=database.use_product_table_where(f"product_id={i['product_id']}")[0]["qty_stock"]
            res=int(qty_in_stock)-int(i["qty"])
            database.update_product_table(i["product_id"],res)
        shopping_cart_stop[uid].pop(tracking_code)
        bot.send_message(uid,"رسید شما تایید شد ممنون از خرید شما میتوانید در بخش 'سوابق خرید' خرید خود را مشاهده کنید")
    elif data =="reject":
        uid=int(call.message.caption.split("**")[0])
        tracking_code=int(call.message.caption.split("**")[-1])
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("منوی اصلی "), KeyboardButton(" سبد خرید 🛒"))
        if cid==admin:
            markup.add("برگشت به منو ادمین")
        list_shop=shopping_cart_stop[uid][tracking_code]
        for i in list_shop:
            database.insert_shopping_cart_table(uid,i["product_id"],i["qty"])
        shopping_cart_stop[uid].pop(tracking_code)
        bot.send_message(uid,"رسیدی که شما ارسال کردید معتبر نمیباشد سفارش شما به سبد خریدتان بازگشت لطفا برای خرید به سبد خرید بروید و رسید معتبری ارسال کنید",reply_markup=markup)
    


@bot.callback_query_handler(func=lambda call: call.data.startswith("send_receipt"))
def call_callback_data(call):
    cid = call.message.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    mid = call.message.message_id
    bot.send_message(cid,"لطفا عکس رسید خود را به صورت واضح ارسال کنید")
    userStep[cid]=100

@bot.callback_query_handler(func=lambda call: call.data.startswith("shop_cart"))
def call_callback_data(call):
    cid = call.message.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    mid = call.message.message_id
    list_shoppingcart=database.use_shopping_cart_table_where(f"cid={cid}")
    price_total=0
    for b in list_shoppingcart:
        list_price=database.use_product_table_where(f"product_id={b['product_id']}")
        for i in list_price:
            price_total+=i["price"]*b["qty"]
    bot.delete_message(cid,mid)
    dict_info_user=database.use_customer_table_where(f"cid={cid}")
    if dict_info_user["phone"]!=None and dict_info_user["name"]!=None and dict_info_user["address"]!=None:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("ارسال رسید",callback_data="send_receipt"))
        bot.send_message(cid,f"""
    قیمت : {price_total}
    لطفا دقیقا مبلغ بالا را به شماره کارت زیر ارسال کنید و سپس با استفاده از دکمه زیر رسید خود را ارسال کنید
    شماره کارت : 00600606006006000600
    """,reply_markup=markup)
    else:
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(" حساب کاربری 👤")
        markup.add("منوی اصلی")
        if cid==admin:
            markup.add("برگشت به منو ادمین")
        bot.send_message(cid,"کاربر گرامی لطفا ابتدا در بخش 'حساب کاربری' اطلاعات خود را تکمیل کنید ",reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("cart"))
def call_callback_data(call):
    cid = call.message.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    mid = call.message.message_id
    data = call.data
    ch = data.split("_")[1]
    if ch == 'edit':
        alki, command, code, size, qty = data.split('_')
        list_product_id=database.use_product_table_where(f"code={code} and size={size}")
        for i in list_product_id:
            product_id=i["product_id"]
            qty_stock=i["qty_stock"]
        if int(qty)>int(qty_stock):
            bot.answer_callback_query(call.id,"متاسفانه از این محصول بیشتر از این تعداد در انبار وجود ندارد")
        else:
            list_shoppingcart=database.use_shopping_cart_table(cid,product_id)
            if len(list_shoppingcart)==0:
                database.insert_shopping_cart_table(cid,product_id,int(qty))
            else:
                database.update_shopping_cart_table(cid,product_id,int(qty))

            list_price=database.use_product_table_where(f"code={int(code)} and size={float(size)}")
            for i in list_price:
                # qty=database.use_shopping_cart_table_where(f"cid={cid} and product_id={i['product_id']}")[0]["qty"]
                bot.edit_message_caption(f"تعداد :'{qty}' با سایز '{size}' از این محصول. قیمت :{i['price']*int(qty)}",cid, mid, reply_markup=gen_cart_markup(code, size, int(qty)))

        # for i in list_price:
        #     bot.edit_message_caption(f"تعداد :'{qty}' با سایز '{size}' از این محصول. قیمت :{i['price']*shopping_cart[cid][code][size]}",cid, mid, reply_markup=gen_cart_markup(code, size, int(qty)))

        show_cart(cid)
    elif ch == 'delete':
        alki, command, code, size = data.split('_')
        product_id_j=database.use_product_table_where(f"code={int(code)} and size={float(size)}")[0]["product_id"]
        database.delete_shopping_cart_table(cid,product_id_j)
        bot.delete_message(cid, mid)
        show_cart(cid)
    elif ch == 'nothing':
        pass
    else:
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)


@bot.callback_query_handler(func=lambda call: call.data.startswith("size"))
def size_p(call):
    cid = call.message.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    mid = call.message.message_id
    data = call.data
    code = data.split("_")[1]
    list_product=database.use_product_table_where(f"code={int(code)}")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("سایز ها", callback_data="nothing"))
    for i in list_product:
        markup.add(InlineKeyboardButton(f'سایز:{i["size"]}  قیمت:{i["price"]}', callback_data=f"sele_{code}_{i['size']}"))
    markup.add(InlineKeyboardButton("برگشت", callback_data=f"delete_{code}"))
    if len(data.split("_")) == 3:
        bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
    else:
        bot.edit_message_reply_markup(
                    cid, products[cid][int(code)]["mid"], "سایز مورد نظر را انتخاب کنید", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("adback"))
def size_p(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")
    # bot.delete_message(cid, mid)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("مشاهده جزئیات",callback_data=f"show_the_deetails_{data[1]}"))
    bot.edit_message_reply_markup(cid,message_id=edit_deerails_admin[cid][int(data[1])]["mid"], reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data.startswith("delete"))
def size_p(call):
    cid = call.message.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    mid = call.message.message_id
    data = call.data.split("_")
    # bot.delete_message(cid, mid)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        "انتخاب سایز", callback_data=f"size_{data[1]}"))
    bot.edit_message_reply_markup(cid,message_id=products[cid][int(data[1])]["mid"], reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith("changedqty"))
def nmayesh(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    comm, code, size = data.split("_")
    list_product_id=database.use_product_table_where(f"code={code} and size={size}")
    for i in list_product_id:
        product_id=i["product_id"]
    qty_in_stock=database.use_product_table_where(f"product_id={product_id}")[0]["qty_stock"]
    markup = gen_product_markup_admin(code, size, qty_in_stock)
    bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data.startswith("sele"))
def nmayesh(call):
    cid = call.message.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    mid = call.message.message_id
    data = call.data
    comm, code, size = data.split("_")
    list_product_id=database.use_product_table_where(f"code={code} and size={size}")
    for i in list_product_id:
        product_id=i["product_id"]
    qty_in_stock=database.use_product_table_where(f"product_id={product_id}")[0]["qty_stock"]
    if qty_in_stock>0:
        list_shoppingcart=database.use_shopping_cart_table(cid,product_id)
        if len(list_shoppingcart)==0:
            qty=1
        else:
            for i in list_shoppingcart:
                qty=i["qty"]

        markup = gen_product_markup(code, size, qty)
        bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
    else:
        bot.answer_callback_query(call.id,"در حال حاضر این سایز محصول در انبار موجود نمیباشد")


@bot.callback_query_handler(func=lambda call: call.data.startswith("updqtystock"))
def call_callback_data(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    ch = data.split("_")[1]
    if ch == 'edit':
        alki, command, code, size, qty = data.split('_')
        bot.edit_message_reply_markup(cid, mid, reply_markup=gen_product_markup_admin(code, size, int(qty)))
    elif ch == 'nothing':
        pass
    elif ch == 'add':
        alki, command, code, size, qty = data.split('_')
        list_product_id=database.use_product_table_where(f"code={code} and size={size}")
        
        for i in list_product_id:
            product_id=i["product_id"]
            database.update_product_table(product_id,int(qty))
        bot.answer_callback_query(call.id, f'تعداد موجود در انبار آپدیت شد')
        markup2 = InlineKeyboardMarkup()
        markup2.add(InlineKeyboardButton("برگشت", callback_data=f"show_the_deetails_{code}"))
        bot.edit_message_reply_markup(cid, mid, reply_markup=markup2)
    else:
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)

@bot.callback_query_handler(func=lambda call: call.data.startswith("product"))
def call_callback_data(call):
    cid = call.message.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    mid = call.message.message_id
    data = call.data
    ch = data.split("_")[1]
    if ch == 'edit':
        alki, command, code, size, qty = data.split('_')
        list_product_id=database.use_product_table_where(f"code={code} and size={size}")
        for i in list_product_id:
            qty_stock=i["qty_stock"]
        if int(qty)>int(qty_stock):
            bot.answer_callback_query(call.id,"متاسفانه از این محصول بیشتر از این تعداد در انبار وجود ندارد")
        else:
            bot.edit_message_reply_markup(cid, mid, reply_markup=gen_product_markup(code, size, int(qty)))
        
    elif ch == 'nothing':
        pass
    elif ch == 'add':
        alki, command, code, size, qty = data.split('_')
        list_product_id=database.use_product_table_where(f"code={code} and size={size}")
        
        for i in list_product_id:
            product_id=i["product_id"]
            shopp_cart=database.use_shopping_cart_table(cid,product_id)
            if len(shopp_cart)==0:
                qty=int(qty)
                database.insert_shopping_cart_table(cid,product_id,qty)
            else:
                qty=int(qty)
                database.update_shopping_cart_table(cid,product_id,qty)

        bot.answer_callback_query(call.id, f'item added to basket')
        markup2 = InlineKeyboardMarkup()
        markup2.add(InlineKeyboardButton(
            "برگشت", callback_data=f"size_{code}_back"))
        bot.edit_message_reply_markup(cid, mid, reply_markup=markup2)
    else:
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)





@bot.callback_query_handler(func=lambda call: call.data.startswith("info_edit"))
def edite_infi_cust(call):
    cid = call.message.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    mid = call.message.message_id
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("منوی اصلی")
    if cid==admin:
        markup.add("برگشت به منو ادمین")
    bot.send_message(cid,"لطفا اطلاعات خود را به ترتیب خواسته شده وارد کنید.")
    bot.send_message(cid,'نام خود را وارد کنید:',reply_markup=markup)
    userStep[cid] = 1


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    userStep.setdefault(cid,0)
    database.create_one_customer(cid,"name",f"{m.from_user.first_name}")
    if cid == admin:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(" افزودن محصول جدید",callback_data="admin_add"), InlineKeyboardButton("حذف محصول",callback_data="admin_delete"))
        markup.add(InlineKeyboardButton("ویرایش محصولات",callback_data="admin_edit"))
        markup.add(InlineKeyboardButton("استفاده از ربات به عنوان کاربر",callback_data="use_as_user"))
        bot.send_message(cid,"سلام ادمین گرامی خوش آمدید برای استفاده از ربات از دکمه های زیر استفاده کنید",reply_markup=markup)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("محصولات"))
        markup.add(KeyboardButton(" سبد خرید 🛒"), KeyboardButton(" حساب کاربری 👤"))
        markup.add(KeyboardButton("ارتباط با ما 📞"), KeyboardButton("سوابق خرید📝"))
        if cid==admin:
            markup.add("برگشت به منو ادمین")
        bot.send_message(cid, "سلام به فروشگاه فورس خوش آمدید")
        bot.send_message(
            cid, "برای استفاده از ربات از گزینه های زیر استفاده کنید", reply_markup=markup)



@bot.message_handler(func=lambda m: m.text == "منوی اصلی")
def command_start(m):
    cid = m.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("محصولات"))
    markup.add(KeyboardButton(" سبد خرید 🛒"), KeyboardButton(" حساب کاربری 👤"))
    markup.add(KeyboardButton("ارتباط با ما 📞"), KeyboardButton("سوابق خرید📝"))
    if cid==admin:
        markup.add("برگشت به منو ادمین")
    # bot.send_message(cid, "سلام به فروشگاه فورس خوش آمدید")
    bot.send_message(
        cid, "جهت خرید یکی از گزینه های زیر را انتخاب کنید", reply_markup=markup)
    userStep.setdefault(cid,0)
    userStep[cid]=0


@bot.message_handler(func=lambda m: m.text=="ویرایش نام📝")
def name_custom_keyboard(m):
    cid = m.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    bot.send_message(cid,"نام خود را وارد کنید:")
    userStep[cid]=1


@bot.message_handler(func=lambda m: m.text=="وارد کردن ایمیل📧")
def phone_custom_keyboard(m):
    cid = m.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    bot.send_message(cid,"ایمیل خود را وارد کنید:")
    userStep[cid]=2


@bot.message_handler(func=lambda m: m.text=="وارد کردن آدرس🏘")
def phone_custom_keyboard(m):
    cid = m.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    bot.send_message(cid,"آدرس خود را وارد کنید:")
    userStep[cid]=3


@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==1)
def name_custom(m):
    cid = m.chat.id
    name=m.text
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    database.update_customer_table(cid,"name",m.text)
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("نمایش اطلاعات📝")
    markup.add("ویرایش نام📝")
    markup.add(KeyboardButton("وارد کردن شماره تلفن📞",request_contact=True))
    markup.add("وارد کردن ایمیل📧")
    markup.add("وارد کردن آدرس🏘")
    markup.add("منوی اصلی")
    if cid==admin:
        markup.add("برگشت به منو ادمین")
    bot.send_message(cid,"نام شما ذخیره شد✅",reply_markup=markup)
    userStep[cid]=0


@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==2)
def phone_custom(m):
    cid = m.chat.id
    phone=m.text
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    database.update_customer_table(cid,"email",m.text)
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("نمایش اطلاعات📝")
    markup.add("ویرایش نام📝")
    markup.add(KeyboardButton("وارد کردن شماره تلفن📞",request_contact=True))
    markup.add("وارد کردن ایمیل📧")
    markup.add("وارد کردن آدرس🏘")
    markup.add("منوی اصلی")
    if cid==admin:
        markup.add("برگشت به منو ادمین")
    bot.send_message(cid,"ایمیل شما ذخیره شد✅",reply_markup=markup)
    userStep[cid]=0

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==3)
def name_custom(m):
    cid = m.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    database.update_customer_table(cid,"address",m.text)
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("نمایش اطلاعات📝")
    markup.add("ویرایش نام📝")
    markup.add(KeyboardButton("وارد کردن شماره تلفن📞",request_contact=True))
    markup.add("وارد کردن ایمیل📧")
    markup.add("وارد کردن آدرس🏘")
    markup.add("منوی اصلی")
    if cid==admin:
        markup.add("برگشت به منو ادمین")
    bot.send_message(cid,"آدرس شما ذخیره شد✅",reply_markup=markup)
    userStep[cid]=0

 

@bot.message_handler(content_types=["contact"])
def address_custom(m):
    cid = m.chat.id
    phone=m.contact.phone_number
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    database.update_customer_table(cid,"phone",phone)
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("نمایش اطلاعات📝")
    markup.add("ویرایش نام📝")
    markup.add(KeyboardButton("وارد کردن شماره تلفن📞",request_contact=True))
    markup.add("وارد کردن ایمیل📧")
    markup.add("وارد کردن آدرس🏘")
    markup.add("منوی اصلی")
    if cid==admin:
        markup.add("برگشت به منو ادمین")
    bot.send_message(cid,"شماره تلفن شما ذخیره شد✅",reply_markup=markup)
    userStep[cid]=0




@bot.message_handler(func=lambda m: m.text == "نمایش اطلاعات📝")
def command_start(m):
    cid = m.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    dict_info=database.use_customer_table_where(f"cid={cid}")
    name=dict_info["name"]
    if name==None:
        name="❌"
    add=dict_info["address"]
    if add==None:
        add="❌"
    email=dict_info["email"]
    if email==None:
        email="❌"
    phone=dict_info["phone"]
    if phone==None:
        phone="❌"
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("ویرایش نام📝")
    markup.add(KeyboardButton("وارد کردن شماره تلفن📞",request_contact=True))
    markup.add("وارد کردن ایمیل📧")
    markup.add("وارد کردن آدرس🏘")
    markup.add("منوی اصلی") 
    if cid==admin:
        markup.add("برگشت به منو ادمین")   
    bot.send_message(cid,f"""
اطلاعات شما📝

* نام : {name}

* شماره تلفن : {phone}

ایمیل : {email}

* آدرس : {add}
""",reply_markup=markup)



@bot.message_handler(func=lambda m: m.text == "محصولات")
def product(m):
    cid = m.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    set_code=set()
    list_product=database.use_product_table()
    for i in list_product:
        set_code.add(i["code"])
    for i in set_code:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(
            "انتخاب سایز", callback_data=f"size_{i}"))
        mid = bot.copy_message(cid, -1002046803532, i,
                               reply_markup=markup)
        products.setdefault(cid,{})
        products[cid].setdefault(i, {})
        products[cid][i]["mid"] = mid.message_id
    markup2 = ReplyKeyboardMarkup(resize_keyboard=True)
    markup2.add(KeyboardButton("منوی اصلی "), KeyboardButton(" سبد خرید 🛒"))
    if cid==admin:
        markup2.add("برگشت به منو ادمین")
    bot.send_message(
        cid, "برای دسترسی به سبد خرید یا منوی اصلی از گزینه های پایین استفاده کنید.", reply_markup=markup2)


@bot.message_handler(func=lambda m: m.text == "سبد خرید 🛒")
def cart(m):
    global sssss
    cid = m.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    list_shoppingcart=database.use_shopping_cart_table_where(f"cid={cid}")
    if len(list_shoppingcart) == 0:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("منوی اصلی "))
        if cid==admin:
            markup.add("برگشت به منو ادمین")
        bot.send_message(cid, "سبد خرید شما خالی است", reply_markup=markup)
        return
    price_total=0
    update=False
    for b in list_shoppingcart:
        list_price=database.use_product_table_where(f"product_id={b['product_id']}")
        for i in list_price:
            if b["qty"]>i["qty_stock"]:
                update=True
                if i["qty_stock"]==0:
                    markup=InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton("❌",callback_data="ddddddd"))
                    bot.copy_message(cid, -1002046803532, i["code"], reply_markup=markup,caption="""متاسفانه در حال حاضر این محصول در انبار وجود ندارد و از سبد خرید شما حذف شد""")
                    product_id_j=database.use_product_table_where(f"code={i['code']} and size={i['size']}")[0]["product_id"]
                    database.delete_shopping_cart_table(cid,product_id_j)
                else:
                    bot.copy_message(cid, -1002046803532, i["code"], reply_markup=gen_cart_markup(str(i["code"]), str(i["size"]), i["qty_stock"]),caption=f"""
از این محصول با سایز : {i["size"]}
شما تعداد {b["qty"]} از این محصول را در سبد خرید خود ذخیره کرده بودید اما در حال حاضر فقط {i["qty_stock"]} عدد از این محصول در انبار وجود دارد
""")
                    price_total+=i["price"]*i["qty_stock"]
                    database.update_shopping_cart_table(cid,b['product_id'],int(i["qty_stock"]))
            else:    
                bot.copy_message(cid, -1002046803532, i["code"], reply_markup=gen_cart_markup(str(i["code"]), str(i["size"]), b["qty"]),caption=f"""تعداد :'{b["qty"]}' با سایز '{i["size"]}' از این محصول. قیمت:{i['price']*b["qty"]}""")
                price_total+=i["price"]*b["qty"]


    markup2 = InlineKeyboardMarkup()
    if update:
        markup2.add(InlineKeyboardButton("آپدیت سبد خرید",callback_data="restart_cart"))
    markup2.add(InlineKeyboardButton("خرید و ثبت نهایی", callback_data="shop_cart"))
    ee = bot.send_message(cid, f"قیمت کل سبد خرید شما برابر است با :{price_total}", reply_markup=markup2)
    sssss = int(ee.message_id)
    markup3 = ReplyKeyboardMarkup(resize_keyboard=True)
    markup3.add(KeyboardButton("منوی اصلی "))
    if cid==admin:
        markup3.add("برگشت به منو ادمین")
    bot.send_message(
        cid, 'برای بازگشت به منو اصلی از گزینه پایین استفاده کنید', reply_markup=markup3)


@bot.message_handler(func=lambda m: m.text == "ارتباط با ما 📞")
def contact_us(m):
    cid = m.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    bot.copy_message(cid, -1002046803532, 8)

@bot.message_handler(func=lambda m: m.text == "سوابق خرید📝")
def records(m):
    cid = m.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    conf=True
    text=""
    if cid in shopping_cart_stop:
        list_awaiting_confirm=shopping_cart_stop[cid]
        if len(list_awaiting_confirm)>0:
            conf=False
            text+="محصولات در انتظار تایید رسید\n"
            for i in list_awaiting_confirm:
                text+=f"سفارش {i}\n"
                price_total=0
                for b in shopping_cart_stop[cid][i]:
                    dict_pro=database.use_product_table_where(f"product_id={b['product_id']}")[0]
                    price_total+=b['qty']*dict_pro["price"]
                    text+=f"""
       >اسم محصول : {dict_pro["name"]}
       >برند : {dict_pro["brand"]}
       >فی : {dict_pro["price"]}
       >تعداد : {b['qty']}
       >قیمت : {b['qty']*dict_pro["price"]}
    ***********************
    """
                text+=f"""
    قیمت کل سفارش {i} : {price_total}
    ###########################

    """
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton("منوی اصلی "))
            if cid==admin:
                markup.add("برگشت به منو ادمین")
            bot.send_message(cid,text,reply_markup=markup)
    text=""
    list_time_sales_row=database.use_sales_table(cid)
    if len(list_time_sales_row)!=0:
        conf=False
        text+="محصولات خریداری شده\n"
        for i in list_time_sales_row:
            text+=f"سفارش {i['inv_id']}\n"
            list_sales_row=database.use_sales_row_table(i["inv_id"])
            price_total=0
            for b in list_sales_row:
                dict_pro=database.use_product_table_where(f"product_id={b['product_id']}")[0]
                price_total+=b['qty']*dict_pro["price"]
                text+=f"""
   >اسم محصول : {dict_pro["name"]}
   >برند : {dict_pro["brand"]}
   >فی : {dict_pro["price"]}
   >تعداد : {b['qty']}
   >قیمت : {b['qty']*dict_pro["price"]}
* * * * * * * * * * * *

"""
            text+=f"""
قیمت کل سفارش {i["inv_id"]} : {price_total}
############################

"""
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("منوی اصلی "))
        if cid==admin:
            markup.add("برگشت به منو ادمین")
        bot.send_message(cid,text,reply_markup=markup)
    if conf:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("منوی اصلی "))
        if cid==admin:
            markup.add("برگشت به منو ادمین")
        bot.send_message(cid,"شما هنوز سفارشی ثبت نکرده اید",reply_markup=markup)
    



    

@bot.message_handler(func=lambda m: m.text == "حساب کاربری 👤")
def contact_us(m):
    cid = m.chat.id
    unblock(cid)
    checking(cid)
    if cid in block:
        return
    markup=InlineKeyboardMarkup()
    if database.use_customer_table_where(f"cid={cid}")==None:
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("ویرایش نام📝")
        markup.add(KeyboardButton("وارد کردن شماره تلفن📞",request_contact=True))
        markup.add("وارد کردن ایمیل📧")
        markup.add("وارد کردن آدرس🏘")
        markup.add("منوی اصلی")
        if cid==admin:
            markup.add("برگشت به منو ادمین")
        bot.send_message(cid,f"""
اطلاعات شما📝

* نام : {m.from_user.first_name}

* شماره تلفن : ❌

ایمیل : ❌

* آدرس : ❌
""",reply_markup=markup)
        bot.send_message(cid,"برای خرید لطفا فیلد های ستاره دار را پر کنید")
        database.create_one_customer(cid,"name",f"{m.from_user.first_name}")
        
    else:
        dict_info=database.use_customer_table_where(f"cid={cid}")
        name=dict_info["name"]
        if name==None:
            name="❌"
        add=dict_info["address"]
        if add==None:
            add="❌"
        email=dict_info["email"]
        if email==None:
            email="❌"
        phone=dict_info["phone"]
        if phone==None:
            phone="❌"
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("ویرایش نام📝")
        markup.add(KeyboardButton("وارد کردن شماره تلفن📞",request_contact=True))
        markup.add("وارد کردن ایمیل📧")
        markup.add("وارد کردن آدرس🏘")
        markup.add("منوی اصلی")
        if cid==admin:
            markup.add("برگشت به منو ادمین")
        bot.send_message(cid,f"""
اطلاعات شما📝

* نام : {name}

* شماره تلفن : {phone}

ایمیل : {email}

* آدرس : {add}
""",reply_markup=markup)



@bot.message_handler(func=lambda m: True)
def product(m):
    cid = m.chat.id
    # bot.send_message(cid, "مقدار وارد شده نامعتبر است ")


bot.infinity_polling()

from flask import Flask, render_template, request, session, redirect, url_for, make_response
from flask_mail import Mail, Message
import pymysql
import re
import datetime

app = Flask(__name__)
app.secret_key = 'random string'

db = pymysql.connect(host="localhost", user="root", password="", database="FYP_booking", port=8081) 

# App Settings
app.config['threaded'] = True

# Enter your email server details below, the following details uses the gmail smtp server (requires gmail account)
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'testtc399565@gmail.com'
app.config['MAIL_PASSWORD'] = 'test12345!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Intialize Mail
mail = Mail(app)


@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM product WHERE status = 'on sale'")
    item = cursor.fetchall()
    cursor.execute("SELECT * FROM service")
    service = cursor.fetchall()
    return render_template('index.html', item=item, service=service)

@app.route('/message', methods=['GET', 'POST'])
def message():
    # Output message & error if something goes wrong or successful
    success = ''
    error = ''
    # message submitted form 
    if request.method == 'POST':
        # Create variables for easy access
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        cursor = db.cursor()
        # insert new message into message table
        cursor.execute("insert into message (name, email, subject, mes_body) values ('{0}', '{1}', '{2}', '{3}')".format(name, email, subject, message))
        try:
            db.commit()
            # check if data is successful entry into message table output the message
            success = "Your message was sended !"
        except Exception as e:
            # check if data is failed entry into message table data will roll bacj and output the error
            db.rollback()
            error = "I am sorry! Some error occurs! Please try again"
    return render_template("contact_form.html", error=error , success = success)
    db.close()


#-------------------------------------Start of Login & Register-------------------------------------------#
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        user = cursor.fetchone()
        # If account exists in accounts table in out database
        if user:
            #Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = username
            session['email']=  user[3]
            return redirect(url_for("service"))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    success=''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cpassword = request.form['cpassword']
        # Check if account exists using MySQL
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username))
        user = cursor.fetchone()
        # If account exists show error and validation checks
        if user:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            return 'Username must contain only characters or numbers!'
        elif not username or not password or not email:
            return 'Please fill out the form!'
        elif cpassword != password:
            msg = 'password is not match!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)', (username, password, email))
            db.commit()
            email_info = Message('Elderly Service Care --- Account Registered!', sender = 'testtc399565@gmail.com', recipients = [email])
            # change the email body below
            email_info.body = 'Congratulation!!! You have successfully registered an account! After Login remember go to profile page to update the personal information!!!'
            mail.send(email_info)
            success = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        return 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg, success=success)
    db.close()
#---------------------------------------End of Login & Register-------------------------------------------#

#-------------------------------------Start of service booking--------------------------------------------#
@app.route('/service')
def service():
    # the user go to this page must after login
    if 'username' in session:
        cursor = db.cursor()
        # get all the data form service table
        cursor.execute("SELECT * FROM service")
        # Fetch records and return result to the page
        data = cursor.fetchall()
        return render_template('service.html' , data=data)
    else:
        # if user is not logged in will turn back to login page
        return redirect(url_for('login'))

@app.route('/servicebooking')
def servicebooking():
    # get the service id for easy to access
    serviceId = request.args.get('serviceId')
    cursor = db.cursor()
    # get the data with same service id 
    cursor.execute("SELECT * FROM service WHERE service_id = '{0}'" .format(serviceId))
    # Fetch service data and return result to the page
    serviceData = cursor.fetchall()
    return render_template("booking.html", serviceData = serviceData)
    db.close()

@app.route('/booking_form')
def serviceform():
    
    if 'username' in session:
        # get the service id for easy to access
        serviceId = request.args.get('serviceId')
        username = session['username']
        now = datetime.date.today()
        cursor = db.cursor()
        # get the data from service and users table
        cursor.execute("SELECT a.service_id, a.service_name, a.service_image, b.FirstName, b.LastName, b.address, b.email, b.phone, b.username FROM service a, users b WHERE a.service_id = '{0}' and b.username = '{1}'" .format(serviceId, username))
        # Fetch service & users data and return result to the page
        serviceData = cursor.fetchall()
        return render_template("booking_form.html", serviceData = serviceData , now=now)
        db.close()
    else:
        return redirect(url_for('login'))

@app.route('/servicebooked', methods=['GET', 'POST'])
def servicebooked():
    # Output message & error if something goes wrong...
    error = ''
    success = ''
    # booking service submitted form
    if request.method == 'POST':
        # Create variables for easy access
        serviceId = request.form['serviceId']
        Name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        service = request.form['service']
        bookingdate = request.form['date']
        bookingtime = request.form['time']
        username = session['username']

        cursor = db.cursor()
        cursor.execute("insert into reservation (email, username, fullname, service_name, address, phone, date, time, service_id) values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}','{8}')".format(email, username, Name, service, address, phone, bookingdate, bookingtime, serviceId))

        try:
            db.commit()
            email_info = Message('Elderly Service Care --- Booking record!', sender = 'testtc399565@gmail.com', recipients = [email])
            # change the email body below
            email_info.body = "Your booking is successfully booked! Here is your booking '" + request.form.get('service') + "' time--'" + request.form.get('time') + "'& date--'"+ request.form.get('date') +"' "
            mail.send(email_info)
            success = "Your booking is successfully booked !"
        except Exception as e:
            db.rollback()
            error = "I am sorry! Your booking have some error occurs! Please try again"
    return render_template("bookingconfilm.html", error=error , success = success)
    db.close()

@app.route('/bookingconfilm')
def bookingconfilm():
    if 'username' in session:
        return render_template('bookingconfilm.html')
    else:
        return redirect(url_for('login'))
#-------------------------------------End of service booking----------------------------------------------#
#-------------------------------------Start of shopping system--------------------------------------------#
@app.route('/groceries')
def groceries():
    if 'username' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM product")
        data = cursor.fetchall()
        return render_template('groceries.html', data = data)
    else:
        return redirect(url_for('login'))

@app.route('/product')
def product():
    P_ID = request.args.get('P_ID')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM product WHERE product_id = '{0}'".format(P_ID))
    data = cursor.fetchall()
    return render_template('product.html', data = data)

@app.route('/shoppingCart')
def shoppingCart():
    if 'username' in session:
        cursor = db.cursor()
        cursor.execute("SELECT a.cart_id, b.name, b.image, b.price FROM cart a, product b where a.product_id = b.product_id and a.username = '" + session['username'] + "' ORDER BY a.cart_id  ")
        data = cursor.fetchall()
        totalPrice = 0
        for row in data:
            totalPrice += int(row[3])
        return render_template('shoppingCart.html', data = data, totalPrice = totalPrice)
    else:
        return redirect(url_for('login'))

@app.route('/checkout')
def checkout():
    if 'username' in session:
        cursor = db.cursor()
        cursor.execute("SELECT a.cart_id, a.product_id, b.product_id ,b.name, b.image, b.price FROM cart a, product b where a.product_id = b.product_id and a.username = '" + session['username'] + "' ORDER BY a.cart_id  ")
        order = cursor.fetchall()
        totalPrice = 0
        now = datetime.date.today()
        for row in order:
            totalPrice += int(row[5])
        return render_template('checkout.html', order = order, totalPrice= totalPrice, now=now)
    else:
        return redirect(url_for('login'))

@app.route('/place_order', methods=["GET", "POST"])
def place_order():
    msg = ''
    if request.method == "POST":
        date = request.form['date']
        totalprice = request.form['totalprice']
        username = session['username']
        
        cursor = db.cursor()
        sql = ("insert into orders (username, dates, totalprice, status) VALUES ('{0}', '{1}', '{2}', 'unpayed')".format(username, date, totalprice))      
        cursor.execute(sql)
        try:
            db.commit()
            msg = "order successfully"
        except:
            db.rollback()
            msg = "Error occured"
    return redirect(url_for('payment', msg = msg))
    db.close()        
    
@app.route('/pay_cancle')
def pay_cancle():
    if 'username' in session:
        O_ID = request.args.get('O_ID')
        cursor = db.cursor()
        try:
            sql = ("DELETE FROM orders WHERE order_id = '{0}'" .format(O_ID))
            cursor.execute(sql)
            db.commit()
            msg = "payment cancle"
        except:
            db.rollback()
            msg = "cancle faile"
        return redirect(url_for('shoppingCart', msg=msg))
        cursor.close()
    else:
        return redirect(url_for('login'))

@app.route('/payment')
def payment():
    if 'username' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM orders WHERE status = 'unpayed' and username = '" + session['username'] + "'")
        data = cursor.fetchall()
        return render_template('payment.html', data=data)  
    else:    
        return redirect(url_for('login'))

@app.route('/paycompleted', methods=["GET", "POST"])
def paycompleted():
    msg = ''
    if request.method == "POST":
        order_id = request.form['order_id']
        C_No = request.form['card-number']
        CCV = request.form['card-ccv']
        holder = request.form['card-holder']
        totalprice = request.form['totalprice']
        username = session['username']
        
        cursor = db.cursor()
        sql = ("insert into payment (card_holder, c_no, ccv, totalprice, order_id) VALUES ('{0}', AES_ENCRYPT('{1}','secretcode'), AES_ENCRYPT('{2}','secretcode'), '{3}', '{4}')".format(holder, C_No, CCV, totalprice, order_id))      
        cursor.execute(sql)
        sql_1 =("UPDATE order_detail SET order_id = '{0}' WHERE username = '{1}' and status = 'unpayed'".format(order_id, username))
        cursor.execute(sql_1)
        sql_3 =("UPDATE order_detail SET status = 'Payment Completed' WHERE status = 'unpayed'")
        cursor.execute(sql_3)
        sql_2 = ("UPDATE orders SET status = 'Payment Completed' WHERE username = '{0}'".format(username))
        cursor.execute(sql_2)
        sql_4 =("DELETE FROM cart WHERE username = '{0}'".format(username))
        cursor.execute(sql_4)
        try:
            db.commit()
            msg = "order successfully"
        except:
            db.rollback()
            msg = "Error occured"
    return redirect(url_for('order', msg = msg))
    db.close()        


@app.route('/addtocart')
def addtocart():
    msg = ''
    if 'username' in session:
        P_ID = request.args.get('P_ID')
        username = session['username']
        cursor = db.cursor()
        try:
            sql = ("INSERT INTO cart (username, product_id) VALUES ('{0}', '{1}')".format(username, P_ID))      
            cursor.execute(sql)
            sql_1 = ("INSERT INTO order_detail (username, product_id, status) VALUES ('{0}', '{1}', 'unpayed')".format(username, P_ID))
            cursor.execute(sql_1)
            db.commit()
            msg = "Added successfully"
        except:
            db.rollback()
            msg = "Error occured"
        cursor.close()        
    return redirect(url_for('shoppingCart', msg = msg))

@app.route('/removefromcart')
def removefromcart():
    if 'username' in session:
        C_ID = request.args.get('C_ID')
        cursor = db.cursor()
        try:
            sql = ("DELETE FROM cart WHERE cart_id = '{0}'" .format(C_ID))
            cursor.execute(sql)
            sql_1 = ("DELETE FROM order_detail WHERE od_id = '{0}'" .format(C_ID))
            cursor.execute(sql_1)
            db.commit()
            msg = "removed successfully"
        except:
            db.rollback()
            msg = "error occured"
    cursor.close()
    return redirect(url_for('shoppingCart', msg= msg))

    
#-------------------------------------End of shopping system--------------------------------------------#

#-------------------------------------Start of personal information-------------------------------------#
@app.route('/profile')
def profile():
    if 'username' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = '" + session['username'] + "'")
        profileData = cursor.fetchone()
        return render_template("profile.html", profileData=profileData)
    return redirect(url_for('login'))

@app.route('/profile/update', methods=["GET", "POST"])
def profile_update():
    msg = ''
    if request.method == 'POST':
       
        firstName = request.form['FirstName']
        lastName = request.form['LastName']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        username = session['username']
                
        cur = db.cursor()
        cur.execute("""UPDATE users SET FirstName = '{0}', LastName = '{1}', address = '{2}', email = '{3}', phone = '{4}', gender = '{5}' WHERE username = '{6}'""".format(firstName, lastName, address, email, phone, gender, username))

        try:
            db.commit()
            msg = "Saved Successfully"
        except:
            db.rollback()
            msg = "Error occured"
        
    return redirect(url_for('profile', msg = msg))
    db.close()

@app.route('/changepassword', methods=["GET", "POST"])
def changepassword():
    msg=''
    error=''
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        newPassword = request.form['newpassword']
        
        cursor = db.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = '" + session['username'] + "'")
        user_id, password = cursor.fetchone()
        if (password == oldPassword):
            try:
                cursor.execute("UPDATE users SET password = '{0}' WHERE id = '{1}'".format(newPassword, user_id))
                db.commit()
                msg="Changed successfully"
            except:
                db.rollback()
                error = "Failed"
            return render_template("changepassword.html", msg=msg)
        else:
            error = "Wrong password"
        
    return render_template("changepassword.html", msg=msg, error=error) 
    db.close()

@app.route('/booking_record')
def booking_record():
    if 'username' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM reservation WHERE username = '" + session['username'] + "'")
        record = cursor.fetchall()
        return render_template('booking_record.html', record = record)
    else:
        return redirect(url_for('login'))

@app.route('/booking_edit', methods=['GET', 'POST'])
def booking_edit():
    if 'username' in session:
        B_ID = request.args.get('B_ID')
        now = datetime.date.today()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM reservation WHERE reser_id = '{0}'".format(B_ID))
        record = cursor.fetchall()
        msg = ''
        error=''
        if request.method == 'POST':
            id = request.form['id']
            name = request.form['name']
            address = request.form['address']
            email = request.form['email']
            phone = request.form['phone']
            service = request.form['service']
            date = request.form['date']
            time = request.form['time']
                    
            cursor = db.cursor()
            cursor.execute("""UPDATE reservation SET fullname = '{0}', address = '{1}', email = '{2}', phone = '{3}', service_name = '{4}', date = '{5}', time = '{6}'WHERE reser_id = '{7}'""".format(name, address, email, phone, service, date, time, id))

            try:
                db.commit()
                msg = "Saved Successfully"
            except:
                db.rollback()
                error = "Error occured"
        return render_template("booking_edit.html", record=record, msg=msg, error=error, now=now)
        db.close()
    else:
        return redirect(url_for('login'))

@app.route('/booking_delete', methods=['post'])
def booking_delete():
    B_ID = request.args.get('B_ID')
    cursor = db.cursor()
    cursor.execute("DELETE FROM reservation WHERE reser_id = '{0}'".format(B_ID))
    db.commit() 
    cursor.close()
    return redirect(url_for('booking_record'))

@app.route('/order')
def order():
    if 'username' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM orders WHERE username = '" + session['username'] + "'")
        orders = cursor.fetchall()
        return render_template('orders.html', orders=orders)
    else:
        return redirect(url_for('login'))

@app.route('/order_detail')
def order_detail():
    msg=''
    if 'username' in session:
        invoice = request.args.get('invoice')
        cursor = db.cursor()
        sql = ("SELECT a.order_id, b.od_id, b.product_id, c.name, c.image, c.price FROM orders a, order_detail b, product c WHERE b.order_id = a.order_id and b.product_id = c.product_id and a.order_id = '{0}'".format(invoice))
        cursor.execute(sql)
        detail = cursor.fetchall()
        sql1 = ("SELECT a.order_id, a.totalprice, a.dates, a.username, b.email, b.address FROM orders a, users b WHERE a.username = b.username and a.order_id ='{0}'".format(invoice))
        cursor.execute(sql1)
        orders = cursor.fetchone()
        try:          
            db.commit()
            msg = "successfully"
        except:
            db.rollback()
            msg = "error occured"
        return render_template('order_detail.html', msg=msg, detail=detail, orders=orders)
        cursor.close()
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('index'))
#-------------------------------------End of personal information-----------------------------------------#

#-------------------------------------------------Admin Section ------------------------------------------#

@app.route('/admin_login', methods=["GET", "POST"])
def admin_login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = db.cursor()
        cursor.execute("SELECT * FROM admin WHERE admin_email = '{0}' AND admin_password = '{1}'".format(email, password))
        # Fetch one record and return result
        user = cursor.fetchone()
        # If account exists in accounts table in out database
        if user:
            #Create session data, we can access this data in other routes
            session['adminlogin'] = True
            session['adminemail'] = email
            return redirect(url_for("admin"))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('admin_login.html', msg=msg)

@app.route('/admin_logout')
def admin_logout():
    session.pop('adminlogin', None)
    session.pop('adminemail', None)
    return render_template('admin_login.html')

@app.route('/admin')
def admin():
    if 'adminlogin' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM order_detail")
        record = cursor.fetchall()
        cursor.execute("SELECT * FROM cart")
        cart = cursor.fetchall()
        cursor.execute("SELECT SUM(totalprice) FROM orders")
        balance = cursor.fetchone()
        cursor.execute("SELECT COUNT(id) FROM users")
        user = cursor.fetchone()
        cursor.execute("SELECT COUNT(reser_id) FROM reservation")
        booking = cursor.fetchone()
        return render_template('admin.html', record=record, balance=balance, user=user, booking=booking, cart=cart)
    else:
        return redirect(url_for('admin_login'))
#-------------------------------------------------Admin Section ------------------------------------------#
@app.route('/admin_booking')
def admin_booking():
    if 'adminlogin' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM reservation")
        booking = cursor.fetchall()
        return render_template('admin_booking.html', booking=booking)
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin_booking_delete', methods=['post'])
def admin_booking_delete():
    bookingId = request.args.get('bookingId')
    cursor = db.cursor()
    cursor.execute("DELETE FROM reservation WHERE reser_id = '{0}'".format(bookingId))
    db.commit() 
    cursor.close()
    return redirect(url_for('admin_booking'))
#-------------------------------------------------Admin Section ------------------------------------------#
@app.route('/admin_groceries')
def admin_groceries():
    if 'adminlogin' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM product")
        product = cursor.fetchall()
        return render_template('admin_groceries.html', product=product)
    else:
        return redirect(url_for('admin_login'))

@app.route('/delete_product', methods=['post'])
def delete_product():
    productId = request.args.get('productId')
    cursor = db.cursor()
    cursor.execute("DELETE FROM product WHERE product_id = '{0}'".format(productId))
    db.commit()  
    cursor.close()
    return redirect(url_for('admin_groceries'))

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'adminlogin' in session:
        msg = ''
        if request.method == 'POST':
            name = request.form['name']
            image = request.form['image']
            price = request.form['price']
            stock = request.form['stock']
            description = request.form['description']
            status = request.form['status']

            cursor = db.cursor()
            cursor.execute("insert into product (name, image, price, stock, description, status) values ('{0}', '{1}', '{2}', '{3}','{4}','{5}')".format(name, image, price, stock, description, status))
            try:
                db.commit()
                msg = "Saved Successfully"
            except:
                db.rollback()
                msg = "Error occured"   
        
        return render_template('admin_addproduct.html', msg=msg)
        cursor.close() 
    else:
        return redirect(url_for('admin_login'))

@app.route('/product_edit')
def product_edit():
    if 'adminlogin' in session:
        productId = request.args.get('productId')
    
        cursor = db.cursor()
        cursor.execute("SELECT * FROM product WHERE product_id = '{0}'".format(productId))
        data = cursor.fetchall()
        return render_template("admin_editproduct.html", data=data)
    else:
        return redirect(url_for('admin_login'))

@app.route('/product_update', methods=["POST", "GET"])
def product_update():
    msg = ''
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        image = request.form['image']
        price = request.form['price']
        stock = request.form['stock']
        description = request.form['description']
        status = request.form['status']

        cursor = db.cursor()
        cursor.execute("UPDATE product SET name= '{0}', image='{1}', price='{2}', stock='{3}', description='{4}', status='{5}' WHERE product_id = '{6}'".format(name, image, price, stock, description, status, id))
        try:
            db.commit()
            msg = "Saved Successfully"
        except:
            db.rollback()
            msg = "Error occured"    
    return redirect(url_for('admin_groceries', msg = msg))
    db.close()
#-------------------------------------------------Admin Section ------------------------------------------#
@app.route('/admin_order')
def admin_order():
    if 'adminlogin' in session:
        cursor = db.cursor()
        cursor.execute("SELECT a.order_id, a.username, a.dates, a.totalprice, a.status, a.shipping_status, b.email FROM orders a, users b Where a.username = b.username")
        orders = cursor.fetchall()
        return render_template('admin_order.html', orders=orders)
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin_order_detail')
def admin_order_detail():
    if 'adminlogin' in session:
        orderId = request.args.get('orderId')
        cursor = db.cursor()
        cursor.execute("SELECT a.order_id, b.od_id, b.product_id, c.name, c.image, c.price FROM orders a, order_detail b, product c WHERE b.order_id = a.order_id and b.product_id = c.product_id and a.order_id = '{0}'".format(orderId))
        detail = cursor.fetchall()
        return render_template('admin_orderdetail.html', detail=detail)
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin_order_update', methods=['GET', 'POST'])
def admin_order_update():
    if 'adminlogin' in session:
        msg=''
        if request.method == 'POST':
            orderId = request.args.get('orderId')
            shipping = request.form['shipping']
            email = request.form['email']
            cursor = db.cursor()
            cursor.execute("UPDATE orders SET shipping_status='{0}' WHERE order_id = '{1}'".format(shipping, orderId))
            try:
                db.commit()
                email_info = Message('Elderly Service Care --- Shipping', sender = 'testtc399565@gmail.com', recipients = [email])
                # change the email body below
                email_info.body = "Your order is '" + request.form.get('shipping') + "'!!!  You can check it on your order record page."
                mail.send(email_info)
                msg = "Saved Successfully"
            except:
                db.rollback()
                msg = "Error occured" 
        return redirect(url_for('admin_order', msg=msg))
        cursor.close()
    else:
        return redirect(url_for('admin_login'))

@app.route('/delete_order', methods=['post'])
def delete_order():
    orderId = request.args.get('orderId')
    cursor = db.cursor()
    cursor.execute("DELETE FROM orders WHERE order_id = '{0}'".format(orderId))
    cursor.execute("DELETE FROM order_detail WHERE order_id = '{0}'".format(orderId))
    db.commit()
    cursor.close()
    return redirect(url_for('admin_order'))
#-------------------------------------------------Admin Section ------------------------------------------#
@app.route('/admin_user')
def admin_user():
    if 'adminlogin' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        user = cursor.fetchall()
        cursor.execute("SELECT * FROM admin")
        admin = cursor.fetchall()
        return render_template('admin_user.html', user=user, admin=admin)
    else:
        return redirect(url_for('admin_login'))

@app.route('/delete_user', methods=['post'])
def delete_user():
    userId = request.args.get('userId')
    cursor = db.cursor()
    sql = ("DELETE FROM users WHERE id = '{0}'".format(userId))
    cursor.execute(sql)
    db.commit()
    cursor.close()
    return redirect(url_for('admin_user'))
#-------------------------------------------------Admin Section ------------------------------------------#
@app.route('/admin_service')
def admin_service():
    if 'adminlogin' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM service")
        service = cursor.fetchall()
        return render_template('admin_service.html', service=service)
    else:
        return redirect(url_for('admin_login'))

@app.route('/delete_service', methods=['post'])
def delete_service():
    serviceId = request.args.get('serviceId')
    cursor = db.cursor()
    cursor.execute("DELETE FROM service WHERE service_id = '{0}'".format(serviceId ))
    db.commit()
    cursor.close()
    return redirect(url_for('admin_service'))

@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    if 'adminlogin' in session:
        msg = ''
        if request.method == 'POST':
            name = request.form['name']
            image = request.form['image']
            description = request.form['description']
            detail = request.form['detail']
            cursor = db.cursor()
            try:
                
                cursor.execute("insert into service (service_name, service_image, description, service_detail) values ('{0}','{1}','{2}','{3}')".format(name, image, description, detail))
                db.commit()
                msg = "Saved Successfully"
            except:
                db.rollback()
                msg = "Error occured"
        
        return render_template('admin_addservice.html',msg=msg)
        cursor.close()
    return redirect(url_for('admin_login'))

@app.route('/service_edit')
def service_edit():
    if 'adminlogin' in session:
        serviceId = request.args.get('serviceId')
    
        cursor = db.cursor()
        cursor.execute("SELECT * FROM service WHERE service_id = '{0}'".format(serviceId))
        data = cursor.fetchall()
        return render_template("admin_editservice.html", data=data)
    else:
        return redirect(url_for('adminlogin'))

@app.route('/service_update', methods=["POST", "GET"])
def service_update():
    msg = ''
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        image = request.form['image']
        description = request.form['description']
        detail = request.form['detail']

        cursor = db.cursor()
        cursor.execute("UPDATE service SET service_name= '{0}', service_image= '{1}', description= '{2}', service_detail= '{3}' WHERE service_id = '{4}'".format(name, image, description, detail, id))
        try:
            db.commit()
            msg = "Saved Successfully"
        except:
            db.rollback()
            msg = "Error occured" 
    return redirect(url_for('admin_service', msg = msg))
    db.close()
###########################################################################################
@app.route('/admin_message')
def admin_message():
    if 'adminlogin' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM message")
        data =cursor.fetchall()
        return render_template('admin_message.html', data=data)
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin_payment')
def admin_payment():
    if 'adminlogin' in session:
        cursor = db.cursor()
        cursor.execute("SELECT pay_id, order_id, c_no, card_holder, totalprice from payment")
        data =cursor.fetchall()
        return render_template('admin_payment.html', data=data)
    else:
        return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug= True)

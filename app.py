#Aidan Martin
from flask import *
import flask_login
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, DecimalField, IntegerField, RadioField
from wtforms.validators import InputRequired, Length
from werkzeug.datastructures import CombinedMultiDict, ImmutableOrderedMultiDict
import sqlite3          #libraries
from datetime import date,datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'wxyzthisisAsecretqbf'
app.config['ENV'] = True
app.config['UPLOAD_FOLDER'] = "static/images/"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'test@gmail.com': {'password': 'pw123'}}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return
    user = User()
    user.id = email
    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']
    return user

#forms
class SubscriberForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])

class ContactForm(FlaskForm):
    fname = StringField('c_f_name', validators=[InputRequired()])
    lname = StringField('c_l_name', validators=[InputRequired()])
    email = StringField('c_email', validators=[InputRequired()])
    subject = StringField('c_subject', validators=[InputRequired()])
    message = TextAreaField('c_message', validators=[InputRequired()])

class CouponCodeForm(FlaskForm):
    code = StringField('code', validators=[InputRequired()])

class CheckoutForm(FlaskForm):
    fname = StringField('f_name', validators=[InputRequired()])
    lname = StringField('l_name', validators=[InputRequired()])
    cname = StringField('c_name', validators=[InputRequired()])
    address = StringField('address', validators=[InputRequired()])
    apt = StringField('apt', validators=[InputRequired()])
    state = StringField('state', validators=[InputRequired()])
    zip = StringField('zip', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired()])
    phone = StringField('phone', validators=[InputRequired()])
    notes = StringField('notes', validators=[InputRequired()])


#bck end forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('Username Required')])
    password = PasswordField('Password', validators=[InputRequired()])

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    price = DecimalField('Price', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    small = IntegerField('Number of Small', validators=[InputRequired()])
    medium = IntegerField('Number of Medium', validators=[InputRequired()])
    large = IntegerField('Number of Large', validators=[InputRequired()])
    xl = IntegerField('Number of XL', validators=[InputRequired()])
    type = StringField('Type', validators=[InputRequired()])
    photo = FileField('Photo', validators=[FileRequired()])

class RemoveForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])

class EditForm(FlaskForm):
    ename = StringField('Name', validators=[InputRequired()])
    eemail = StringField('CompanyEmail', validators=[InputRequired()])
    eaddress = StringField('CompanyAddress', validators=[InputRequired()])
    ephone = StringField('CompanyPhone', validators=[InputRequired()])
    eabout = TextAreaField('CompanyAbout', validators=[InputRequired()])

class EditHome(FlaskForm):
    card1Title = StringField('Card 1 Title', validators=[InputRequired()])
    card1Tagline = StringField('Card 1 Tagline', validators=[InputRequired()])
    card1Price = StringField('Card 1 Price', validators=[InputRequired()])
    card1Link = StringField('Card 1 Link', validators=[InputRequired()])
    card1Photo = FileField('Card 1 Photo', validators=[FileRequired()])
    card2Hashtag = StringField('Card 2 Hashtag', validators=[InputRequired()])
    card2Title = StringField('Card 2 Title', validators=[InputRequired()])
    card2Link = StringField('Card 2 Link', validators=[InputRequired()])
    card2Photo = FileField('Card 2 Photo', validators=[FileRequired()])
    card3Hashtag = StringField('Card 3 Hashtag', validators=[InputRequired()])
    card3Title = StringField('Card 3 Title', validators=[InputRequired()])
    card3Link = StringField('Card 3 Link', validators=[InputRequired()])
    card3Photo = FileField('Card 3 Photo', validators=[FileRequired()])

class EditAbout(FlaskForm):
    aboutPar = StringField('About Paragraph', validators=[InputRequired()])
    title = StringField('Title ex How We Started', validators=[InputRequired()])
    cardPar = StringField('Card Paragraph', validators=[InputRequired()])
    cardPhoto = FileField('Card Photo', validators=[FileRequired()])
    team1Name = StringField('Team Member 1 Name', validators=[InputRequired()])
    team1Position = StringField('Team Member 1 Position', validators=[InputRequired()])
    team1About = StringField('Team Member 1 About', validators=[InputRequired()])
    team1Photo = FileField('Team 1 Photo', validators=[FileRequired()])
    team2Name = StringField('Team Member 2 Name', validators=[InputRequired()])
    team2Position = StringField('Team Member 2 Position', validators=[InputRequired()])
    team2About = StringField('Team Member 2 About', validators=[InputRequired()])
    team2Photo = FileField('Team 2 Photo', validators=[FileRequired()])
    team3Name = StringField('Team Member 3 Name', validators=[InputRequired()])
    team3Position = StringField('Team Member 3 Position', validators=[InputRequired()])
    team3About = StringField('Team Member 3 About', validators=[InputRequired()])
    team3Photo = FileField('Team 3 Photo', validators=[FileRequired()])
    team4Name = StringField('Team Member 4 Name', validators=[InputRequired()])
    team4Position = StringField('Team Member 4 Position', validators=[InputRequired()])
    team4About = StringField('Team Member 4 About', validators=[InputRequired()])
    team4Photo = FileField('Team 4 Photo', validators=[FileRequired()])

#classes



class Cart():
    def __init__(self,id):  #id for session or user
        self.id = id
        self.cart = []
        self.items = 0
        self.total = 0
    def addToCart(self, obj):
        self.cart.append(obj)
        self.items = self.items + 1
        self.total = self.total + obj.p

def visits():
    #dropTable(cur,"Visitors")
    createTable("Visitors","Date TEXT,Sessions INTEGER")
    count = selectOne("count(*)","Visitors")
    if count == 0:
        insert("Visitors","Date,Sessions",(str(date.today()),session.get('visits')))
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # reading and updating session data
        rows = selectAll("Visitors")
        for row in rows:
            if row[0] > str(date.today()):
                session['visits'] = 1
                insert("Visitors","Date,Sessions",(str(date.today()),session.get('visits')))
            else:
                update("Sessions","Visitors","Date", (session.get('visits'),str(date.today())))
    else:
        session['visits'] = 1 # setting session data
    return session.get('visits')

def cartSum():
    rows = selectAll("Cart")
    if len(rows) == 0:
        return 0
    return selectOne("SUM(Quantity)","Cart")

def editinfo():
    rows = selectAll("SiteInfo")
    if len(rows) == 0:
        return "Name", "Email", "Address", "Phone Number", "About"
    else:
        name = selectOne("Name","SiteInfo")
        email = selectOne("Email","SiteInfo")
        address = selectOne("Address","SiteInfo")
        phonenumber = selectOne("PhoneNumber","SiteInfo")
        about = selectOne("About","SiteInfo")
    return name,email,address,phonenumber,about

def homeinfo():
    rows = selectAll("EditHome")
    if len(rows) == 0:  #add images
        return "card1Title", "card1Tagline", "card1Link","card1Image", "card2Hashtag","card2Title", "card2Link","card2image","card3Hashtag","card3Title","card3Link","card3image"
    else:
        c1ti = selectOne("Card1Title","EditHome")
        c1ta = selectOne("Card1Tagline","EditHome")
        c1p = selectOne("Card1Price","EditHome")
        c1l = selectOne("Card1Link","EditHome")
        dst1 = selectOne("Card1Photo","EditHome")
        c2h = selectOne("Card2Hashtag","EditHome")
        c2t = selectOne("Card2Title","EditHome")
        c2l = selectOne("Card2Link","EditHome")
        dst2 = selectOne("Card2Photo","EditHome")
        c3h = selectOne("Card3Hashtag","EditHome")
        c3t = selectOne("Card3Title","EditHome")
        c3l = selectOne("Card3Link","EditHome")
        dst3 = selectOne("Card3Photo","EditHome")
    return c1ti,c1ta,c1p,c1l,dst1,c2h,c2t,c2l,dst2,c3h,c3t,c3l,dst3

def aboutinfo():
    rows = selectAll("EditAbout")
    if len(rows) == 0:  #add images
        return "About Paragraph", "Title, ex. How We Started", "Card Paragraph", "Team1Name","Team1Position", "Team1About","Team2Name","Team2Position", "Team2About","Team3Name","Team3Position", "Team3About","Team4Name","Team4Position", "Team4About"
    else:
        aP = selectOne("aboutPar","EditAbout")
        t = selectOne("Title","EditAbout")
        c1p = selectOne("cardPar","EditAbout")
        dst = selectOne("cardPhoto","EditAbout")
        t1n = selectOne("Team1Name","EditAbout")
        t1p = selectOne("Team1Position","EditAbout")
        t1a = selectOne("Team1About","EditAbout")
        dst1 = selectOne("Team1Photo","EditAbout")
        t2n = selectOne("Team2Name","EditAbout")
        t2p = selectOne("Team2Position","EditAbout")
        t2a = selectOne("Team2About","EditAbout")
        dst2 = selectOne("Team2Photo","EditAbout")
        t3n = selectOne("Team3Name","EditAbout")
        t3p = selectOne("Team3Position","EditAbout")
        t3a = selectOne("Team3About","EditAbout")
        dst3 = selectOne("Team3Photo","EditAbout")
        t4n = selectOne("Team4Name","EditAbout")
        t4p = selectOne("Team4Position","EditAbout")
        t4a = selectOne("Team4About","EditAbout")
        dst4 = selectOne("Team4Photo","EditAbout")
    return aP,t,c1p,dst,t1n,t1p,t1a,dst1,t2n,t2p,t2a,dst2,t3n,t3p,t3a,dst3,t4n,t4p,t4a,dst4

def createTable(table,fields):
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    temp = "CREATE TABLE IF NOT EXISTS "+table+" ("+fields+");"
    cur.execute(temp)
    con.commit()
    con.close()
    return

def dropTable(table):
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    temp = "DROP TABLE IF EXISTS "+table
    cur.execute(temp)
    con.commit()
    con.close()
    return

def selectOne(field,table):
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    temp = "SELECT "+field+" FROM "+table
    cur.execute(temp)
    ret = cur.fetchone()[0]
    con.close()
    return ret

def selectOneWhere(field,table,field2,option):
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    temp = "SELECT "+field+" FROM "+table+" WHERE "+field2+" = ?"
    if field == "EXISTS(SELECT 1":
        temp = temp+")"
    print (temp)
    cur.execute(temp,(option,))
    ret = cur.fetchone()[0]
    con.close()
    return ret

def selectAll(table):
    con = sqlite3.connect('products.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    temp = "SELECT * FROM "+table
    cur.execute(temp)
    ret = cur.fetchall()
    con.close()
    return ret

def selectAllWhere(table,field,option):
    con = sqlite3.connect('products.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    temp = "SELECT * FROM "+table+" WHERE "+field+" = ?"
    cur.execute(temp,(option,))
    ret = cur.fetchall()
    con.close()
    return ret

def insert(table,values,tuple):
    spots = ""
    for x in range(len(tuple)-1):
        spots = spots + "?,"
    spots = spots + "?"
    try:
       with sqlite3.connect("products.db") as con:
          cur = con.cursor()
          temp = "INSERT INTO "+table+" ("+values+") VALUES ("+spots+");"
          cur.execute(temp, tuple)
          con.commit()
    except:
       con.rollback()
    finally:
        con.close()
    return

def removeitem(table,field,option):
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    temp = 'SELECT EXISTS(SELECT 1 FROM '+table+' WHERE '+field+'=?);'
    cur.execute(temp,(option,))
    if (cur.fetchone()[0]==1):
        temp = 'DELETE FROM '+table+' WHERE '+field+' = ?;'
        cur.execute(temp,(option,))
        con.commit()
        con.close()
        return True
    con.close()
    return

def update(field,table,field2,option):
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    temp = 'UPDATE '+table+' SET '+field+'=? WHERE '+field2+' = ?;'
    cur.execute(temp,(option))
    con.commit()
    con.close()
    return

def uploadImage(file):
    filename = secure_filename(file.data.filename)
    file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.data.save(file_path)
    return "static/images/"+filename

createTable("SiteInfo","Name TEXT,Email TEXT,Address TEXT,PhoneNumber TEXT,About TEXT")
createTable("EditHome","Card1Title TEXT,Card1Tagline TEXT,Card1Price TEXT,Card1Link TEXT,Card1Photo BLOB,Card2Hashtag TEXT,Card2Title TEXT,Card2Link TEXT,Card2Photo BLOB,Card3Hashtag TEXT,Card3Title TEXT,Card3Link TEXT,Card3Photo BLOB")
createTable("EditAbout","aboutPar TEXT,Title TEXT,cardPar TEXT,cardPhoto BLOB,Team1Name TEXT,Team1Position TEXT,Team1About TEXT,Team1Photo BLOB,Team2Name TEXT,Team2Position TEXT,Team2About TEXT,Team2Photo BLOB,Team3Name TEXT,Team3Position TEXT,Team3About TEXT,Team3Photo BLOB,Team4Name TEXT,Team4Position TEXT,Team4About TEXT,Team4Photo BLOB")

createTable("Products","Name TEXT,Price REAL,Description TEXT,Small INTEGER,Medium INTEGER,Large INTEGER,XL INTEGER,Type TEXT,Image BLOB")
createTable("Cart","ItemNum TEXT,Name TEXT,Price REAL,Size TEXT,Quantity INTEGER,Total REAL,Image BLOB")

createTable("Subscribers","Email TEXT")
createTable("Contact","FName TEXT,LName TEXT,Email TEXT,Subject TEXT,Message TEXT")
createTable("Orders","FName TEXT,LName TEXT,Address TEXT,State TEXT,Zip TEXT,ProductsOption TEXT")

@app.route('/', methods = ['POST', 'GET'])
def home():
    name,email,address,phonenumber,about=editinfo()
    c1ti,c1ta,c1p,c1l,dst1,c2h,c2t,c2l,dst2,c3h,c3t,c3l,dst3=homeinfo()
    if request.method == 'POST':
        return redirect(url_for('shopsingle', prod=request.form['product']))
    return render_template("index.html", cart=cartSum(), subsciber_form=SubscriberForm(),
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,
        rows=selectAll("Products"),
        c1ti=c1ti,c1ta=c1ta,c1p=c1p,c1l=c1l,dst1=dst1,
        c2h=c2h,c2t=c2t,c2l=c2l,dst2=dst2,
        c3h=c3h,c3t=c3t,c3l=c3l,dst3=dst3)

@app.route('/index.html', methods = ['POST', 'GET'])
def index():
    return redirect(url_for('home'))

@app.route('/about.html',methods = ['POST', 'GET'])
def about():
   subsciber_form = SubscriberForm()
   cart = cartSum()
   name,email,address,phonenumber,about=editinfo()
   aP,t,c1p,dst,t1n,t1p,t1a,dst1,t2n,t2p,t2a,dst2,t3n,t3p,t3a,dst3,t4n,t4p,t4a,dst4=aboutinfo()
   if subsciber_form.validate_on_submit():
       insert("Subscribers",(subsciber_form.email.data))
   return render_template('about.html',cart=cartSum(), subsciber_form=SubscriberForm(),
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,
        aP=aP,t=t,c1p=c1p,dst=dst,t1n=t1n,t1p=t1p,t1a=t1a,dst1=dst1,
        t2n=t2n,t2p=t2p,t2a=t2a,dst2=dst2,
        t3n=t3n,t3p=t3p,t3a=t3a,dst3=dst3,
        t4n=t4n,t4p=t4p,t4a=t4a,dst4=dst4)

@app.route('/subscribed.html',methods = ['POST', 'GET'])
def subscribed():
   subsciber_form=SubscriberForm()
   name,email,address,phonenumber,about=editinfo()
   if subsciber_form.validate_on_submit():
       val = subsciber_form.email.data
       insert("Subscribers","Email",(val))
   return render_template('subscribed.html',cart=cartSum(),subsciber_form=subsciber_form,
        name=name, email=email,address=address,phonenumber=phonenumber,about=about)

@app.route('/contact.html',methods = ['POST', 'GET'])
def contact():
    contact_form = ContactForm()
    name,email,address,phonenumber,about=editinfo()
    if contact_form.validate_on_submit():
        insert("Contact","FName,LName,Email,Subject,Message",(contact_form.fname.data,contact_form.lname.data,contact_form.email.data,contact_form.subject.data,contact_form.message.data))
        return redirect(url_for('home'))   #returning to homepage after adding data
    return render_template("contact.html", cart=cartSum(), contact_form=contact_form,
    name=name, email=email,address=address,phonenumber=phonenumber,about=about)


@app.route('/shop.html',methods = ['POST', 'GET'])
def shop():
    name,email,address,phonenumber,about=editinfo()
    if request.method == 'POST':
        return redirect(url_for('shopsingle', prod=request.form['product']))
    return render_template('shop.html',cart=cartSum(), subsciber_form=SubscriberForm(),
    name=name, email=email,address=address,phonenumber=phonenumber,about=about,
    rows=selectAll("Products"))

@app.route('/<prod>.html',methods = ['POST', 'GET'])
def shopsingle(prod=None):    #get name, price, pricture, descritption, or row number and get from directory
    subsciber_form = SubscriberForm()
    cart = cartSum()
    name,email,address,phonenumber,about=editinfo()
    options = []
    t="Services"
    flag = selectOneWhere("EXISTS(SELECT 1","Products","Name",prod)
    if flag == 1:
        t="Products"
        if selectOneWhere("Small","Products","Name",prod) > 0:
            options.append('Small')
        if selectOneWhere("Medium","Products","Name",prod) > 0:
            options.append('Medium')
        if selectOneWhere("Large","Products","Name",prod) > 0:
            options.append('Large')
        if selectOneWhere("XL","Products","Name",prod) > 0:
            options.append('XL')
    price = selectOneWhere("Price",t,"Name",prod)
    description = selectOneWhere("Description",t,"Name",prod)
    dst = selectOneWhere("Image",t,"Name",prod)
    if request.method == 'POST':
        option = request.form['option']
        quantity = int(request.form['qty'])
        total=selectOneWhere("Price",t,"Name",prod)*quantity
        item=date.today()
        insert("Cart","ItemNum,Name,Price,Size,Quantity,Total,Image",(item,prod,price,option,quantity,total,dst))
        return redirect(url_for('cart'))
    return render_template('shop-single.html',prod=prod,cart=cart, subsciber_form=subsciber_form,
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,
        options=options,price=format(price, '.2f'),description=description,image=dst)


@app.route('/cart.html',methods = ['POST', 'GET'])
def cart():
    name,email,address,phonenumber,about=editinfo()
    rows = selectAll("Cart")
    if len(rows) == 0:
        sub = 0
    else:
        sub = float(selectOne("SUM(Total)","Cart"))
    if request.method == 'POST':
        #dropTable("Cart")
        createTable("Cart","ItemNum TEXT,Name TEXT,Price REAL,Size TEXT,Quantity INTEGER,Total REAL,Image BLOB")
        if removeitem("Cart","ItemNum",request.form['remove']):
            if len(selectAll("Cart")) == 0:
                sub = 0
            else:
                sub = float(selectOne("SUM(Total)","Cart"))
        ship = 5
        total = round(sub * 1.07,2)
        return render_template('cart.html',cart=cartSum(),subsciber_form=SubscriberForm(),
            name=name, email=email,address=address,phonenumber=phonenumber,about=about,
            rows=selectAll("Cart"), subtotal=sub, total=total)
    ship = 5
    total = round(sub * 1.07,2)
    return render_template('cart.html',cart=cartSum(),subsciber_form=SubscriberForm(),
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,
        rows=selectAll("Cart"), subtotal=sub, total=total)

@app.route('/checkout.html',methods = ['POST', 'GET'])
def checkout():
    subsciber_form = SubscriberForm()
    coupon_form = CouponCodeForm()
    name,email,address,phonenumber,about=editinfo()
    rows = selectAll("Cart")
    sub = float(selectOne("SUM(Total)","Cart"))
    ship = 5
    total = round(sub * 1.07,2)
    sub = format(sub, '.2f')
    total = format(total, '.2f')
    if request.method == 'POST':
        return redirect(url_for('thankyou'))
    return render_template('checkout.html',cart=cartSum(), subsciber_form=subsciber_form,
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,
        rows=selectAll("Cart"), subtotal=sub, total=total)

@app.route('/thankyou.html',methods = ['POST', 'GET'])
def thankyou():
   subsciber_form = SubscriberForm()
   name,email,address,phonenumber,about=editinfo()
   dropTable("Cart")
   createTable("Cart","ItemNum INTEGER,Name TEXT,Price REAL,Size TEXT,Quantity INTEGER,Total REAL,Image BLOB")
   return render_template('thankyou.html',cart=cartSum(),subsciber_form=subsciber_form,
        name=name, email=email,address=address,phonenumber=phonenumber,about=about)


#back-end   (ADMIN)
@app.route('/login',methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == users[form.username.data]['password']:
            user = User()
            user.id = form.username.data
            flask_login.login_user(user)
            return(redirect(url_for('adminhome')))
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/adminhome',methods = ['POST', 'GET'])
@flask_login.login_required
def adminhome():
    labels=[]
    values=[]
    max = 0
    sessions = visits() #add to eveyr page?
    rows = selectAll("Visitors")
    for row in rows:
        labels.append(row[0])
        values.append(row[1])
        if row[1] > max:
            max = row[1]
    max = max * 1.125
    return render_template('adminhome.html',sessions=sessions,labels=labels, values=values, max=max)

@app.route('/edit', methods = ['POST', 'GET'])
@flask_login.login_required
def edit():
    form = EditForm()
    name="Overall"
    if form.validate_on_submit():
        ename = form.ename.data
        eemail = form.eemail.data
        eaddress = form.eaddress.data
        ephone = form.ephone.data
        eabout = form.eabout.data
        dropTable("SiteInfo")
        createTable("SiteInfo","Name TEXT,Email TEXT,Address TEXT,PhoneNumber TEXT,About TEXT")
        insert("SiteInfo","Name, Email, Address, PhoneNumber, About",(ename,eemail, eaddress, ephone, eabout))
        return redirect(url_for('home'))
    return render_template("edit.html", form=form, name=name)

@app.route('/edithome', methods = ['POST', 'GET'])
@flask_login.login_required
def edithome():
    form = EditHome()
    name="Home"
    if form.validate_on_submit():
        c1ti = form.card1Title.data
        c1ta = form.card1Tagline.data
        c1p = form.card1Price.data
        c1l = form.card1Link.data
        dst1 = uploadImage(form.card1Photo)
        c2h = form.card2Hashtag.data
        c2t = form.card2Title.data
        c2l = form.card2Link.data
        dst2 = uploadImage(form.card2Photo)
        c3h = form.card3Hashtag.data
        c3t = form.card3Title.data
        c3l = form.card3Link.data
        dst3 = uploadImage(form.card3Photo)
        dropTable("EditHome")
        createTable("EditHome","Card1Title TEXT,Card1Tagline TEXT,Card1Price TEXT,Card1Link TEXT,Card1Photo BLOB,Card2Hashtag TEXT,Card2Title TEXT,Card2Link TEXT,Card2Photo BLOB,Card3Hashtag TEXT,Card3Title TEXT,Card3Link TEXT,Card3Photo BLOB")
        insert("EditHome","Card1Title, Card1Tagline, Card1Price, Card1Link, Card1Photo, Card2Hashtag,Card2Title,Card2Link,Card2Photo,Card3Hashtag,Card3Title,Card3Link,Card3Photo",(c1ti,c1ta,c1p,c1l,dst1, c2h,c2t,c2l,dst2, c3h,c3t,c3l,dst3))
        return redirect(url_for('home'))
    return render_template("edit.html", form=form, name=name)

@app.route('/editabout', methods = ['POST', 'GET'])
@flask_login.login_required
def editabout():
    form = EditAbout()
    name="About"
    if form.validate_on_submit():
        about = form.aboutPar.data
        title = form.title.data
        dst = uploadImage(form.cardPhoto)
        t1n = form.team1Name.data
        t1p = form.team1Position.data
        t1a = form.team1About.data
        dst1 = uploadImage(form.team1Photo)
        t2n = form.team2Name.data
        t2p = form.team2Position.data
        t2a = form.team2About.data
        dst2 = uploadImage(form.team2Photo)
        t3n = form.team1Name.data
        t3p = form.team3Position.data
        t3a = form.team3About.data
        dst3 = uploadImage(form.team3Photo)
        t4n = form.team1Name.data
        t4p = form.team4Position.data
        t4a = form.team4About.data
        dst4 = uploadImage(form.team4Photo)
        dropTable("EditAbout")
        createTable("EditAbout","aboutPar TEXT,Title TEXT,cardPar TEXT,cardPhoto BLOB,Team1Name TEXT,Team1Position TEXT,Team1About TEXT,Team1Photo BLOB,Team2Name TEXT,Team2Position TEXT,Team2About TEXT,Team2Photo BLOB,Team3Name TEXT,Team3Position TEXT,Team3About TEXT,Team3Photo BLOB,Team4Name TEXT,Team4Position TEXT,Team4About TEXT,Team4Photo BLOB")
        insert("EditAbout","aboutPar, Title, cardPar,cardPhoto,Team1Name,Team1Position, Team1About,Team1Photo, Team2Name,Team2Position,Team2About,Team2Photo,Team3Name,Team3Position,Team3About,Team3Photo,Team4Name,Team4Position,Team4About,Team4Photo",(about,title,c1p,dst,t1n,t1p,t1a,dst1,t2n,t2p,t2a,dst2,t3n,t3p,t3a,dst3,t4n,t4p,t4a,dst4))
        return redirect(url_for('about'))
    return render_template("edit.html", form=form, name=name)

@app.route('/add', methods = ['POST', 'GET'])
@flask_login.login_required
def add():
    form = ProductForm()
    form2 = RemoveForm()
    list=['Name', 'Price', 'Description', 'Small', 'Medium', 'Large', 'XL', 'Type', 'Image']
    if form.validate_on_submit():
        name = form.name.data
        price = float(form.price.data)
        description = form.description.data
        small = int(form.small.data)
        medium = int(form.medium.data)
        large = int(form.large.data)
        xl = int(form.xl.data)
        type = form.type.data
        dst = uploadImage(form.photo)
        insert("Products","Name, Price, Description, Small, Medium, Large, XL, Type, Image",(name,price, description, small, medium, large, xl, type, dst))
        return render_template("add.html", name="Products",form=form, form2=form2, rows=selectAll("Products"),list=list)
    return render_template("add.html", name="Products", form=form, form2=form2, rows=selectAll("Products"),list=list)

@app.route('/services', methods = ['POST', 'GET'])
@flask_login.login_required
def services():
    form = ServicesForm()
    form2 = RemoveForm()
    list=['Name', 'Price', 'Time', 'Description', 'Type', 'Image']
    if form.validate_on_submit():
        name = form.sname.data
        price = float(form.sprice.data)
        time = form.stime.data
        description = form.sdescription.data
        type = form.stype.data
        dst = uploadImage(form.sphoto)
        insert("Services","Name, Price, Time, Description, Type, Image",(name,price,time,description,type,dst))
        return render_template("add.html", name="Services", form=form,form2=form2,rows=selectAll("Services"),list=list)
    return render_template("add.html", name="Services", form=form,form2=form2,rows=selectAll("Services"),list=list)

@app.route('/remove', methods = ['POST', 'GET'])
@flask_login.login_required
def remove():
    form = ProductForm()
    form2 = RemoveForm()
    if form2.validate_on_submit():
        name = form2.name.data
        if removeitem("Products","Name",name):
            return redirect(url_for('add'))
        if removeitem("Services","Name",name):
            return redirect(url_for('services'))
        if removeitem("Artists","Name",name):
            return redirect(url_for('addartist'))
        if removeitem("Watch","Name",name):
            return redirect(url_for('addwatch'))
        if removeitem("Playlist","Name",name):
            return redirect(url_for('addplaylist'))
        return redirect(url_for('add'))
    return redirect(url_for('add'))

@app.route('/orders', methods = ['POST', 'GET'])
@flask_login.login_required
def orders():
    list=['FName','LName','Address','State','ProductsOption']
    return render_template("orders.html", name="Orders",rows=selectAll("Orders"),list=list)

@app.route('/subscribers', methods = ['POST', 'GET'])
@flask_login.login_required
def subscribers():
    list=['Email']
    return render_template("orders.html", name="Subscribers", rows=selectAll("Subscribers"),list=list)

@app.route('/contactList', methods = ['POST', 'GET'])
@flask_login.login_required
def contactList():
    list=['FName','LName','Email','Subject','Message']
    return render_template("orders.html", name="Contacts", rows=selectAll("Contact"),list=list)

@app.route('/logout', methods = ['POST', 'GET'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':  #function for if this were main

   app.run(debug = True)    #run application

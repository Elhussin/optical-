# Importing the Required Library
import os 
import pywhatkit
from flask_qrcode import QRcode
from pyFile.brand import brand
from pyFile.payment import payment
from pyFile.payment import payments
from pyFile.register import register, login
from pyFile.company import company
from pyFile.users import admin, brofile
from pyFile.cart import cart
from pyFile.data import *
from pyFile.sqlRequest import *
from pyFile.addres import addres
from pyFile.branch import branch
from pyFile.model import model,updateproduct
from pyFile.data import navList, brand_list
from pyFile.resetPassword import reset  
from pyFile.userupdate import update
from pyFile.viwer import viwer  
from pyFile.updates import updateCompany  ,updateBrand, updatTrack,updateBranch,deleteInvoice
import sqlite3
from flask import ( Flask, request,render_template,redirect,flash, session,jsonify )
from flask_session import Session
from werkzeug.utils import secure_filename
from pyFile.helpers import login_required
from flask_caching import Cache


# Check Configuring Flask-Cache section for more details
config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
}
# declara app
app = Flask(__name__)
# qr code
QRcode(app)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# configer cash
app.config.from_mapping(config)
cache = Cache(app)

import os

# تحقق من وجود متغير البيئة DISPLAY
if os.environ.get('DISPLAY'):
    import pyautogui
    import pywhatkit
    print("تم استيراد pyautogui و pywhatkit")
else:
    print("لا يمكن استخدام pyautogui و pywhatkit في هذه البيئة")
    # يمكنك أيضًا تعطيل الوظائف التي تعتمد على هذه المكتبات هنا


# call routes from another file
app.register_blueprint(brand, url_prefix="")
app.register_blueprint(register, url_prefix="")
app.register_blueprint(login, url_prefix="")
app.register_blueprint(company, url_prefix="")
app.register_blueprint(admin, url_prefix="")
app.register_blueprint(brofile, url_prefix="")
app.register_blueprint(cart, url_prefix="")
app.register_blueprint(model, url_prefix="")
app.register_blueprint(addres, url_prefix="")
app.register_blueprint(payments, url_prefix="")
app.register_blueprint(payment, url_prefix="")
app.register_blueprint(branch, url_prefix="")
app.register_blueprint(reset, url_prefix="")
app.register_blueprint(update, url_prefix="")
app.register_blueprint(viwer, url_prefix="")
app.register_blueprint(updateCompany, url_prefix="")
app.register_blueprint(updateBrand, url_prefix="")
app.register_blueprint(updatTrack, url_prefix="")
app.register_blueprint(updateBranch, url_prefix="")
app.register_blueprint(deleteInvoice, url_prefix="")
app.register_blueprint(updateproduct, url_prefix="")
@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    # session.clear()
    try:
        del session["user_id"]
        del session["company_id"]
        del session["brandType"]
    except KeyError:
        pass
    return redirect("/")


#  index rout
@app.route("/")
@cache.cached(timeout=50)
def index():
    rows= allPProdueact()

    return render_template("index.html", response=rows, navList=navList)
 

@app.route("/sun" , methods=["GET", "POST"])
@app.route("/glasses" , methods=["GET", "POST"])
@app.route("/ContactLens", methods=["GET", "POST"])
@app.route("/Accessories" , methods=["GET", "POST"]) 
def fram_cotgery():
    txt=request.url
    x = txt.split("/")
    x=x[-1]
    shows = fram_cetgeray(x)
    return render_template("index.html", response=shows, title=x)

# viwer functian 
@app.route("/topSeller", methods=["GET", "POST"])
@app.route("/new" , methods=["GET", "POST"]) 
@app.route("/offers" , methods=["GET", "POST"])
def newOffetTopseller():
    txt=request.url
    x = txt.split("/")
    x=x[-1]
    shows = newOffetTopSell(x)
    return render_template("index.html", response=shows, title=x)

@app.route("/hotsell", methods=["GET", "POST"])

def hotsell():
    txt=request.url
    x = txt.split("/")
    x=x[-1]
    shows = hotseller()
    return render_template("index.html", response=shows, title=x)


# viwer function  with two argment 

@app.route("/new_MEN") 
@app.route("/new_Women") 
@app.route("/new_Kids")
 
@app.route("/sun_MEN")
@app.route("/sun_Women")
@app.route("/sun_Kids")
@app.route("/glasses_MEN")
@app.route("/glasses_Women")
@app.route("/glasses_Kids")
@app.route("/ContactLens_Clear")
@app.route("/ContactLens_Color")
@app.route("/Accessories_Women") 
@app.route("/Accessories_Kids")
def nav_view_branch():
    txt=request.url
    x = txt.split("/")
    x=x[-1]
    x=x.split("_")
    shows = cotegryList_collection(x[0],x[1])
    return render_template("index.html", response=shows, title=x[-1])





# search function
@app.route("/search")
def search():

    search = request.args.get("value")

    if search:
        shows =  cotegryList(search)
    else:
        shows = []
    return jsonify(shows)

#  view one iteam
@app.route("/item", methods=["GET", "POST"])
def iteam():
    if request.method == "POST":
        product_id = request.form.get("item_id")
        shows= iteam_view(product_id)
        return render_template("index.html", response_card=shows,title='VIEW')
    else:
        return redirect("/")

# uploud files and media
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif","webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# uploud data 
@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_file():
    conifg_users= conifg_user(session["user_id"])
    if conifg_users== 'user':
        flash("Access is denied!")
        return redirect("/")
    product_type = request.args.get("product_type")
    if product_type:
        listof_proudeact = readBroudectList(product_type)
        return jsonify(listof_proudeact)

    else:
        listof_proudeact = []
    if request.method == "GET":
        return render_template("upload.html", brand_list=brand_list)
    elif request.method == "POST":
        product_id = request.form.get("product_id")
        if not product_id or product_id == "null":
            flash("Select Proudect ")
        media_description = request.form.get("description")
        Show_stat = request.form.get("Show_on")

        files = request.files.getlist("multiple_files[]")
        filenames = []
        conn = sqlite3.connect("stor.db")
        cursor = conn.cursor()
        proudet_confiarm = cursor.execute(
            """ SELECT *  From  addMedia where product_id = :product_id""",
            {"product_id": product_id},
        )
        records = proudet_confiarm.fetchall()
        if len(records) >= 1:
            response = "This Iteam Add Alreayd, Product Id :  " + product_id
            return render_template(
                "upload.html", brand_list=brand_list, response=response
            )


        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                filenames.append(filename)

                try:
                    cursor.execute(
                        """insert into addMedia(imagelink,media_description,product_id,Show_stat,user_id) values(
                  :imagelink,:media_description,:product_id,:Show_stat,:user_id)""",
                        {
                            "imagelink": filename,
                            # "product_type": request.form.get("product_type"),
                            "media_description": media_description,
                            "product_id": product_id,
                            "Show_stat": Show_stat,
                            "user_id": session["user_id"],
                        },
                    )
                    conn.commit()
                    flash("Uploaded files: {}".format(", ".join(filenames)))

                    response = "Done Add  Media "

                    return render_template(
                        "upload.html", brand_list=brand_list, response=response
                    )

                except sqlite3.Error as error:
                    flash(f"{error}")

        if len(filenames) == 0:
            flash("No Media File  Uploud File")
            return render_template("upload.html",brand_list=brand_list)
        else:
            flash("Uploaded files: {}".format(", ".join(filenames)))

            conn.close()

    return render_template("upload.html", brand_list=brand_list)


# invoice history for user 
@app.route("/history")
@login_required
def invoiceHistory():
    conn = sqlite3.connect("stor.db")
    conn.row_factory = sqlite3.Row
    conifg_users=conifg_user(session["user_id"]) 
    """Show history of invoice """
    if conifg_users[0]["U_type"] == 'user':
        history=mainInvoiceList(session["user_id"])
        return render_template("history.html", history=history )
    elif conifg_users[0]["U_type"] == 'admin': 
        cursor = conn.cursor()
        cursor.execute( """ SELECT * FROM  invoice """)
        conn.commit()
        records = cursor.fetchall() 
        conn.close() 
        history=sqliteHandel(records)
        return render_template("history.html", history=history )
    return render_template("history.html")

# invoice  
@app.route("/invoice", methods=["GET", "POST"])
# @login_required
def invoicedatiles():
    """Show orderTrack of transactions"""
    # InvoiceList=mainInvoiceList(session["user_id"])
    if request.method == "POST":
        invoice_id = request.form.get("invoice_id")
        payment_id =request.form.get("payment_id")
        if invoice_id:
            invoiceDatilesList=invoiceDatiles(invoice_id)
            return render_template("invoice.html",invoice=invoiceDatilesList)
        if payment_id :
            invoiceDatilesList=invoiceDatilesByPaumeant(payment_id)
            return render_template("invoice.html",invoice=invoiceDatilesList)
    if request.method == "GET":
         invoice_id= request.args.get("serial")

         invoiceDatilesList=invoiceDatiles(invoice_id)
         return render_template("invoice.html",invoice=invoiceDatilesList)
    




# order track for user 
@app.route("/orderTrack")
@login_required
def orderTrackfun():
    conn = sqlite3.connect("stor.db")
    conn.row_factory = sqlite3.Row
    conifg_users=conifg_user(session["user_id"]) 
    """Show history of order track transactions"""
    if conifg_users[0]["U_type"] == 'user':
        orderTracks=orderTrack(session["user_id"])
        return render_template("orderTrack.html" ,orderTracks=orderTracks)
    # """Show history of order track transactions for admin """
    elif conifg_users[0]["U_type"] == 'admin': 
        cursor = conn.cursor()
        cursor.execute ("""SELECT * FROM order_trak   ORDER BY order_id DESC""")
        conn.commit()
        records = cursor.fetchall() 
        conn.close() 
        orderTracks=sqliteHandel(records) 
        return render_template("orderTrack.html" ,orderTracks=orderTracks)
    return render_template("orderTrack.html")


   

# payment history for user and admin  aLL 
@app.route("/payhistory")
@login_required
def paymentHistorys():
    conn = sqlite3.connect("stor.db")
    conn.row_factory = sqlite3.Row
    conifg_users=conifg_user(session["user_id"]) 
    """Show history of payment transactions"""
    if conifg_users[0]["U_type"] == 'user':
        paymentHistory=paymentview_user(session["user_id"])
        return render_template("payhistory.html", paymentHistory=paymentHistory )
    elif conifg_users[0]["U_type"] == 'admin':
        cursor = conn.cursor()
        cursor.execute( """ SELECT * FROM  payment  """)   
        conn.commit()
        records = cursor.fetchall() 
        conn.close() 
        paymentHistory=sqliteHandel(records) 
        return render_template("payhistory.html", paymentHistory=paymentHistory )
    return render_template("payhistory.html" )


@app.route("/netfectian")
@login_required
def netfectians():
    """Show Notification for users """
    conn = sqlite3.connect("stor.db")
    conn.row_factory = sqlite3.Row
    session["netfectians"]=0
    """Show history of netfectians """
    conifg_users=conifg_user(session["user_id"]) 
    if conifg_users[0]["U_type"] == 'user':
        cursor = conn.cursor()
        cursor.execute( """ SELECT * FROM  invoice where status=1 OR status=2 and user_Id=:user_Id""",
                       {"user_Id":session["user_id"]})
        conn.commit()
        records = cursor.fetchall() 
        session["netfectians"]=len(records)

        conn.close() 
        netfectiansInvoice=sqliteHandel(records) 
        return render_template("netfectian.html", netfectiansInvoice=netfectiansInvoice )
    #  Notification for admin 
    elif conifg_users[0]["U_type"] == 'admin':
        cursor = conn.cursor()
        cursor.execute( """ SELECT * FROM  invoice where status=1 """)
        conn.commit()
        records = cursor.fetchall() 
        session["netfectians"]=len(records)
 
        conn.close() 
        netfectiansInvoice=sqliteHandel(records) 

        
        return render_template("netfectian.html", netfectiansInvoice=netfectiansInvoice )
    

        

# Defining the Phone Number and Message

@app.route("/whatsUp")       
def whatsUp():
        phone_number = "+966540919725"
        message = "I Want Get Recommended About your Products"
# Sending the WhatsApp Message
        pywhatkit.sendwhatmsg_instantly(phone_number, message)
        
        return redirect("/")


# @app.jop("/jop")      

@app.route("/help", methods=["GET", "POST"])     
def help():
    conn = sqlite3.connect("stor.db")
    cursor = conn.cursor()
    if request.method == "POST":
        tell = request.form.get("TellNamber")
        MessageBody = request.form.get("Message")
        email = request.form.get("Email")
        name = request.form.get("Name")
        cursor.execute(
                        """insert into coustmearMessage(name,email,tell,MessageBody) values( :name,:email,:tell,:MessageBody)""",
                        {"name": name,"email": email,"tell": tell, "MessageBody": MessageBody,},
                    )
           
        conn.commit()
        conn.close()
        message='thanks for your contact ,We are happy to receive your message ,our team will call you soon.'
        return render_template("help.html" ,message=message )
    
    
    return render_template("help.html" )


           

#     Requirement  

@app.route("/addJop", methods=["GET", "POST"])     
@login_required
def addjop():
    conifg_users= conifg_user(session["user_id"])
    if conifg_users== 'user':
        flash("Access is denied!")
        return redirect("/")
    conn = sqlite3.connect("stor.db")
    conn.row_factory = sqlite3.Row

    if request.method == "POST":
        sallery = request.form.get("Sallery")
        requirement = request.form.get("requirement")
        location = request.form.get("location")
        EndIn = request.form.get("EndIn")
        Title = request.form.get("Title")
        startIn = request.form.get("startIn")
        datiles = request.form.get("datiles")
        cursor = conn.cursor()
        cursor.execute(
                        """insert into addJops(sallery,loctian,EndIn,requermeant,Title,startIn,datiles,admin_id) 
                        values( :sallery,:location,:EndIn,:requirement,:Title,:startIn,:datiles,:admin_id)""",
                        {"sallery": sallery,"location": location,"EndIn": EndIn, "requirement": requirement,
                         'Title':Title,'startIn':startIn,'datiles':datiles,'admin_id':session['user_id']},
                    )
           
        conn.commit()
        conn.close()
        message='Jop Add Success'
        return render_template("addJop.html" ,message=message )
    return render_template("addJop.html")





@app.route("/newJop", methods=["GET", "POST"])     
def newJop():
        conn = sqlite3.connect("stor.db")
        conn.row_factory = sqlite3.Row
        if request.method == "GET":
            cursor = conn.cursor()
            cursor.execute( """ SELECT * FROM  addJops  """)
            conn.commit()
            records = cursor.fetchall() 
            NewJops=sqliteHandel(records)
            conn.close() 
            return render_template("newJop.html",NewJops=NewJops )
        return render_template("newJop.html")

@app.route("/ourBranch", methods=["GET", "POST"])     
def ourBranch():
        conn = sqlite3.connect("stor.db")
        conn.row_factory = sqlite3.Row
        if request.method == "GET":
            cursor = conn.cursor()
            cursor.execute( """ SELECT * FROM  branchs  """)
            conn.commit()
            records = cursor.fetchall() 
            branchs=sqliteHandel(records)
            conn.close() 
            return render_template("ourBranch.html",branchs=branchs )
        return render_template("ourBranch.html")

@app.route("/learn", methods=["GET", "POST"])     
def learning():
        messag='You are Welcome in our Continuing Learning Center,  We are always up to date with the latest developments in the sciences of optics, medical glasses and sunglasses.'
        return render_template("lern.html" ,messag=messag)
    

# if __name__ == '__main__':
#     app.run(host="0.0.0.0",port="5000")

# # if __name__ == "__main__":
# #     app.run()

if __name__ == "__main__":
    app.run(debug=True)
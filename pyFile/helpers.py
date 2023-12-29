import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid
from twilio.rest import Client

from flask import redirect, render_template, session,request
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('\"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("error.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history&includeAdjustedClose=true"
    )

    # Query API
    try:
        response = requests.get(
            url,
            cookies={"session": str(uuid.uuid4())},
            headers={"User-Agent": "python-requests", "Accept": "*/*"},
        )
        response.raise_for_status()

        # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
        quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
        quotes.reverse()
        price = round(float(quotes[0]["Adj Close"]), 2)
        return {"name": symbol, "price": price, "symbol": symbol}
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def password_confiarm(password):
    pasord_special_char = ["$", "@", "#", "%", "&", "*"]
    error_maseg = ""
    if len(password) < 8:
        error_maseg = "length should be at least 8 and not be greater than 20"
        # return render_template("register.html", error_maseg=error_maseg)
    elif len(password) > 20:
        error_maseg = "length should be at least 8 and not be greater than 20"
        # return render_template("register.html", error_maseg=error_maseg)

    elif not any(i.isdigit() for i in password):
        error_maseg = "Password should have at least one digit"
        # return render_template("register.html", error_maseg=error_maseg)
    elif not any(i.isupper() for i in password):
        error_maseg = "Password should have at least one uppercase letter"
        # return render_template("register.html", error_maseg=error_maseg)
    elif not any(i.islower() for i in password):
        error_maseg = "Password should have at least one lowercase letter"
        # return render_template("register.html", error_maseg=error_maseg)

    elif not any(i in pasord_special_char for i in password):
        error_maseg = "Password should have at least one of the symbols $ @ # % & *"
        # return render_template("register.html", error_maseg=error_maseg)
    else:
        error_maseg = True

    return error_maseg




# Verifying if the message is sent or not


def messag(inov,order,user):
    print("userm",user[1])
    # first_name,phone,email
    link='http://127.0.0.1:5000/invoice?serial='+str(inov)
   
    messages=f"Dear Mr {str(user[0])} Your Order number :{order} start prparining  to print your invoice clik here  {link}"
    account_sid = 'AC201ecaea74068e00addc87abccafd775'
    auth_token = '0e0cbc15314d5c2d64271f02aa570220'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='+14157499226',
    body=messages,
    to=user[1])
    
    print(f"SMS sent successfully. Message ID: {message.sid}")
    # return redirect("/")
    
    
    
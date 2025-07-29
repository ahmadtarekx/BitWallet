import datetime 

import sqlite3

import random 
import string

import os
os.chdir(r"E:\Study\python\test 10")

db=sqlite3.connect("BitWalletInc.db")#DataBase Creation
cr=db.cursor()#Cursor Creation

#creation of table 
cr.execute("create table if not exists user(SSN text,username text,password text,fullname text)")
cr.execute("create table if not exists wallet(SSN text,username text,amount float)")
#Commit And Close
def commit():
    db.commit()

def close():
        db.close()

def time():
    today=datetime.date.today()
    hour=datetime.datetime.now().hour
    min=datetime.datetime.now().minute
    sec=datetime.datetime.now().second
    print(f"Transaction Made At <{today}>")
    print(f"                     <{hour}:{min}:{sec}>")

# def serial(count):
#     all_char = string.ascii_letters + string.digits

#     char_count = len(all_char)

#     serial_list = []

#     while count > 0 :
#         random_num = random.randint(0 , char_count - 1)
#         random_char =all_char[random_num]
#         serial_list.append(random_char)
#         count -= 1
#     SSN = "".join(serial_list)
#     return SSN

def serial(count):
    all_char = string.digits

    char_count = len(all_char)

    serial_list = []

    while count > 0 :
        random_num = random.randint(0 , char_count - 1)
        random_char =all_char[random_num]
        serial_list.append(random_char)
        count -= 1
    SSN = "".join(serial_list)
    return SSN

class user:
     def login():
        user_ssn = input("Enter your SSN: ").strip()
        global ussn
        ussn=user_ssn
        cr.execute("SELECT SSN FROM user WHERE SSN = ?", (user_ssn,))
        result = cr.fetchone()
        cr.execute("SELECT username FROM user WHERE SSN = ?", (user_ssn,))
        username=cr.fetchone()

        if result:
            print(f"Hello {username[0]}")
            pas = input("Please enter your password: ").strip()
        
            cr.execute("SELECT password FROM user WHERE SSN = ? AND username = ? ", (user_ssn,username[0],))
            password_check = cr.fetchone()
        
            if password_check[0]==pas:
                print("Log_in successfull! :) ")
                commands.get_action()
            else:
                print("Invalid password.")
                user.login()
        else:
            user.sign_up()
        
     def sign_up():

        print("Hello Dear You Seem to be New in Town")
        user_name = input("Enter your username: ").strip().capitalize()
        user_pass= input("Please enter your Password: ").strip()
        user_FN= input("Please enter your FullName: ").lower()
        User_SSN=serial(6)

        check=True

        while check: 
            cr.execute("SELECT SSN FROM user WHERE SSN = ?", (User_SSN,))
            result = cr.fetchone()

            if result:
                User_SSN=serial(6)
            else:
                check = False

        cr.execute("insert into user(SSN,username,password,fullname) values(?,?,?,?)",(User_SSN,user_name,user_pass,user_FN,))
        cr.execute("insert into wallet(SSN,username) values(?,?)",(User_SSN,user_name,))
        commit()
        print("Don't share your ID with anyone; you can use it for future processes.")
        print(f"your ID ==> {User_SSN}")

        user.login()

class commands(user):
    def currency_selector(curr):
        currency=1
        if curr=="usd":
            return currency * 48.35
        elif curr=="eur":
            return currency * 53.40
        elif curr=="cny":
            return currency * 6.80
        elif curr=="kwd":
            return currency * 158.8583
        elif curr=="sar":
            return currency * 12.88
        elif curr=="rub":
            return currency * 0.53 
        else:
            return False
        
    def cif(action):
        if action=="input":
            commands.input_c()
        elif action=="withdraw":
             print("withdraw funtion!")
        elif action=="review":
             print("review funtion!")
        else:
            print("Inavailble function!")
            commands.cif(action)

    def get_action():
        print("There are 3 choices --> input/withdraw/review")
        action=input("What do you want to do: ")
        commands.cif(action)

    def input_c():
        curr=input("Please enter currency of input: ").strip().lower()
        am=input("Please enter the amount for input: ")
        amount=float(am)
        rcv=amount*commands.currency_selector(curr)
        cr.execute("insert into wallet(amount) values (?) where SSN=?",(rcv,ussn,))
        commit()

user.login()
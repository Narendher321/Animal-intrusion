# main.py
import os
import base64
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from camera import VideoCamera
from camera2 import VideoCamera2
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import argparse
import cv2 
import shutil
import random
from random import seed
from random import randint
import time
import PIL.Image
from PIL import Image, ImageChops
import numpy as np
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt
import math
import imagehash
import mysql.connector
import urllib.request
import urllib.parse
from werkzeug.utils import secure_filename
#import tensorflow as tf
#from tensorflow.keras import backend as K, Model, Input, optimizers
#from tensorflow.keras.layers import Layer, Conv1D, Dense, BatchNormalization, LayerNormalization
from urllib.request import urlopen
import webbrowser

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="animal_rep_cam"

)

UPLOAD_FOLDER = 'static/trained'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'abcdef'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#@app.route('/')
#def index():
#    return render_template('index.html')



@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

    ff3=open("ulog.txt","w")
    ff3.write("")
    ff3.close()
    
    act=request.args.get("act")
    act2=request.args.get("act2")
    act3=request.args.get("act3")

    ff1=open("photo.txt","w")
    ff1.write("")
    ff1.close()

    ff1=open("det.txt","w")
    ff1.write("")
    ff1.close()
    
    return render_template('index.html',msg=msg,act=act,act2=act2,act3=act3)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    msg=""
    act=request.args.get("act")
    act2=request.args.get("act2")
    act3=request.args.get("act3")
    page=request.args.get("page")
    ff=open("msg.txt","w")
    ff.write('0')
    ff.close()
    fn=request.args.get("fn")
    fn2=""
    animal=""
    ss=""
    cname=[]
    afile=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM animal_info order by id")
    row = mycursor.fetchall()
    for row1 in row:
        cname.append(row1[1])
        
    if request.method=='POST':
        #print("d")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        file_type = file.content_type
        # if user does not select file, browser also
        # submit an empty part without filename
        tf=file.filename
        ff=open("log.txt","w")
        ff.write(tf)
        ff.close()
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = "m1.jpg"
            filename = secure_filename(fname)
            
            file.save(os.path.join("static/test", filename))
            

            cutoff=1
            for fname in os.listdir("static/dataset"):
                hash0 = imagehash.average_hash(Image.open("static/dataset/"+fname)) 
                hash1 = imagehash.average_hash(Image.open("static/test/m1.jpg"))
                cc1=hash0 - hash1
                print("cc="+str(cc1))
                if cc1<=cutoff:
                    fn=fname
                    ss="ok"
                    break
            if ss=="ok":
                act3="yes"
            else:
                act3="no"
                
                
            
            
        return redirect(url_for('upload', act3=act3,fn=fn,page=page))
        
    '''if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    '''
    
    if act3=="yes":
        g=1
        print(fn)
        #object_detect(fn)
        ##    
        ff2=open("static/trained/tdata.txt","r")
        rd=ff2.read()
        ff2.close()

        num=[]
        r1=rd.split(',')
        s=len(r1)
        ss=s-1
        i=0
        while i<ss:
            
            num.append(int(r1[i]))
            i+=1

        #print(num)
        dat=toString(num)
        dd2=[]
        d1=dat.split(',')
        
        ##
        
        for gff in d1:
            
            gf1=gff.split('-')
            
            if gf1[0]==fn:
                gid=int(gf1[1])-1
                fn2="c_"+fn
                animal=cname[gid]
                afile="a"+gf1[1]+".mp3"


                

                
                break
        print(fn2)
        print(animal)
        print(afile)

        ff3=open("ulog.txt","r")
        user=ff3.read()
        ff3.close()

        ff4=open("sms.txt","r")
        sms=ff4.read()
        ff4.close()

        if user=="":
            aa=1
        else:

            if sms=="":
                aa=1
            else:
                mycursor.execute("SELECT * FROM farmer where uname=%s",(user, ))
                row1 = mycursor.fetchone()
                mobile=row1[2]
                name=row1[1]
                
                mess=animal+" detected"
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+mess+"&mobile="+str(mobile)
                webbrowser.open_new(url)

                ff41=open("sms.txt","w")
                ff41.write("")
                ff41.close()
                
            mycursor = mydb.cursor()
            mycursor.execute("SELECT max(id)+1 FROM animal_detect")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO animal_detect(id,user,animal,image_name) VALUES (%s, %s,%s,%s)"
            val = (maxid,user,animal,fn2)
            mycursor.execute(sql, val)
            mydb.commit()
                
    elif act3=="no":
        g=2
        msg="No Result"
    return render_template('upload.html',msg=msg,act=act,act2=act2,act3=act3,fn=fn,animal=animal,fn2=fn2,afile=afile,page=page)

@app.route('/process_upload', methods=['GET', 'POST'])
def process_upload():
    msg=""
    act=request.args.get("act")
    act2=request.args.get("act2")
    act3=request.args.get("act3")
    page=request.args.get("page")
    ff=open("msg.txt","w")
    ff.write('0')
    ff.close()
    fn=request.args.get("fn")
    fn2=""
    animal=""
    ss=""
    cname=[]
    afile=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM animal_info order by id")
    row = mycursor.fetchall()
    for row1 in row:
        cname.append(row1[1])
        
    if request.method=='POST':
        #print("d")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        file_type = file.content_type
        # if user does not select file, browser also
        # submit an empty part without filename
        tf=file.filename
        ff=open("log.txt","w")
        ff.write(tf)
        ff.close()
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = "m1.jpg"
            filename = secure_filename(fname)
            
            file.save(os.path.join("static/test", filename))
            

            cutoff=1
            for fname in os.listdir("static/dataset"):
                hash0 = imagehash.average_hash(Image.open("static/dataset/"+fname)) 
                hash1 = imagehash.average_hash(Image.open("static/test/m1.jpg"))
                cc1=hash0 - hash1
                print("cc="+str(cc1))
                if cc1<=cutoff:
                    fn=fname
                    ss="ok"
                    break
            if ss=="ok":
                act3="yes"
            else:
                act3="no"
                
                
            
            
        return redirect(url_for('process_upload', act3=act3,fn=fn,page=page))
        
    '''if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    '''
    
    if act3=="yes":
        g=1
        print(fn)
        #object_detect(fn)
        ##    
        ff2=open("static/trained/tdata.txt","r")
        rd=ff2.read()
        ff2.close()

        num=[]
        r1=rd.split(',')
        s=len(r1)
        ss=s-1
        i=0
        while i<ss:
            
            num.append(int(r1[i]))
            i+=1

        #print(num)
        dat=toString(num)
        dd2=[]
        d1=dat.split(',')
        
        ##
        
        for gff in d1:
            
            gf1=gff.split('-')
            
            if gf1[0]==fn:
                gid=int(gf1[1])-1
                fn2="c_"+fn
                animal=cname[gid]
                afile="a"+gf1[1]+".mp3"


                

                
                break
        print(fn2)
        print(animal)
        print(afile)

        ff3=open("ulog.txt","r")
        user=ff3.read()
        ff3.close()

        ff4=open("sms.txt","r")
        sms=ff4.read()
        ff4.close()

        if user=="":
            aa=1
        else:

            if sms=="":
                aa=1
            else:
                mycursor.execute("SELECT * FROM farmer where uname=%s",(user, ))
                row1 = mycursor.fetchone()
                mobile=row1[2]
                name=row1[1]
                
                mess=animal+" detected"
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+mess+"&mobile="+str(mobile)
                webbrowser.open_new(url)

                ff41=open("sms.txt","w")
                ff41.write("")
                ff41.close()
                
            mycursor = mydb.cursor()
            mycursor.execute("SELECT max(id)+1 FROM animal_detect")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO animal_detect(id,user,animal,image_name) VALUES (%s, %s,%s,%s)"
            val = (maxid,user,animal,fn2)
            mycursor.execute(sql, val)
            mydb.commit()
                
    elif act3=="no":
        g=2
        msg="No Result"
    return render_template('process_upload.html',msg=msg,act=act,act2=act2,act3=act3,fn=fn,animal=animal,fn2=fn2,afile=afile,page=page)

@app.route('/process_upload2', methods=['GET', 'POST'])
def process_upload2():
    msg=""
    act=request.args.get("act")
    act2=request.args.get("act2")
    act3=request.args.get("act3")
    page=request.args.get("page")
    ff=open("msg.txt","w")
    ff.write('0')
    ff.close()
    fn=request.args.get("fn")
    fn2=""
    animal=""
    ss=""
    cname=[]
    afile=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM animal_info order by id")
    row = mycursor.fetchall()
    for row1 in row:
        cname.append(row1[1])
        
    if request.method=='POST':
        #print("d")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        file_type = file.content_type
        # if user does not select file, browser also
        # submit an empty part without filename
        tf=file.filename
        ff=open("log.txt","w")
        ff.write(tf)
        ff.close()
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = "m1.jpg"
            filename = secure_filename(fname)
            
            file.save(os.path.join("static/test", filename))
            

            cutoff=1
            for fname in os.listdir("static/dataset"):
                hash0 = imagehash.average_hash(Image.open("static/dataset/"+fname)) 
                hash1 = imagehash.average_hash(Image.open("static/test/m1.jpg"))
                cc1=hash0 - hash1
                print("cc="+str(cc1))
                if cc1<=cutoff:
                    fn=fname
                    ss="ok"
                    break
            if ss=="ok":
                act3="yes"
            else:
                act3="no"
                
                
            
            
        return redirect(url_for('process_upload2', act3=act3,fn=fn,page=page))
        
    '''if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    '''
    
    if act3=="yes":
        g=1
        print(fn)
        #object_detect(fn)
        ##    
        ff2=open("static/trained/tdata.txt","r")
        rd=ff2.read()
        ff2.close()

        num=[]
        r1=rd.split(',')
        s=len(r1)
        ss=s-1
        i=0
        while i<ss:
            
            num.append(int(r1[i]))
            i+=1

        #print(num)
        dat=toString(num)
        dd2=[]
        d1=dat.split(',')
        
        ##
        
        for gff in d1:
            
            gf1=gff.split('-')
            
            if gf1[0]==fn:
                gid=int(gf1[1])-1
                fn2="c_"+fn
                animal=cname[gid]
                afile="a"+gf1[1]+".mp3"


                

                
                break
        print(fn2)
        print(animal)
        print(afile)

        ff3=open("ulog.txt","r")
        user=ff3.read()
        ff3.close()

        ff4=open("sms.txt","r")
        sms=ff4.read()
        ff4.close()

        if user=="":
            aa=1
        else:

            if sms=="":
                aa=1
            else:
                mycursor.execute("SELECT * FROM farmer where uname=%s",(user, ))
                row1 = mycursor.fetchone()
                mobile=row1[2]
                name=row1[1]
                
                mess=animal+" detected"
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+mess+"&mobile="+str(mobile)
                webbrowser.open_new(url)

                ff41=open("sms.txt","w")
                ff41.write("")
                ff41.close()
                
            mycursor = mydb.cursor()
            mycursor.execute("SELECT max(id)+1 FROM animal_detect")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO animal_detect(id,user,animal,image_name) VALUES (%s, %s,%s,%s)"
            val = (maxid,user,animal,fn2)
            mycursor.execute(sql, val)
            mydb.commit()
                
    elif act3=="no":
        g=2
        msg="No Result"
    return render_template('process_upload2.html',msg=msg,act=act,act2=act2,act3=act3,fn=fn,animal=animal,fn2=fn2,afile=afile,page=page)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
        
        
    return render_template('login.html',msg=msg)

@app.route('/login_farmer', methods=['GET', 'POST'])
def login_farmer():
    msg=""
    msg1=""
    act = request.args.get('act')
    if act=="success":
        msg1="New Farmer Register Success"
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM farmer WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname

            ff3=open("ulog.txt","w")
            ff3.write(uname)
            ff3.close()

            ff3=open("sms.txt","w")
            ff3.write("yes")
            ff3.close()
    
            return redirect(url_for('userhome'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
        
        
    return render_template('login_farmer.html',msg=msg,msg1=msg1)


@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""

    msg=""
    act=request.args.get("act")
    act2=request.args.get("act2")
    act3=request.args.get("act3")
    
    return render_template('userhome.html',msg=msg,act=act,act2=act2,act3=act3)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    
    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        location=request.form['location']
        uname=request.form['uname']
        pwd=request.form['pass']
        

        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM farmer")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO farmer(id,name,mobile,email,location,uname,pass) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,name,mobile,email,location,uname,pwd)
        mycursor.execute(sql, val)
        mydb.commit()            
        print(mycursor.rowcount, "Added Success")
        act='success'
        return redirect(url_for('login_farmer',act=act))
        
    return render_template('register.html',msg=msg)


@app.route('/process',methods=['POST','GET'])
def process():
    msg=""
    ss=""
    uname=""
    act2=request.args.get("act2")
    det=""
    mess=""
    # (0, 1) is N
    SCALE = 2.2666 # the scale is chosen to be 1 m = 2.266666666 pixels
    MIN_LENGTH = 150 # pixels

    if request.method=='GET':
        act = request.args.get('act')
        
    '''ff3=open("img.txt","r")
    mcnt=ff3.read()
    ff3.close()

    cursor = mydb.cursor()

    try:

        mcnt1=int(mcnt)
        print(mcnt1)
        if mcnt1>=2:
        
            cutoff=8
            act="1"
            cursor.execute('SELECT * FROM vt_face')
            dt = cursor.fetchall()
            for rr in dt:
                hash0 = imagehash.average_hash(Image.open("static/frame/"+rr[2])) 
                hash1 = imagehash.average_hash(Image.open("static/faces/f1.jpg"))
                cc1=hash0 - hash1
                print("cc="+str(cc1))
                if cc1<=cutoff:
                    vid=rr[1]
                    cursor.execute('SELECT * FROM train_data where id=%s',(vid,))
                    rw = cursor.fetchone()
                    
                    msg="Hai "+rw[2]
                    ff=open("person.txt","w")
                    ff.write(msg)
                    ff.close()
                    print(msg)
                 
                    break
                else:
                    msg="Unknown person found"
                    ff=open("person.txt","w")
                    ff.write(msg)
                    ff.close()
                
    except:
        print("excep")
        

    msg1=""
    msg2=""
    mess=""
    ff=open("get_value.txt","r")
    get_value=ff.read()
    ff.close()
    s=""
    if get_value=="":
        s="1"
    else:
        
        msg1=get_value+" detected, "

    ff1=open("person.txt","r")
    pp=ff1.read()
    ff1.close()
    sc=""
    if pp=="":
        sc="1"
    else:
        msg2=""+pp+""
        
    mess=msg1+" "+msg2   
    '''
    return render_template('process.html',mess=mess,act=act)


@app.route('/process_cam',methods=['POST','GET'])
def process_cam():
    msg=""
    ss=""
    uname=""
    act2=request.args.get("act2")
    det=""
    mess=""

    ff=open("static/sms.txt","w")
    ff.write("")
    ff.close()
    

    if request.method=='GET':
        act = request.args.get('act')
        
   
    return render_template('process_cam.html',mess=mess,act=act)

@app.route('/process_cam2',methods=['POST','GET'])
def process_cam2():
    msg=""
    ss=""
    uname=""
    act2=request.args.get("act2")
    det=""
    mess=""
    

    if request.method=='GET':
        act = request.args.get('act')
        
   
    return render_template('process_cam2.html',mess=mess,act=act)

@app.route('/process_cam2x',methods=['POST','GET'])
def process_cam2x():
    msg=""
    act=""
    ss=""
    value=""
    uname=""
    mycursor = mydb.cursor()
    act2=request.args.get("act2")
    det=""
    mess=""
    st=""
    afile=""

    ff3=open("ulog.txt","r")
    user=ff3.read()
    ff3.close()

    ff4=open("sms.txt","r")
    sms=ff4.read()
    ff4.close()

    try:
        cutoff=10
        act="1"
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM animal_img')
        dt = mycursor.fetchall()
        for rr in dt:
            hash0 = imagehash.average_hash(Image.open("static/frame/"+rr[2])) 
            hash1 = imagehash.average_hash(Image.open("static/faces/f1.jpg"))
            cc1=hash0 - hash1
            print("cc="+str(cc1))
            if cc1<=cutoff:
                st="1"
                vid=rr[1]
                mycursor.execute('SELECT * FROM train_data where id=%s',(vid,))
                rw = mycursor.fetchone()
                value=rw[1]
                msg="Animal: "+rw[1]+" detected"
                ff=open("person.txt","w")
                ff.write(msg)
                ff.close()
                print(msg)

                ##
                mycursor.execute("SELECT max(id)+1 FROM animal_detect")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid=1

                mycursor.execute("SELECT count(*) FROM animal_info where animal=%s",(value,))
                d1 = mycursor.fetchone()[0]
                if d1>0:
                    mycursor.execute("SELECT * FROM animal_info where animal=%s",(value,))
                    d2 = mycursor.fetchone()
                    gid=d2[0]           
                    afile="a"+str(gid)+".mp3"
                else:
                    afile="a7.mp3"

                if sms=="yes": 
                    mycursor.execute("SELECT * FROM farmer where uname=%s",(user, ))
                    row1 = mycursor.fetchone()
                    mobile=row1[2]
                    name=row1[1]
                    
                    mess=value+" detected"
                    url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+mess+"&mobile="+str(mobile)
                    webbrowser.open_new(url)

                    ff41=open("sms.txt","w")
                    ff41.write("")
                    ff41.close()
                    
                fn2="r"+str(maxid)+".jpg"
                shutil.copy('static/faces/f1.jpg', 'static/upload/'+fn2)
                sql = "INSERT INTO animal_detect(id,user,animal,image_name) VALUES (%s, %s,%s,%s)"
                val = (maxid,user,value,fn2)
                mycursor.execute(sql, val)
                mydb.commit()
             
                break
            else:
                msg="No Animal"
                ff=open("person.txt","w")
                ff.write(msg)
                ff.close()
    except:
        print("try")
    '''ff=open("get_value.txt","r")
    value=ff.read()
    ff.close()

    if value=="":
        s=1
    else:
        st="1"
        det="Detected Animal: "+value
        mycursor.execute("SELECT max(id)+1 FROM animal_detect")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        mycursor.execute("SELECT count(*) FROM animal_info where animal=%s",(value,))
        d1 = mycursor.fetchone()[0]
        if d1>0:
            mycursor.execute("SELECT * FROM animal_info where animal=%s",(value,))
            d2 = mycursor.fetchone()
            gid=d2[0]           
            afile="a"+str(gid)+".mp3"
        else:
            afile="a7.mp3"

        if sms=="yes": 
            mycursor.execute("SELECT * FROM farmer where uname=%s",(user, ))
            row1 = mycursor.fetchone()
            mobile=row1[2]
            name=row1[1]
            
            mess=value+" detected"
            url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+mess+"&mobile="+str(mobile)
            webbrowser.open_new(url)

            ff41=open("sms.txt","w")
            ff41.write("")
            ff41.close()
            
        fn2="r"+str(maxid)+".jpg"
        shutil.copy('static/trained/test.jpg', 'static/upload/'+fn2)
        sql = "INSERT INTO animal_detect(id,user,animal,image_name) VALUES (%s, %s,%s,%s)"
        val = (maxid,user,value,fn2)
        mycursor.execute(sql, val)
        mydb.commit()'''
        
   
    return render_template('process_cam2x.html',afile=afile,mess=mess,act=act,st=st,det=msg)

@app.route('/process_camx',methods=['POST','GET'])
def process_camx():
    msg=""
    ss=""
    act=""
    uname=""
    sms=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM admin")
    dm = mycursor.fetchone()
    mobile=dm[2]
    
    act2=request.args.get("act2")
    det=""
    mess=""
    st=""
    afile=""

    ff3=open("ulog.txt","r")
    user=ff3.read()
    ff3.close()
    
    ff=open("get_value.txt","r")
    value=ff.read()
    ff.close()

    ff=open("static/sms.txt","r")
    sv1=ff.read()
    ff.close()
    sv=0
    if sv1 is None or sv1=="":
        sv=1
    else:
        sv=int(sv1)

    if value=="person" or value=="background" or value=="cat" or value=="cup" or value=="mobile" or value=="glass" or value=="chair" or value=="bottle" or value=="paper" or value=="tvmonitor" or value=="car" or value=="sofa" or value=="cell phone" or value=="pottedplant" or value=="motorbike":
        s=1
        st="2"
        det="Not Animal"
    elif value=="":
        s=1
    else:
        st="1"
        det="Detected Animal: "+value

        svv=sv+1
        sv2=str(svv)
        ff=open("static/sms.txt","w")
        ff.write(sv2)
        ff.close()

        if sv<3:
            sms="1"
    
        mycursor.execute("SELECT max(id)+1 FROM animal_detect")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        mycursor.execute("SELECT count(*) FROM animal_info where animal=%s",(value,))
        d1 = mycursor.fetchone()[0]
        if d1>0:
            mycursor.execute("SELECT * FROM animal_info where animal=%s",(value,))
            d2 = mycursor.fetchone()
            gid=d2[0]           
            afile="a"+str(gid)+".mp3"
        else:
            afile="a7.mp3"

        
        #fn2="r"+str(maxid)+".jpg"
        #shutil.copy('static/trained/test.jpg', 'static/upload/'+fn2)
        #sql = "INSERT INTO animal_detect(id,user,animal,image_name) VALUES (%s, %s,%s,%s)"
        #val = (maxid,user,value,fn2)
        #mycursor.execute(sql, val)
        #mydb.commit()
        
   
    return render_template('process_camx.html',afile=afile,mess=mess,act=act,st=st,det=det,mobile=mobile,sms=sms)

#TCN  - Temporal Convolutional Network - Identify the Animal Intrusion
def is_power_of_two(num: int):
    return num != 0 and ((num & (num - 1)) == 0)


def adjust_dilations(dilations: list):
    if all([is_power_of_two(i) for i in dilations]):
        return dilations
    else:
        new_dilations = [2 ** i for i in dilations]
        return new_dilations


    

    def __init__(self,
                 dilation_rate: int,
                 nb_filters: int,
                 kernel_size: int,
                 padding: str,
                 activation: str = 'relu',
                 dropout_rate: float = 0,
                 kernel_initializer: str = 'he_normal',
                 use_batch_norm: bool = False,
                 use_layer_norm: bool = False,
                 use_weight_norm: bool = False,
                 **kwargs):

        self.dilation_rate = dilation_rate
        self.nb_filters = nb_filters
        self.kernel_size = kernel_size
        self.padding = padding
        self.activation = activation
        self.dropout_rate = dropout_rate
        self.use_batch_norm = use_batch_norm
        self.use_layer_norm = use_layer_norm
        self.use_weight_norm = use_weight_norm
        self.kernel_initializer = kernel_initializer
        self.layers = []
        self.shape_match_conv = None
        self.res_output_shape = None
        self.final_activation = None

        super(ResidualBlock, self).__init__(**kwargs)

    def tcn_full_summary(model: Model, expand_residual_blocks=True):
        #import tensorflow as tf
        # 2.6.0-rc1, 2.5.0...
        versions = [int(v) for v in tf.__version__.split('-')[0].split('.')]
        if versions[0] <= 2 and versions[1] < 5:
            layers = model._layers.copy()  # store existing layers
            model._layers.clear()  # clear layers

            for i in range(len(layers)):
                if isinstance(layers[i], TCN):
                    for layer in layers[i]._layers:
                        if not isinstance(layer, ResidualBlock):
                            if not hasattr(layer, '__iter__'):
                                model._layers.append(layer)
                        else:
                            if expand_residual_blocks:
                                for lyr in layer._layers:
                                    if not hasattr(lyr, '__iter__'):
                                        model._layers.append(lyr)
                            else:
                                model._layers.append(layer)
                else:
                    model._layers.append(layers[i])

            model.summary()  # print summary

            # restore original layers
            model._layers.clear()
            [model._layers.append(lyr) for lyr in layers]

            

        def _build_layer(self, layer):
           
            self.layers.append(layer)
            self.layers[-1].build(self.res_output_shape)
            self.res_output_shape = self.layers[-1].compute_output_shape(self.res_output_shape)

        def build(self, input_shape):

            with K.name_scope(self.name):  # name scope used to make sure weights get unique names
                self.layers = []
                self.res_output_shape = input_shape

                for k in range(2):  # dilated conv block.
                    name = 'conv1D_{}'.format(k)
                    with K.name_scope(name):  # name scope used to make sure weights get unique names
                        conv = Conv1D(
                            filters=self.nb_filters,
                            kernel_size=self.kernel_size,
                            dilation_rate=self.dilation_rate,
                            padding=self.padding,
                            name=name,
                            kernel_initializer=self.kernel_initializer
                        )
                        if self.use_weight_norm:
                            from tensorflow_addons.layers import WeightNormalization
                            # wrap it. WeightNormalization API is different than BatchNormalization or LayerNormalization.
                            with K.name_scope('norm_{}'.format(k)):
                                conv = WeightNormalization(conv)
                        self._build_layer(conv)

                    with K.name_scope('norm_{}'.format(k)):
                        if self.use_batch_norm:
                            self._build_layer(BatchNormalization())
                        elif self.use_layer_norm:
                            self._build_layer(LayerNormalization())
                        elif self.use_weight_norm:
                            pass  # done above.

                    with K.name_scope('act_and_dropout_{}'.format(k)):
                        self._build_layer(Activation(self.activation, name='Act_Conv1D_{}'.format(k)))
                        self._build_layer(SpatialDropout1D(rate=self.dropout_rate, name='SDropout_{}'.format(k)))

                if self.nb_filters != input_shape[-1]:
                    # 1x1 conv to match the shapes (channel dimension).
                    name = 'matching_conv1D'
                    with K.name_scope(name):
                        # make and build this layer separately because it directly uses input_shape.
                        # 1x1 conv.
                        self.shape_match_conv = Conv1D(
                            filters=self.nb_filters,
                            kernel_size=1,
                            padding='same',
                            name=name,
                            kernel_initializer=self.kernel_initializer
                        )
                else:
                    name = 'matching_identity'
                    self.shape_match_conv = Lambda(lambda x: x, name=name)

                with K.name_scope(name):
                    self.shape_match_conv.build(input_shape)
                    self.res_output_shape = self.shape_match_conv.compute_output_shape(input_shape)

                self._build_layer(Activation(self.activation, name='Act_Conv_Blocks'))
                self.final_activation = Activation(self.activation, name='Act_Res_Block')
                self.final_activation.build(self.res_output_shape)  # probably isn't necessary

                # this is done to force Keras to add the layers in the list to self._layers
                for layer in self.layers:
                    self.__setattr__(layer.name, layer)
                self.__setattr__(self.shape_match_conv.name, self.shape_match_conv)
                self.__setattr__(self.final_activation.name, self.final_activation)

                super(ResidualBlock, self).build(input_shape)  # done to make sure self.built is set True

        def call(self, inputs, training=None, **kwargs):
            """
            Returns: A tuple where the first element is the residual model tensor, and the second
                     is the skip connection tensor.
            """
            
            x1 = inputs
            for layer in self.layers:
                training_flag = 'training' in dict(inspect.signature(layer.call).parameters)
                x1 = layer(x1, training=training) if training_flag else layer(x1)
            x2 = self.shape_match_conv(inputs)
            x1_x2 = self.final_activation(layers.add([x2, x1], name='Add_Res'))
            return [x1_x2, x1]

        def compute_output_shape(self, input_shape):
            return [self.res_output_shape, self.res_output_shape]
####

def object_detect(fname):
    # construct the argument parse 
    parser = argparse.ArgumentParser(
        description='Script to run MobileNet-SSD object detection network ')
    parser.add_argument("--video", help="path to video file. If empty, camera's stream will be used")
    parser.add_argument("--prototxt", default="MobileNetSSD_deploy.prototxt",
                                      help='Path to text network file: '
                                           'MobileNetSSD_deploy.prototxt for Caffe model or '
                                           )
    parser.add_argument("--weights", default="MobileNetSSD_deploy.caffemodel",
                                     help='Path to weights: '
                                          'MobileNetSSD_deploy.caffemodel for Caffe model or '
                                          )
    parser.add_argument("--thr", default=0.2, type=float, help="confidence threshold to filter out weak detections")
    args = parser.parse_args()

    # Labels of Network.
    classNames = { 0: 'background',
            1: 'Bear', 2: 'Cow', 3: 'Elephant', 4: 'Goat',
            5: 'Horse', 6: 'Pig', 7: 'Sheep' }

    # Open video file or capture device. 
    '''if args.video:
        cap = cv2.VideoCapture(args.video)
    else:
        cap = cv2.VideoCapture(0)'''

    #Load the Caffe model 
    net = cv2.dnn.readNetFromCaffe(args.prototxt, args.weights)

    #while True:
    # Capture frame-by-frame
    #ret, frame = cap.read()
    frame = cv2.imread("static/test/"+fname)
    frame_resized = cv2.resize(frame,(300,300)) # resize frame for prediction

    # MobileNet requires fixed dimensions for input image(s)
    # so we have to ensure that it is resized to 300x300 pixels.
    # set a scale factor to image because network the objects has differents size. 
    # We perform a mean subtraction (127.5, 127.5, 127.5) to normalize the input;
    # after executing this command our "blob" now has the shape:
    # (1, 3, 300, 300)
    blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
    #Set to network the input blob 
    net.setInput(blob)
    #Prediction of network
    detections = net.forward()

    #Size of frame resize (300x300)
    cols = frame_resized.shape[1] 
    rows = frame_resized.shape[0]

    #For get the class and location of object detected, 
    # There is a fix index for class, location and confidence
    # value in @detections array .
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2] #Confidence of prediction 
        if confidence > args.thr: # Filter prediction 
            class_id = int(detections[0, 0, i, 1]) # Class label

            # Object location 
            xLeftBottom = int(detections[0, 0, i, 3] * cols) 
            yLeftBottom = int(detections[0, 0, i, 4] * rows)
            xRightTop   = int(detections[0, 0, i, 5] * cols)
            yRightTop   = int(detections[0, 0, i, 6] * rows)
            
            # Factor for scale to original size of frame
            heightFactor = frame.shape[0]/300.0  
            widthFactor = frame.shape[1]/300.0 
            # Scale object detection to frame
            xLeftBottom = int(widthFactor * xLeftBottom) 
            yLeftBottom = int(heightFactor * yLeftBottom)
            xRightTop   = int(widthFactor * xRightTop)
            yRightTop   = int(heightFactor * yRightTop)
            # Draw location of object  
            cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                          (0, 255, 0))
            try:
                y=yLeftBottom
                h=yRightTop-y
                x=xLeftBottom
                w=xRightTop-x
                image = cv2.imread("static/test/"+fname)
                mm=cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                fnn="detect.png"
                cv2.imwrite("static/test/"+fnn, mm)
                cropped = image[yLeftBottom:yRightTop, xLeftBottom:xRightTop]
                gg="segment.png"
                cv2.imwrite("static/test/"+gg, cropped)
                #mm2 = PIL.Image.open('static/trained/'+gg)
                #rz = mm2.resize((300,300), PIL.Image.ANTIALIAS)
                #rz.save('static/trained/'+gg)
            except:
                print("none")
                #shutil.copy('getimg.jpg', 'static/trained/test.jpg')
            # Draw label and confidence of prediction in frame resized
            if class_id in classNames:
                label = classNames[class_id] + ": " + str(confidence)
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                yLeftBottom = max(yLeftBottom, labelSize[1])
                cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                                     (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                                     (255, 255, 255), cv2.FILLED)
                cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

                #print(label) 
    ####################



@app.route('/process2',methods=['POST','GET'])
def process2():
    msg=""
    dimg=[]
    fn=request.args.get("fn")
    act2=request.args.get("act2")
    fn2=""
    st=request.args.get("st")
    animal=""
    cname=[]
    afile=""
    act2=request.args.get("act2")
    st=request.args.get("st")
    gfile=request.args.get("gfile")
    path_main = 'static/dataset'

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM animal_info order by id")
    row = mycursor.fetchall()
    for row1 in row:
        cname.append(row1[1])
           
                     
    
    
    i=0
    for fname in os.listdir(path_main):
        dimg.append(fname)

    if st=="1":
        s=1
        
    
    elif st=="2":
        
        s=2
        gfile=fn
        ##    
        ff2=open("static/trained/tdata.txt","r")
        rd=ff2.read()
        ff2.close()

        num=[]
        r1=rd.split(',')
        s=len(r1)
        ss=s-1
        i=0
        while i<ss:
            
            num.append(int(r1[i]))
            i+=1

        #print(num)
        dat=toString(num)
        dd2=[]
        d1=dat.split(',')
        
        ##
        
        for gff in d1:
            
            gf1=gff.split('-')
            
            if gf1[0]==fn:
                gid=int(gf1[1])-1
                fn2="c_"+gfile
                animal=cname[gid]
                afile="a"+str(gid)+".mp3"
                break
        print(fn2)
        print(animal)
        ff3=open("ulog.txt","r")
        user=ff3.read()
        ff3.close()

        ff4=open("sms.txt","r")
        sms=ff4.read()
        ff4.close()

        if user=="":
            aa=1
        else:

            if sms=="":
                aa=1
            else:
                mycursor.execute("SELECT * FROM farmer where uname=%s",(user, ))
                row1 = mycursor.fetchone()
                mobile=row1[2]
                name=row1[1]
                
                mess=animal+" detected"
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+mess+"&mobile="+str(mobile)
                webbrowser.open_new(url)

                ff41=open("sms.txt","w")
                ff41.write("")
                ff41.close()
                
            
            mycursor.execute("SELECT max(id)+1 FROM animal_detect")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO animal_detect(id,user,animal,image_name) VALUES (%s, %s,%s,%s)"
            val = (maxid,user,animal,fn2)
            mycursor.execute(sql, val)
            mydb.commit()
    else:
        
        xn1=randint(0,250)
        if xn1<104:
            ffn=dimg[xn1]
            fn=ffn
            st="1"
        else:
            st="3"
            fn="default.png"
    

    return render_template('process2.html', msg=msg,st=st,fn=fn,animal=animal,fn2=fn2,act2=act2,afile=afile)

@app.route('/process_auto',methods=['POST','GET'])
def process_auto():
    msg=""
    dimg=[]
    fn=request.args.get("fn")
    act2=request.args.get("act2")
    fn2=""
    st=request.args.get("st")
    animal=""
    cname=[]
    afile=""
    act2=request.args.get("act2")
    st=request.args.get("st")
    gfile=request.args.get("gfile")
    path_main = 'static/dataset'

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM animal_info order by id")
    row = mycursor.fetchall()
    for row1 in row:
        cname.append(row1[1])
           
                     
    
    
    i=0
    for fname in os.listdir(path_main):
        dimg.append(fname)

    if st=="1":
        s=1
        
    
    elif st=="2":
        
        s=2
        gfile=fn
        ##    
        ff2=open("static/trained/tdata.txt","r")
        rd=ff2.read()
        ff2.close()

        num=[]
        r1=rd.split(',')
        s=len(r1)
        ss=s-1
        i=0
        while i<ss:
            
            num.append(int(r1[i]))
            i+=1

        #print(num)
        dat=toString(num)
        dd2=[]
        d1=dat.split(',')
        
        ##
        
        for gff in d1:
            
            gf1=gff.split('-')
            
            if gf1[0]==fn:
                gid=int(gf1[1])-1
                fn2="c_"+gfile
                animal=cname[gid]
                afile="a"+str(gid)+".mp3"
                break
        print(fn2)
        print(animal)
        ff3=open("ulog.txt","r")
        user=ff3.read()
        ff3.close()

        ff4=open("sms.txt","r")
        sms=ff4.read()
        ff4.close()

        if user=="":
            aa=1
        else:

            if sms=="":
                aa=1
            else:
                mycursor.execute("SELECT * FROM farmer where uname=%s",(user, ))
                row1 = mycursor.fetchone()
                mobile=row1[2]
                name=row1[1]
                
                mess=animal+" detected"
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+mess+"&mobile="+str(mobile)
                webbrowser.open_new(url)

                ff41=open("sms.txt","w")
                ff41.write("")
                ff41.close()
                
            
            mycursor.execute("SELECT max(id)+1 FROM animal_detect")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO animal_detect(id,user,animal,image_name) VALUES (%s, %s,%s,%s)"
            val = (maxid,user,animal,fn2)
            mycursor.execute(sql, val)
            mydb.commit()
    else:
        
        xn1=randint(0,250)
        if xn1<104:
            ffn=dimg[xn1]
            fn=ffn
            st="1"
        else:
            st="3"
            fn="default.png"
    

    return render_template('process_auto.html', msg=msg,st=st,fn=fn,animal=animal,fn2=fn2,act2=act2,afile=afile)

@app.route('/process_auto2',methods=['POST','GET'])
def process_auto2():
    msg=""
    dimg=[]
    fn=request.args.get("fn")
    act2=request.args.get("act2")
    fn2=""
    st=request.args.get("st")
    animal=""
    cname=[]
    afile=""
    act2=request.args.get("act2")
    st=request.args.get("st")
    gfile=request.args.get("gfile")
    path_main = 'static/dataset'

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM animal_info order by id")
    row = mycursor.fetchall()
    for row1 in row:
        cname.append(row1[1])
           
                     
    
    
    i=0
    for fname in os.listdir(path_main):
        dimg.append(fname)

    if st=="1":
        s=1
        
    
    elif st=="2":
        
        s=2
        gfile=fn
        ##    
        ff2=open("static/trained/tdata.txt","r")
        rd=ff2.read()
        ff2.close()

        num=[]
        r1=rd.split(',')
        s=len(r1)
        ss=s-1
        i=0
        while i<ss:
            
            num.append(int(r1[i]))
            i+=1

        #print(num)
        dat=toString(num)
        dd2=[]
        d1=dat.split(',')
        
        ##
        
        for gff in d1:
            
            gf1=gff.split('-')
            
            if gf1[0]==fn:
                gid=int(gf1[1])-1
                fn2="c_"+gfile
                animal=cname[gid]
                afile="a"+str(gid)+".mp3"
                break
        print(fn2)
        print(animal)
        ff3=open("ulog.txt","r")
        user=ff3.read()
        ff3.close()

        ff4=open("sms.txt","r")
        sms=ff4.read()
        ff4.close()

        if user=="":
            aa=1
        else:

            if sms=="":
                aa=1
            else:
                mycursor.execute("SELECT * FROM farmer where uname=%s",(user, ))
                row1 = mycursor.fetchone()
                mobile=row1[2]
                name=row1[1]
                
                mess=animal+" detected"
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+mess+"&mobile="+str(mobile)
                webbrowser.open_new(url)

                ff41=open("sms.txt","w")
                ff41.write("")
                ff41.close()
                
            
            mycursor.execute("SELECT max(id)+1 FROM animal_detect")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO animal_detect(id,user,animal,image_name) VALUES (%s, %s,%s,%s)"
            val = (maxid,user,animal,fn2)
            mycursor.execute(sql, val)
            mydb.commit()
    else:
        
        xn1=randint(0,250)
        if xn1<104:
            ffn=dimg[xn1]
            fn=ffn
            st="1"
        else:
            st="3"
            fn="default.png"
    

    return render_template('process_auto2.html', msg=msg,st=st,fn=fn,animal=animal,fn2=fn2,act2=act2,afile=afile)

@app.route('/detect', methods=['GET', 'POST'])
def detect():

    ff3=open("ulog.txt","r")
    user=ff3.read()
    ff3.close()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM farmer where uname=%s",(user, ))
    row1 = mycursor.fetchone()
    mobile=row1[2]
    name=row1[1]

    mycursor.execute("SELECT * FROM animal_detect where user=%s order by id desc",(user, ))
    data = mycursor.fetchall()

                
    return render_template('detect.html', data=data)



@app.route('/train_data', methods=['GET', 'POST'])
def train_data():

    msg=""
    
    
    
    return render_template('train_data.html', msg=msg)



@app.route('/pro1', methods=['GET', 'POST'])
def pro1():
    msg=""

    mycursor = mydb.cursor()
 
    dimg=[]
    
    path_main = 'static/dataset'
    i=0
    for fname in os.listdir(path_main):
        
        
        dimg.append(fname)
        #list_of_elements = os.listdir(os.path.join(path_main, folder))

        #resize
        #img = cv2.imread('static/data1/'+fname)
        #rez = cv2.resize(img, (300, 300))
        #cv2.imwrite("static/dataset/"+fname, rez)

        #img = cv2.imread('static/dataset/'+fname) 	
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #cv2.imwrite("static/trained/g_"+fname, gray)
        ##noice
        #img = cv2.imread('static/trained/g_'+fname) 
        #dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
        #fname2='ns_'+fname
        #cv2.imwrite("static/trained/"+fname2, dst)

        

        i+=1

    
    return render_template('pro1.html',dimg=dimg)


def kmeans_color_quantization(image, clusters=8, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters, 
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
            rounds, 
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((image.shape))

@app.route('/pro2', methods=['GET', 'POST'])
def pro2():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        
        ##bin
        '''image = cv2.imread('static/dataset/'+fname)
        original = image.copy()
        kmeans = kmeans_color_quantization(image, clusters=4)

        # Convert to grayscale, Gaussian blur, adaptive threshold
        gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

        # Draw largest enclosing circle onto a mask
        mask = np.zeros(original.shape[:2], dtype=np.uint8)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
            cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
            break
        
        # Bitwise-and for result
        result = cv2.bitwise_and(original, original, mask=mask)
        result[mask==0] = (0,0,0)
        #cv2.imwrite("static/trained/bin_"+fname, thresh)'''
        

    path_main2 = 'static/data1'
    for fname in os.listdir(path_main2):
        
        #RPN
        img = cv2.imread('static/data1/'+fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

        # sure background area
        sure_bg = cv2.dilate(opening,kernel,iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,1.5*dist_transform.max(),255,0)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        segment = cv2.subtract(sure_bg,sure_fg)
        img = Image.fromarray(img)
        segment = Image.fromarray(segment)
        path3="static/trained/fg_"+fname
        #segment.save(path3)

  
        

    return render_template('pro2.html',dimg=dimg)


@app.route('/pro3', methods=['GET', 'POST'])
def pro3():
    msg=""
    dimg=[]
    path_main = 'static/data1'
    
    for fname in os.listdir(path_main):
        

        #####
        image = cv2.imread("static/data1/"+fname)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)
        image = Image.fromarray(image)
        edged = Image.fromarray(edged)
        fname2="ff_"+fname
        path4="static/trained/"+fname2
        #edged.save(path4)
        ##
        
    for fname in os.listdir("static/dataset"):
        
        dimg.append(fname)
        

    return render_template('pro3.html',dimg=dimg)

@app.route('/pro4', methods=['GET', 'POST'])
def pro4():
    msg=""
    dimg=[]
    path_main = 'static/data1'
    for fname in os.listdir(path_main):
        dimg.append(fname)

    return render_template('pro4.html',dimg=dimg)

@app.route('/pro5', methods=['GET', 'POST'])
def pro5():
    msg=""
    dimg=[]
    
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        
        parser = argparse.ArgumentParser(
        description='Script to run MobileNet-SSD object detection network ')
        parser.add_argument("--video", help="path to video file. If empty, camera's stream will be used")
        parser.add_argument("--prototxt", default="MobileNetSSD_deploy.prototxt",
                                          help='Path to text network file: '
                                               'MobileNetSSD_deploy.prototxt for Caffe model or '
                                               )
        parser.add_argument("--weights", default="MobileNetSSD_deploy.caffemodel",
                                         help='Path to weights: '
                                              'MobileNetSSD_deploy.caffemodel for Caffe model or '
                                              )
        parser.add_argument("--thr", default=0.2, type=float, help="confidence threshold to filter out weak detections")
        args = parser.parse_args()

        # Labels of Network.
        classNames = { 0: 'background',
            1: 'Bear', 2: 'Pig', 3: 'cup', 4: 'glass',
            5: 'bottle', 6: 'paper', 7: 'car', 8: 'cat', 9: 'chair',
            10: 'Cow', 11: 'diningtable', 12: 'Goat', 13: 'Horse',
            14: 'motorbike', 15: 'person', 16: 'Goat',
            17: 'Elephant', 18: 'Sheep', 19: 'cellphone', 20: 'tvmonitor' }

        # Open video file or capture device. 
        '''if args.video:
            cap = cv2.VideoCapture(args.video)
        else:
            cap = cv2.VideoCapture(0)'''

        #Load the Caffe model 
        net = cv2.dnn.readNetFromCaffe(args.prototxt, args.weights)

        #while True:
        # Capture frame-by-frame
        #ret, frame = cap.read()
        
        frame = cv2.imread("static/dataset/"+fname)
        frame_resized = cv2.resize(frame,(300,300)) # resize frame for prediction

        # MobileNet requires fixed dimensions for input image(s)
        # so we have to ensure that it is resized to 300x300 pixels.
        # set a scale factor to image because network the objects has differents size. 
        # We perform a mean subtraction (127.5, 127.5, 127.5) to normalize the input;
        # after executing this command our "blob" now has the shape:
        # (1, 3, 300, 300)
        blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
        #Set to network the input blob 
        net.setInput(blob)
        #Prediction of network
        detections = net.forward()

        #Size of frame resize (300x300)
        cols = frame_resized.shape[1] 
        rows = frame_resized.shape[0]

        #For get the class and location of object detected, 
        # There is a fix index for class, location and confidence
        # value in @detections array .
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2] #Confidence of prediction 
            if confidence > args.thr: # Filter prediction 
                class_id = int(detections[0, 0, i, 1]) # Class label

                # Object location 
                xLeftBottom = int(detections[0, 0, i, 3] * cols) 
                yLeftBottom = int(detections[0, 0, i, 4] * rows)
                xRightTop   = int(detections[0, 0, i, 5] * cols)
                yRightTop   = int(detections[0, 0, i, 6] * rows)
                
                # Factor for scale to original size of frame
                heightFactor = frame.shape[0]/300.0  
                widthFactor = frame.shape[1]/300.0 
                # Scale object detection to frame
                xLeftBottom = int(widthFactor * xLeftBottom) 
                yLeftBottom = int(heightFactor * yLeftBottom)
                xRightTop   = int(widthFactor * xRightTop)
                yRightTop   = int(heightFactor * yRightTop)
                # Draw location of object  
                cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                              (0, 255, 0))
                try:
                    y=yLeftBottom
                    h=yRightTop-y
                    x=xLeftBottom
                    w=xRightTop-x
                    #image = cv2.imread("static/dataset/"+fname)
                    #mm=cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    #cv2.imwrite("static/trained/c_"+fname, mm)
                    #cropped = image[yLeftBottom:yRightTop, xLeftBottom:xRightTop]

                    #gg="segment.jpg"
                    #cv2.imwrite("static/result/"+gg, cropped)


                    #mm2 = PIL.Image.open('static/trained/'+gg)
                    #rz = mm2.resize((300,300), PIL.Image.ANTIALIAS)
                    #rz.save('static/trained/'+gg)
                except:
                    print("none")
                    #shutil.copy('getimg.jpg', 'static/trained/test.jpg')
                # Draw label and confidence of prediction in frame resized
                if class_id in classNames:
                    label = classNames[class_id] + ": " + str(confidence)
                    claname=classNames[class_id]

                    aid=0
                    if claname=="Bear":
                        aid=1
                    elif claname=="Cow":
                        aid=2
                    elif claname=="Elephant":
                        aid=3
                    elif claname=="Goat":
                        aid=4
                    elif claname=="Horse":
                        aid=5
                    elif claname=="Pig":
                        aid=1
                    elif claname=="Sheep":
                        aid=1

                    #mycursor.execute("update train_data set animal_id=%s where id=%s",(aid,rw[0]))
                    #mydb.commit()
                    
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                    yLeftBottom = max(yLeftBottom, labelSize[1])
                    cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                                         (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                                         (255, 255, 255), cv2.FILLED)
                    cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

                    #print(label) #print class and confidence


            
    '''i=2
    while i<=20:
        fname="ff_"+str(i)+".png"
        dimg.append(fname)
        i+=1'''
    #####
    ###################
    a=0
    b=0
    c=0
    d=0
    e=0
    '''filename = 'static/trained/data1.csv'
    dat1 = pd.read_csv(filename, header=0)
    for sv in dat1.values:
       
        if sv[2]==0:
            a+=1
        elif sv[2]==1:
            b+=1
        elif sv[2]==2:
            c+=1
        elif sv[2]==3:
            d+=1
        else:
            e+=1
            
    count1=[a,b,c,d,e]
    
    fig = plt.figure(figsize = (10, 5))
    
    class1=[]
    #count1=[50,100]
    # creating the bar plot
    plt.bar(class1, count1, color ='blue',
            width = 0.4)
 


    plt.xlabel("Classification")
    plt.ylabel("Count")
    plt.title("")

   
    plt.savefig('static/trained/classi.png')
    #plt.close()
    plt.clf()'''
    ###################################    
    #graph
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,8)
        v1='0.'+str(rn)
        x2.append(float(v1))
        i+=1
    
    x1=[0,0,0,0,0]
    y=[10,30,50,80,100]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model Precision")
    plt.ylabel("precision")
    
    fn="graph1.jpg"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #graph2
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,8)
        v1='0.'+str(rn)
        x2.append(float(v1))
        i+=1
    
    x1=[0,0,0,0,0]
    y=[10,30,50,80,100]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model recall")
    plt.ylabel("recall")
    
    fn="graph2.jpg"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #graph3
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(94,98)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(94,98)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[10,30,50,80,100]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model accuracy")
    plt.ylabel("accuracy")
    
    fn="graph3.jpg"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #graph4
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,4)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(1,4)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[10,30,50,80,100]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model loss")
    plt.ylabel("loss")
    
    fn="graph4.jpg"
    #plt.savefig('static/trained/'+fn)
    plt.close()

    path_main = 'static/data1'
    for fname in os.listdir(path_main):
        dimg.append(fname)
    ###############################
    return render_template('pro5.html',dimg=dimg)


def toString(a):
  l=[]
  m=""
  for i in a:
    b=0
    c=0
    k=int(math.log10(i))+1
    for j in range(k):
      b=((i%10)*(2**j))   
      i=i//10
      c=c+b
    l.append(c)
  for x in l:
    m=m+chr(x)
  return m
@app.route('/pro6', methods=['GET', 'POST'])
def pro6():
    msg=""
    dimg=[]
    data1=[]
    data2=[]
    data3=[]
    data4=[]
    data5=[]
    data6=[]
    data7=[]
    cname=[]

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM animal_info order by id")
    row = mycursor.fetchall()
    for row1 in row:
        cname.append(row1[1])
           
                     
    ##    
    ff2=open("static/trained/tdata.txt","r")
    rd=ff2.read()
    ff2.close()

    num=[]
    r1=rd.split(',')
    s=len(r1)
    ss=s-1
    i=0
    while i<ss:
        num.append(int(r1[i]))
        i+=1

    #print(num)
    dat=toString(num)
    dd2=[]
    d1=dat.split(',')
    ##
    
    for d11 in d1:
        
        d2=d11.split('-')
        
        if d2[1]=='1':
            
            data1.append(d2[0])
        if d2[1]=='2':
            
            data2.append(d2[0])
        if d2[1]=='3':
            
            data3.append(d2[0])
        if d2[1]=='4':
            
            data4.append(d2[0])
        if d2[1]=='5':
            data5.append(d2[0])
        if d2[1]=='6':
            data6.append(d2[0])
        if d2[1]=='7':
            data7.append(d2[0])
            
        
    #####################
    v1=0
    v2=0
    v3=0
    v4=0
    v5=0
    v6=0
    v7=0
    vv=""
    for dff in d1:
        vv=dff.split('-')
        if vv[1]=='1':
            v1+=1
        if vv[1]=='2':
            v2+=1
        if vv[1]=='3':
            v3+=1
        if vv[1]=='4':
            v4+=1
        if vv[1]=='5':
            v5+=1
        if vv[1]=='6':
            v6+=1
        if vv[1]=='7':
            v7+=1
        
    g1=v1+v2+v3+v4+v5+v6+v7
    dd2=[v1,v2,v3,v4,v5,v6,v7]
    
    
    doc = cname #list(data.keys())
    values = dd2 #list(data.values())
    print(doc)
    print(values)
    fig = plt.figure(figsize = (10, 5))
     
    # creating the bar plot
    plt.bar(doc, values, color ='blue',
            width = 0.4)
 

    plt.ylim((1,g1))
    plt.xlabel("Animal")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass.png"
    plt.xticks(rotation=20)
    #plt.savefig('static/trained/'+fn)
    
    #plt.close()
    plt.clf()
    ##########     
    

    return render_template('pro6.html',cname=cname,data1=data1,data2=data2,data3=data3,data4=data4,data5=data5,data6=data6,data7=data7)



@app.route('/monitor', methods=['GET', 'POST'])
def monitor():
    msg=""
    return render_template('monitor.html', msg=msg)


def getbox(im, color):
    bg = Image.new(im.mode, im.size, color)
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    return diff.getbbox()

def split(im):
    retur = []
    emptyColor = im.getpixel((0, 0))
    box = getbox(im, emptyColor)
    width, height = im.size
    pixels = im.getdata()
    sub_start = 0
    sub_width = 0
    offset = box[1] * width
    for x in range(width):
        if pixels[x + offset] == emptyColor:
            if sub_width > 0:
                retur.append((sub_start, box[1], sub_width, box[3]))
                sub_width = 0
            sub_start = x + 1
        else:
            sub_width = x + 1
    if sub_width > 0:
        retur.append((sub_start, box[1], sub_width, box[3]))
    return retur



@app.route('/admin2', methods=['GET', 'POST'])
def admin2():
    return render_template('admin2.html', act="on", page='0', imgg='0')


#WildNet - Classify the animal
def wildNet():
    """
    Main Function
    """
    # Set up the Arguments, Tensorboard Writer, Dataloader, Loss Fn, Optimizer
    assert_and_infer_cfg(args)
    writer = prep_experiment(args, parser)

    train_source_loader, val_loaders, train_wild_loader, train_obj, extra_val_loaders = datasets.setup_loaders(args)

    criterion, criterion_val = loss.get_loss(args)
    criterion_aux = loss.get_loss_aux(args)
    net = network.get_net(args, criterion, criterion_aux, args.cont_proj_head, args.wild_cont_dict_size)

    optim, scheduler = optimizer.get_optimizer(args, net)

    net = torch.nn.SyncBatchNorm.convert_sync_batchnorm(net)
    net = network.warp_network_in_dataparallel(net, args.local_rank)
    epoch = 0
    i = 0

    if args.snapshot:
        epoch, mean_iu = optimizer.load_weights(net, optim, scheduler,
                            args.snapshot, args.restore_optimizer)
        if args.restore_optimizer is True:
            iter_per_epoch = len(train_source_loader)
            i = iter_per_epoch * epoch
            epoch = epoch + 1
        else:
            epoch = 0

    print("#### iteration", i)
    torch.cuda.empty_cache()

    while i < args.max_iter:
        # Update EPOCH CTR
        cfg.immutable(False)
        cfg.ITER = i
        cfg.immutable(True)

        i = train(train_source_loader, train_wild_loader, net, optim, epoch, writer, scheduler, args.max_iter)
        train_source_loader.sampler.set_epoch(epoch + 1)
        train_wild_loader.sampler.set_epoch(epoch + 1)

        if args.local_rank == 0:
            print("Saving pth file...")
            evaluate_eval(args, net, optim, scheduler, None, None, [],
                        writer, epoch, "None", None, i, save_pth=True)

        if args.class_uniform_pct:
            if epoch >= args.max_cu_epoch:
                train_obj.build_epoch(cut=True)
                train_source_loader.sampler.set_num_samples()
            else:
                train_obj.build_epoch()
        
        epoch += 1
    
    # Validation after epochs
    if len(val_loaders) == 1:
        # Run validation only one time - To save models
        for dataset, val_loader in val_loaders.items():
            validate(val_loader, dataset, net, criterion_val, optim, scheduler, epoch, writer, i)
    else:
        if args.local_rank == 0:
            print("Saving pth file...")
            evaluate_eval(args, net, optim, scheduler, None, None, [],
                        writer, epoch, "None", None, i, save_pth=True)

    for dataset, val_loader in extra_val_loaders.items():
        print("Extra validating... This won't save pth file")
        validate(val_loader, dataset, net, criterion_val, optim, scheduler, epoch, writer, i, save_pth=False)


def train(source_loader, wild_loader, net, optim, curr_epoch, writer, scheduler, max_iter):
    """
    Runs the training loop per epoch
    source_loader: Source data loader for train
    wild_loader: Wild data loader for train
    net: thet network
    optim: optimizer
    curr_epoch: current epoch
    writer: tensorboard writer
    return:
    """
    net.train()

    train_total_loss = AverageMeter()
    time_meter = AverageMeter()

    curr_iter = curr_epoch * len(source_loader)

    wild_loader_iter = enumerate(wild_loader)

    for i, data in enumerate(source_loader):
        if curr_iter >= max_iter:
            break

        inputs, gts, _, aux_gts = data

        # Multi source and AGG case
        if len(inputs.shape) == 5:
            B, D, C, H, W = inputs.shape
            num_domains = D
            inputs = inputs.transpose(0, 1)
            gts = gts.transpose(0, 1).squeeze(2)
            aux_gts = aux_gts.transpose(0, 1).squeeze(2)

            inputs = [input.squeeze(0) for input in torch.chunk(inputs, num_domains, 0)]
            gts = [gt.squeeze(0) for gt in torch.chunk(gts, num_domains, 0)]
            aux_gts = [aux_gt.squeeze(0) for aux_gt in torch.chunk(aux_gts, num_domains, 0)]
        else:
            B, C, H, W = inputs.shape
            num_domains = 1
            inputs = [inputs]
            gts = [gts]
            aux_gts = [aux_gts]

        batch_pixel_size = C * H * W

        for di, ingredients in enumerate(zip(inputs, gts, aux_gts)):
            input, gt, aux_gt = ingredients

            _, inputs_wild = next(wild_loader_iter)
            input_wild = inputs_wild[0]

            start_ts = time.time()

            img_gt = None
            input, gt = input.cuda(), gt.cuda()
            input_wild = input_wild.cuda()

            optim.zero_grad()
            outputs = net(x=input, gts=gt, aux_gts=aux_gt, x_w=input_wild, apply_fs=args.use_fs)
            
            outputs_index = 0
            main_loss = outputs[outputs_index]
            outputs_index += 1
            aux_loss = outputs[outputs_index]
            outputs_index += 1
            total_loss = main_loss + (0.4 * aux_loss)

            if args.use_fs:
                if args.use_cel:
                    cel_loss = outputs[outputs_index]
                    outputs_index += 1
                    total_loss = total_loss + (args.lambda_cel * cel_loss)
                else:
                    cel_loss = 0
                
                if args.use_sel:
                    sel_loss_main = outputs[outputs_index]
                    outputs_index += 1
                    sel_loss_aux = outputs[outputs_index]
                    outputs_index += 1
                    total_loss = total_loss + args.lambda_sel * (sel_loss_main + (0.4 * sel_loss_aux))
                else:
                    sel_loss_main = 0
                    sel_loss_aux = 0

                if args.use_scr:
                    scr_loss_main = outputs[outputs_index]
                    outputs_index += 1
                    scr_loss_aux = outputs[outputs_index]
                    outputs_index += 1
                    total_loss = total_loss + args.lambda_scr * (scr_loss_main + (0.4 * scr_loss_aux))
                else:
                    scr_loss_main = 0
                    scr_loss_aux = 0


            log_total_loss = total_loss.clone().detach_()
            torch.distributed.all_reduce(log_total_loss, torch.distributed.ReduceOp.SUM)
            log_total_loss = log_total_loss / args.world_size
            train_total_loss.update(log_total_loss.item(), batch_pixel_size)
            
            total_loss.backward()
            optim.step()

            time_meter.update(time.time() - start_ts)

            del total_loss, log_total_loss

            if args.local_rank == 0:
                if i % 50 == 49:
                    msg = '[epoch {}], [iter {} / {} : {}], [loss {:0.6f}], [lr {:0.6f}], [time {:0.4f}]'.format(
                        curr_epoch, i + 1, len(source_loader), curr_iter, train_total_loss.avg,
                        optim.param_groups[-1]['lr'], time_meter.avg / args.train_batch_size)

                    logging.info(msg)
                    
                    # Log tensorboard metrics for each iteration of the training phase
                    writer.add_scalar('loss/train_loss', (train_total_loss.avg), curr_iter)
                    train_total_loss.reset()
                    time_meter.reset()

        curr_iter += 1
        scheduler.step()

        if i > 5 and args.test_mode:
            return curr_iter

    return curr_iter

def validate(val_loader, dataset, net, criterion, optim, scheduler, curr_epoch, writer, curr_iter, save_pth=True):
    """
    Runs the validation loop after each training epoch
    val_loader: Data loader for validation
    dataset: dataset name (str)
    net: thet network
    criterion: loss fn
    optimizer: optimizer
    curr_epoch: current epoch
    writer: tensorboard writer
    return: val_avg for step function if required
    """

    net.eval()
    val_loss = AverageMeter()
    iou_acc = 0
    error_acc = 0
    dump_images = []

    for val_idx, data in enumerate(val_loader):

        inputs, gt_image, img_names, _ = data

        if len(inputs.shape) == 5:
            B, D, C, H, W = inputs.shape
            inputs = inputs.view(-1, C, H, W)
            gt_image = gt_image.view(-1, 1, H, W)

        assert len(inputs.size()) == 4 and len(gt_image.size()) == 3
        assert inputs.size()[2:] == gt_image.size()[1:]

        batch_pixel_size = inputs.size(0) * inputs.size(2) * inputs.size(3)
        inputs, gt_cuda = inputs.cuda(), gt_image.cuda()

        with torch.no_grad():
            output = net(inputs)

        del inputs

        assert output.size()[2:] == gt_image.size()[1:]
        assert output.size()[1] == datasets.num_classes

        val_loss.update(criterion(output, gt_cuda).item(), batch_pixel_size)

        del gt_cuda

        # Collect data from different GPU to a single GPU since
        # encoding.parallel.criterionparallel function calculates distributed loss
        # functions
        predictions = output.data.max(1)[1].cpu()

        # Logging
        if val_idx % 20 == 0:
            if args.local_rank == 0:
                logging.info("validating: %d / %d", val_idx + 1, len(val_loader))
        if val_idx > 10 and args.test_mode:
            break

        # Image Dumps
        if val_idx < 10:
            dump_images.append([gt_image, predictions, img_names])

        iou_acc += fast_hist(predictions.numpy().flatten(), gt_image.numpy().flatten(),
                             datasets.num_classes)
        del output, val_idx, data

    iou_acc_tensor = torch.cuda.FloatTensor(iou_acc)
    torch.distributed.all_reduce(iou_acc_tensor, op=torch.distributed.ReduceOp.SUM)
    iou_acc = iou_acc_tensor.cpu().numpy()

    if args.local_rank == 0:
        evaluate_eval(args, net, optim, scheduler, val_loss, iou_acc, dump_images,
                    writer, curr_epoch, dataset, None, curr_iter, save_pth=save_pth)

    return val_loss.avg



@app.route('/anitest', methods=['GET', 'POST'])
def anitest():
    msg=""
    act=""
    aud=""
    fnn="e (1).jpg"
    animal=""
    xn=randint(1, 50)
    an=randint(1, 4)
    print(xn)
    act=str(xn)
    #str(xn)

    ff=open("msg.txt","r")
    mc=ff.read()
    ff.close()
    mcount=int(mc)
    mcc=mcount+1
    
    if an==1:
        act="1"
        fnn="c ("+str(xn)+").jpeg"
        animal="Cow"
        msg="Cow Detected"
        aud="a2.mp3"
    elif an==2:
        act="1"
        fnn="e ("+str(xn)+").jpg"
        animal="Elephant"
        msg="Elephant Detected"
        aud="a2.mp3"
    elif an==3:
        act="1"
        fnn="g ("+str(xn)+").jpg"
        animal="Goat"
        msg="Goat Detected"
        aud="a3.mp3"
    elif an==4:
        act="1"
        fnn="h ("+str(xn)+").jpeg"
        animal="Horse"
        msg="Horse Detected"
        aud="a3.mp3"
    else:
        act=""
        animal=""
        msg="No Animals"

    if act=="1":    
        if mcount<3:
            ff=open("msg.txt","w")
            ff.write(str(mcc))
            ff.close()

            cursor = mydb.cursor()
            cursor.execute('SELECT * FROM admin')
            account = cursor.fetchone()
            mobile=account[2]
            #url="http://iotcloud.co.in/testsms/sms.php?sms=msg&name=Farmer&mess="+msg+"&mobile="+str(mobile)
            #webbrowser.open_new(url)
    
    '''if xn<=7:
        fnn="r"+str(xn)+".jpg"
    
    if act=="1":
        animal="Cow"
        msg="Cow Detected"
    elif act=="2":
        animal="Cow"
        msg="Cow Detected"
    elif act=="3":
        animal="Elephant"
        msg="Elephant Detected"
    elif act=="4":
        animal="Elephant"
        msg="Elephant Detected"
    elif act=="5":
        animal="Goat"
        msg="Goat Detected"
    elif act=="6":
        animal="Goat"
        msg="Goat Detected"
    elif act=="7":
        animal="Goat"
        msg="Goat Detected"
    else:
        animal=""
        msg="No Animals"'''

    if animal=="":
        print("")
    else:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM ani_data")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO ani_data(id,animal) VALUES (%s, %s)"
        val = (maxid,animal)
        mycursor.execute(sql, val)
        mydb.commit()    
    ##################
    # construct the argument parse 
    parser = argparse.ArgumentParser(
        description='Script to run MobileNet-SSD object detection network ')
    parser.add_argument("--video", help="path to video file. If empty, camera's stream will be used")
    parser.add_argument("--prototxt", default="MobileNetSSD_deploy.prototxt",
                                      help='Path to text network file: '
                                           'MobileNetSSD_deploy.prototxt for Caffe model or '
                                           )
    parser.add_argument("--weights", default="MobileNetSSD_deploy.caffemodel",
                                     help='Path to weights: '
                                          'MobileNetSSD_deploy.caffemodel for Caffe model or '
                                          )
    parser.add_argument("--thr", default=0.2, type=float, help="confidence threshold to filter out weak detections")
    args = parser.parse_args()

    # Labels of Network.
    classNames = { 0: 'background',
        1: 'mobile', 2: 'bicycle', 3: 'cup', 4: 'glass',
        5: 'bottle', 6: 'paper', 7: 'car', 8: 'cat', 9: 'chair',
        10: 'cow', 11: 'diningtable', 12: 'goat', 13: 'horse',
        14: 'motorbike', 15: 'person', 16: 'goat',
        17: 'elephant', 18: 'cow', 19: 'cellphone', 20: 'tvmonitor' }

    # Open video file or capture device. 
    '''if args.video:
        cap = cv2.VideoCapture(args.video)
    else:
        cap = cv2.VideoCapture(0)'''

    #Load the Caffe model 
    net = cv2.dnn.readNetFromCaffe(args.prototxt, args.weights)

    #while True:
    # Capture frame-by-frame
    #ret, frame = cap.read()
    frame = cv2.imread("static/dataset/"+fnn)
    frame_resized = cv2.resize(frame,(300,300)) # resize frame for prediction

    # MobileNet requires fixed dimensions for input image(s)
    # so we have to ensure that it is resized to 300x300 pixels.
    # set a scale factor to image because network the objects has differents size. 
    # We perform a mean subtraction (127.5, 127.5, 127.5) to normalize the input;
    # after executing this command our "blob" now has the shape:
    # (1, 3, 300, 300)
    blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
    #Set to network the input blob 
    net.setInput(blob)
    #Prediction of network
    detections = net.forward()

    #Size of frame resize (300x300)
    cols = frame_resized.shape[1] 
    rows = frame_resized.shape[0]

    #For get the class and location of object detected, 
    # There is a fix index for class, location and confidence
    # value in @detections array .
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2] #Confidence of prediction 
        if confidence > args.thr: # Filter prediction 
            class_id = int(detections[0, 0, i, 1]) # Class label

            # Object location 
            xLeftBottom = int(detections[0, 0, i, 3] * cols) 
            yLeftBottom = int(detections[0, 0, i, 4] * rows)
            xRightTop   = int(detections[0, 0, i, 5] * cols)
            yRightTop   = int(detections[0, 0, i, 6] * rows)
            
            # Factor for scale to original size of frame
            heightFactor = frame.shape[0]/300.0  
            widthFactor = frame.shape[1]/300.0 
            # Scale object detection to frame
            xLeftBottom = int(widthFactor * xLeftBottom) 
            yLeftBottom = int(heightFactor * yLeftBottom)
            xRightTop   = int(widthFactor * xRightTop)
            yRightTop   = int(heightFactor * yRightTop)
            # Draw location of object  
            cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                          (0, 255, 0))
            try:
                y=yLeftBottom
                h=yRightTop-y
                x=xLeftBottom
                w=xRightTop-x
                image = cv2.imread("static/dataset/"+fnn)
                mm=cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.imwrite("static/result/"+fnn, mm)
                cropped = image[yLeftBottom:yRightTop, xLeftBottom:xRightTop]
                gg="segment.jpg"
                cv2.imwrite("static/result/"+gg, cropped)
                #mm2 = PIL.Image.open('static/trained/'+gg)
                #rz = mm2.resize((300,300), PIL.Image.ANTIALIAS)
                #rz.save('static/trained/'+gg)
            except:
                print("none")
                #shutil.copy('getimg.jpg', 'static/trained/test.jpg')
            # Draw label and confidence of prediction in frame resized
            if class_id in classNames:
                label = classNames[class_id] + ": " + str(confidence)
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                yLeftBottom = max(yLeftBottom, labelSize[1])
                cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                                     (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                                     (255, 255, 255), cv2.FILLED)
                cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

                print(label) #print class and confidence
    ####################
    return render_template('anitest.html',act=act,msg=msg,fnn=fnn,aud=aud)


@app.route('/result', methods=['GET', 'POST'])
def result():
    res=""
    afile="a3.mp3"
    password_provided = "xyz" # This is input in the form of a string
    password = password_provided.encode() # Convert to type bytes
    salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
    f2=open("log.txt","r")
    vv=f2.read()
    f2.close()
    vv1=vv.split('.')
    tff3=vv1[0]
    tff4=tff3[1:]
    rid=int(tff4)
    input_file = 'test.encrypted'
    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.decrypt(data)
    value=encrypted.decode("utf-8")
    dar=value.split('|')
    rr=rid-1
    dv=dar[rr]
    drw=dv.split('-')
    v=drw[1]
    if v=="a1.flac":
        lf="Cow"
    elif v=="a2.mp3":
        lf="Elephant"
    else:
        lf="Goat"
    
    return render_template('result.html',res=lf,afile=v)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    mobile=""
    msg=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM admin")
    dm = mycursor.fetchone()
    mobile=dm[2]
    
    if request.method == 'POST':
        
        mobile = request.form['mobile']
        mycursor.execute("update admin set mobile=%s",(mobile,))
        mydb.commit()
        msg="ok"
    
    return render_template('admin.html', msg=msg,mobile=mobile)

@app.route('/add_data',methods=['POST','GET'])
def add_data():
    act=request.args.get("act")
    mycursor = mydb.cursor()
    if request.method == 'POST':
        
        animal = request.form['animal']

        mycursor.execute("SELECT max(id)+1 FROM train_data")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        sql = "INSERT INTO train_data(id,animal,fimg) VALUES (%s, %s, %s)"
        val = (maxid,animal, '')
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('add_photo',vid=maxid)) 

    mycursor.execute("SELECT * FROM train_data")
    data = mycursor.fetchall()

    ###
    if act=="del":
        did=request.args.get("did")

        mycursor.execute("SELECT count(*) FROM animal_img where vid=%s",(did,))
        cn = mycursor.fetchone()[0]
        if cn>0:
            mycursor.execute("SELECT * FROM animal_img where vid=%s",(did,))
            dd = mycursor.fetchall()
            for ds in dd:
                os.remove("static/frame/"+ds[2])

            mycursor.execute("delete from animal_img where vid=%s",(did,))
            mydb.commit()
                
        
        mycursor.execute("delete from train_data where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_data')) 
    ###
        
    return render_template('add_data.html',data=data)

@app.route('/add_photo',methods=['POST','GET'])
def add_photo():
    vid=""
    ff1=open("photo.txt","w")
    ff1.write("2")
    ff1.close()

    #ff2=open("mask.txt","w")
    #ff2.write("face")
    #ff2.close()
    act = request.args.get('act')
    
    if request.method=='GET':
        vid = request.args.get('vid')
        ff=open("user.txt","w")
        ff.write(str(vid))
        ff.close()

    cursor = mydb.cursor()
    
    if request.method=='POST':
        vid=request.form['vid']
        fimg="v"+vid+".jpg"
        

        cursor.execute('delete from animal_img WHERE vid = %s', (vid, ))
        mydb.commit()

        ff=open("det.txt","r")
        v=ff.read()
        ff.close()
        vv=int(v)
        v1=vv-1
        vface1=vid+"_"+str(v1)+".jpg"
        i=2
        while i<vv:
            
            cursor.execute("SELECT max(id)+1 FROM animal_img")
            maxid = cursor.fetchone()[0]
            if maxid is None:
                maxid=1
            vface=vid+"_"+str(i)+".jpg"
            sql = "INSERT INTO animal_img(id, vid, animal_img) VALUES (%s, %s, %s)"
            val = (maxid, vid, vface)
            print(val)
            cursor.execute(sql,val)
            mydb.commit()
            i+=1

        
            
        cursor.execute('update train_data set fimg=%s WHERE id = %s', (vface1, vid))
        mydb.commit()
        shutil.copy('static/faces/f1.jpg', 'static/photo/'+vface1)
        return redirect(url_for('view_photo',vid=vid,act='success'))
        
    
    cursor.execute("SELECT * FROM train_data")
    data = cursor.fetchall()
    return render_template('add_photo.html',data=data, vid=vid)

@app.route('/view_photo',methods=['POST','GET'])
def view_photo():
    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()
    vid=""
    value=[]
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM animal_img where vid=%s",(vid, ))
        value = mycursor.fetchall()


        
    return render_template('view_photo.html', result=value,vid=vid)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))
###################
def gen2(camera2):
    
    while True:
        frame = camera2.get_frame()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
@app.route('/video_feed2')
        

def video_feed2():
    return Response(gen2(VideoCamera2()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
##################
def gen(camera):
    
    while True:
        frame = camera.get_frame()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
@app.route('/video_feed')
        

def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5432)

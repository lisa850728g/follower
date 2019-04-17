#!/usr/bin/python
#coding:utf8

from flask import Flask, render_template, url_for, request,redirect,make_response,session
import pymongo
from pymongo import MongoClient, InsertOne

app = Flask(__name__)
user_list = [u'jim',u'max',u'py']

@app.route('/')
def index():
    username = request.cookies.get('username')
    if not username:
        username = u'請先登入'
    islogin = session.get('islogin')
    nav_list = [u'首頁',u'個人資料',u'粉絲',u'追蹤中']
    blog = {'title':'welcome to my page','content':'hello, welcome!'}
    return render_template('index.html', nav_list=nav_list, username=username, blog = blog, islogin=islogin)

@app.route('/reg', methods=['GET','POST'])
def regist():
    if request.method == 'POST':
        username = request.form['username']
        userpwd = request.form['userpwd']
        client = MongoClient('localhost', 27017)
        db = client['information']
        table_usr = db.user
        table_usr.insert_one({'account': username, 'password': userpwd})
        client.close()
        return "user '%s' regist ok!" % request.form['username']
    else:
        #request.args[‘username’]
        return render_template('regis.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)

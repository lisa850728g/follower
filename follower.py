#!/usr/bin/python
#coding:utf8

from flask import Flask, render_template, url_for, request,redirect,make_response,session
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "dk54pgk42u/4nau4ul4g"

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
        usersex = request.form['usersex']
        client = MongoClient('localhost', 27017)
        tableUsr = client['information'].user
        tableUsr.insert_one({'account': username, 'password': userpwd, 'sex': usersex})
        client.close()
        return "註冊成功"
    else:
        return render_template('regis.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        userpwd = request.form.get('userpwd')
        client = MongoClient('localhost', 27017)
        tableUsr = client['information'].user
        userlist = tableUsr.distinct('account')
        if username in userlist :
            if userpwd == tableUsr.find_one({'account': username})['password'] :
                response = make_response(redirect('/'))
                response.set_cookie('username', value=username, max_age=300)
                session['islogin'] = '1'
                return response
            else:
                session['islogin'] = '0'
                return render_template('login.html', message="密碼輸入錯誤")
        else:
            session['islogin'] = '0'
            return render_template('login.html', message="無此使用者")
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)

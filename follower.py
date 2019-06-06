#!/usr/bin/python
#coding:utf8

from flask import Flask, render_template, url_for, request,redirect,make_response,session
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "dk54pgk42u/4nau4ul4g"

@app.route('/home')
def index():
    username = request.cookies.get('username')
    client = MongoClient('localhost', 27017)
    collectUsr = client['information'].user

    if not username:
        session['islogin'] = '0'
        username = u'登入'

    usrInfo = collectUsr.find_one({"account":username})
    usrList = collectUsr.find({"account": {"$ne":username} })

    islogin = session.get('islogin')
    nav_list = [u'首頁',u'個人資料',u'粉絲',u'追蹤中']
    blog = {'title':'welcome to my page','users':usrList, 'userInfo':usrInfo}
    client.close()
    return render_template('index.html', nav_list=nav_list, username=username, blog = blog, islogin=islogin)

# def follow(follower,fan):
#     client = MongoClient('localhost', 27017)
#     collectUsr = client['information'].user
#     sql = {'account':follower}
#     for addFan in collectUsr.find(sql):
#         old_amt_fan = addFan['amt_fan']
#         old_fan = addFan['fan']
#     newvalues = {'$set': {'amt_fan':old_amt_fan+1, 'fan':old_fan.append(fan)}
#     collectUsr.update(sql,newvalues)
#     return render_template('index.html', nav_list=nav_list, username=username, blog = blog, islogin=islogin)

@app.route('/reg', methods=['GET','POST'])
def regist():
    if request.method == 'POST':
        username = request.form['username']
        userpwd = request.form['userpwd']
        usersex = request.form['usersex']
        client = MongoClient('localhost', 27017)
        collectUsr = client['information'].user
        collectUsr.insert_one({'account':username, 'password':userpwd, 'sex':usersex, 'amt_follower':0,'follower':[],'amt_fan':0,'fan':[]})
        client.close()
        return redirect('/login/')
    else:
        return render_template('regis.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        userpwd = request.form.get('userpwd')
        client = MongoClient('localhost', 27017)
        collectUsr = client['information'].user
        userlist = collectUsr.distinct('account')
        if username in userlist :
            if userpwd == collectUsr.find_one({'account': username})['password'] :
                response = make_response(redirect('/home'))
                response.set_cookie('username', value=username, max_age=300)
                session['islogin'] = '1'
                return response
            else:
                session['islogin'] = '0'
                return render_template('login.html', message="密碼輸入錯誤")
        else:
            session['islogin'] = '0'
            return render_template('login.html', message="無此使用者")
        client.close()
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)

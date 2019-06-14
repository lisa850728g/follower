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
    client = MongoClient('localhost', 27017)
    collectUsr = client['information'].user

    if not username:
        session['islogin'] = '0'
        username = u'登入'
        usrList = collectUsr.find()
        blog = {'title':'welcome','users':usrList}

    else:
        usrInfo = collectUsr.find_one({"account":username})

        def sortBySex(usrSex):
            num = {
                "girl" : -1,
                "boy" : 1
            }
            return num.get(usrSex, 1)

        usrList = collectUsr.find({"account": {"$ne":username} }).sort([("sex",sortBySex(usrInfo['sex']))])
        blog = {'title':'welcome to my page','users':usrList, 'userInfo':usrInfo}

    nav_list = [u'首頁',u'個人資料',u'粉絲',u'追蹤中']
    client.close()
    islogin = session.get('islogin')
    return render_template('index.html', nav_list=nav_list, username=username,blog = blog, islogin=islogin)

# @app.route('/follow=<string:toFollow>',methods=['POST'])
# def follow(toFollow):
#     client = MongoClient('localhost', 27017)
#     collectUsr = client['information'].user
#     username = request.cookies.get('username')
#
#     if not username:
#         session['islogin'] = '0'
#         username = u'登入'
#
#     sql = {'account':toFollow}
#     old_amt_fan = collectUsr.find_one(sql)['amt_fan']
#     newFanNum = {'$set': {'amt_fan':old_amt_fan+1}}
#     collectUsr.update(sql,newFanNum)
#     newFanName = {'$addToSet': {'fan':username}}
#     collectUsr.update(sql,newFanName)
#
#     sql2 = {'account':username}
#     old_amt_follower2 = collectUsr.find_one(sql2)['amt_follower']
#     newFollowerNum = {'$set': {'amt_follower':old_amt_follower2+1}}
#     collectUsr.update(sql2,newFollowerNum)
#     newFollowerName = {'$addToSet': {'follow':toFollow}}
#     collectUsr.update(sql,newFollowerName)
#
#     usrInfo = collectUsr.find_one({"account":username})
#     usrList = collectUsr.find({"account": {"$ne":username} })
#     blog = {'title':'welcome to my page','users':usrList, 'userInfo':usrInfo}
#     client.close()
#     return render_template('index.html', blog = blog)

@app.route('/reg', methods=['GET','POST'])
def regist():
    if request.method == 'POST':
        username = request.form['username']
        userpwd = request.form['userpwd']
        usersex = request.form['usersex']
        client = MongoClient('localhost', 27017)
        collectUsr = client['information'].user
        checkAccount = collectUsr.count({'account':username})
        if checkAccount != 0:
            return render_template('regis.html', message="此帳號已有人使用")
        else:
            collectUsr.insert_one({'account':username, 'password':userpwd, 'sex':usersex, 'amt_follower':0,'follower':[],'amt_fan':0,'fan':[]})
        client.close()
        return redirect('/log')
    else:
        return render_template('regis.html')

@app.route('/log', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        userpwd = request.form.get('userpwd')
        client = MongoClient('localhost', 27017)
        collectUsr = client['information'].user
        userlist = collectUsr.distinct('account')
        if username in userlist :
            if userpwd == collectUsr.find_one({'account': username})['password'] :
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
        client.close()
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('islogin',0)
    response = make_response(redirect('/'))
    response.set_cookie('username', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)

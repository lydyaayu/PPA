import os
from os.path import join, dirname
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta
import jwt
import hashlib
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    url_for,
)
from werkzeug.utils import secure_filename

app=Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = './static/profile_pics'

SECRET_KEY = 'SPARTA'
TOKEN_KEY = 'mytoken'

client=MongoClient('mongodb+srv://Aryama:1234@cluster0.9x3eatx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db=client.dbPPA

app = Flask(__name__)

@app.route("/")
def home():
    token_receive = request.cookies.get(TOKEN_KEY)
    if token_receive:
        try:
            payload = jwt.decode(
                token_receive,
                SECRET_KEY,
                algorithms=['HS256']
            )
            user_info = db.normal_users.find_one({'username': payload.get('id')})
            user_info2 = db.expert_users.find_one({'username': payload.get('id')})

            if user_info:

                return render_template('home.html',user_info=user_info)
            elif user_info2:
                return render_template('home2.html',user_info2=user_info2)

                return render_template('home.html', user_info=user_info)  # Mengarahkan ke home.html sebagai dashboard
            elif user_info2:
                return render_template('expert.html', user_info=user_info2)

            else:
                return render_template('login.html')

        except jwt.ExpiredSignatureError:
            msg = 'Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return render_template('login.html')

@app.route("/login")
def login():
    token_receive = request.cookies.get(TOKEN_KEY)
    msg = request.args.get("msg")
    if msg:
        return render_template('login.html',msg=msg)
    else:
        if token_receive:
            try:
                payload = jwt.decode(
                    token_receive,
                    SECRET_KEY,
                    algorithms=['HS256']
                )
                user_info = db.normal_users.find_one({'username':payload.get('id')})
                user_info2 = db.expert_users.find_one({'username':payload.get('id')})
                
                if user_info:
                    return render_template('about.html',user_info=user_info)
                elif user_info2:
                    return render_template('contact.html',user_info2=user_info2)
                else:
                    return render_template('login.html')
                    
            except jwt.ExpiredSignatureError:
                msg='Your token has expired'
                return redirect(url_for('login', msg=msg))
            except jwt.exceptions.DecodeError:
                msg='There was a problem logging you in'
                return redirect(url_for('login', msg=msg))
        else:
            return render_template('login.html',msg=msg)


@app.route("/user/<username>")
def user(username):
    # an endpoint for retrieving a user's profile information
    # and all of their posts
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # if this is my own profile, True
        # if this is somebody else's profile, False
        status = username == payload["id"]

        user_info = db.users.find_one({"username": username}, {"_id": False})
        return render_template("user.html", user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/sign_in", methods=["POST"])
def sign_in():
    # Sign in
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    print(username_receive, pw_hash)
    result = db.normal_users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    result2 = db.expert_users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    if result:
        payload = {
            "id": username_receive,
            # the token will be valid for 24 hours
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    elif result2:
        payload = {
            "id": username_receive,
            # the token will be valid for 24 hours
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "We could not find a user with that id/password combination",
            }
        )


@app.route("/sign_up/save", methods=["POST"])
def sign_up():
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    role_receive = request.form["role_give"]
    password_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    if(role_receive == 'expert'):
        doc = {
            "username": username_receive,                               
            "password": password_hash,                                  
            "profile_name": username_receive,
            "role":role_receive,                                            
            }
        db.expert_users.insert_one(doc)
        return jsonify({'result': 'success'})
    elif(role_receive == 'normal'):
        doc = {
            "username": username_receive,                               
            "password": password_hash,
            "profile_name" : username_receive,     
            "role":role_receive,                                                                        
            }
        db.normal_users.insert_one(doc)
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failed'})


@app.route("/sign_up/check_dup", methods=["POST"])
def check_dup():
    # ID we should check whether or not the id is already taken
    username_receive = request.form["username_give"]
    exists = bool(db.normal_users.find_one({'username':username_receive}))
    exists2 = bool(db.expert_users.find_one({'username':username_receive}))
    return jsonify({"result": "success", "exists": exists+exists2})

# ACT
@app.route("/act", methods=["POST"])
def act_post():
    act_receive = request.form['act_give']

    count = db.act.count_documents({})
    num = count + 1

    doc = {
        'num': num,
        'act': act_receive,
        'done': 0,
    }
    db.act.insert_one(doc)
    return jsonify({'msg': 'Kegiatan Berhasil Ditambah!'})

@app.route("/act/done", methods=["POST"])
def act_done():
    num_receive = request.form['num_give']
    db.act.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update Kegiatan Selesai!'})

@app.route("/delete", methods=["POST"])
def act_bucket():
    num_receive = request.form['num_give']
    db.act.delete_one({'num': int(num_receive)})
    return jsonify({'msg': 'delete success!'})

@app.route("/act", methods=["GET"])
def act_get():
    act_list = list(db.act.find({}, {'_id': False}))
    return jsonify({'acts': act_list})

# ACT_WEEK
@app.route("/act_week", methods=["POST"])
def act_week_post():
    act_week_receive = request.form['act_week_give']

    count = db.act_week.count_documents({})
    num = count + 1

    doc = {
        'num': num,
        'act_week': act_week_receive,
        'done': 0,
    }
    db.act_week.insert_one(doc)
    return jsonify({'msg': 'Rencana Minggu Ini Berhasil Ditambah!'})

@app.route("/act_week/done", methods=["POST"])
def act_week_done():
    num_receive = request.form['num_give']
    db.act_week.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update Rencana Selesai!'})

@app.route("/delete_week", methods=["POST"])
def act_week_bucket():
    num_receive = request.form['num_give']
    db.act_week.delete_one({'num': int(num_receive)})
    return jsonify({'msg': 'delete success!'})

@app.route("/act_week", methods=["GET"])
def act_week_get():
    act_week_list = list(db.act_week.find({}, {'_id': False}))
    return jsonify({'acts_week': act_week_list})

# Note
@app.route("/note", methods=["POST"])
def note_post():
    note_receive = request.form['note_give']

    count = db.note.count_documents({})
    num = count + 1

    doc = {
        'num': num,
        'note': note_receive,
        'done': 0,
    }
    db.note.insert_one(doc)
    return jsonify({'msg': 'Catatan Berhasil Ditambah!'})

@app.route("/note/done", methods=["POST"])
def note_done():
    num_receive = request.form['num_give']
    db.note.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update Rencana Selesai!'})

@app.route("/delete_note", methods=["POST"])
def note():
    num_receive = request.form['num_give']
    db.note.delete_one({'num': int(num_receive)})
    return jsonify({'msg': 'delete success!'})

@app.route("/note", methods=["GET"])
def note_get():
    note_list = list(db.note.find({}, {'_id': False}))
    return jsonify({'notes': note_list})

@app.route ('/about')
def about():
    return render_template('about.html')


@app.route ('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)   

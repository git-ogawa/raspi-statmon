"""Routing module
"""
import json
import subprocess
from pathlib import Path

from flask import render_template, url_for, flash, redirect, request,jsonify, abort
from flask_login import (
    login_user, current_user, logout_user, login_required, LoginManager
)

from mylogger import MyLogger
from statdata import Hardware, StatData
from auth import RegistrationForm, LoginForm
from database import User
from passhash import bcrypt
from database import db
from usermodel import UserModel, JinjaTemplate
from app import app


@app.route("/")
def root():
    return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        form = LoginForm(meta={'csrf': False})
        if not form.check_validate():
            MyLogger().write_log(f"{request.remote_addr} : login failed", "error")
            return render_template('login.html', title='Login', form=form, address=request.remote_addr)
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash("The user doesn't exist.", "danger")
            MyLogger().write_log(f"{request.remote_addr} : login failed", "error")
            return render_template('login.html', title='Login', form=form, address=request.remote_addr)
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            MyLogger().write_log(f"{request.remote_addr} : login success", "success")
            return redirect(url_for("home"))
        else:
            flash("The password is incorrect.", "danger")
            MyLogger().write_log(f"{request.remote_addr} : login failed", "error")
            return render_template('login.html', title='Login', form=form, address=request.remote_addr)
    return render_template('login.html', title='Login', address=request.remote_addr)


@app.route('/register', methods=["GET", 'POST'])
def register():
    if request.remote_addr != "127.0.0.1":
        abort()

    if request.method == "POST":
        form = RegistrationForm(meta={'csrf': False})
        if form.check_validate():
            username = request.form.get("username")
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Input user already exists.', "danger")
                return redirect(url_for('register'))
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                username=form.username.data,
                password=hashed_password)
            user_id = 1
            while user_id < 1000:
                if not User.query.filter_by(user_id=user_id).first():
                    break
                user_id += 1
            user.user_id = "{:03}".format(user_id)
            db.session.add(user)
            db.session.commit()
            flash("The account has been created!", "success")
            MyLogger().write_log("{} : created account".format(request.remote_addr), "success")
            return redirect(url_for("login"))
        else:
            return render_template('register.html', title='Register', form=form)
    else:
        return render_template('register.html', title='Register')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    MyLogger().write_log("{} : logout success".format(request.remote_addr), "success")
    return render_template("logout.html", title="Logout")


@app.route("/home")
@login_required
def home():
    hard = Hardware()
    info = hard.get_hard_info()
    settings = Path(__file__).resolve().parent / "config/settings/settings.json"
    with open(settings, "r") as f:
        json_data = json.load(f)
    return render_template("home.html", title="Home", data=info, graph=json_data)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='profile')


@app.route('/user_model')
@login_required
def user_model():
    settings = Path(__file__).resolve().parent / "config/user_model/model_prop.json"
    with open(settings, "r") as f:
        json_data = json.load(f)
    return render_template('user_model.html', title='user_model', graph=json_data)


@app.route('/model_value', methods=["POST", "GET"])
@login_required
def model_value():
    model = UserModel()
    data = {"data": model.get_value()}
    return jsonify(ResultSet=json.dumps(data))


@app.route('/add')
@login_required
def add():
    return render_template('add_pyfile.html', title='add_pyfile')


@app.route("/add_graph", methods=["GET", "POST"])
@login_required
def add_graph():
    if request.method == "POST":
        j = JinjaTemplate(request.form)
        j.make_template()
        msg = "The new model has been added."
        return render_template('result.html', title='result', msg=msg)
    return render_template('add_pyfile.html', title='add_pyfile')


@app.route("/remove_model", methods=["GET", "POST"])
@login_required
def remove_model():
    j = JinjaTemplate(request.form)
    j.remove_model()
    msg = "The current model has been removed."
    return render_template('result.html', title='result', msg=msg)


@app.route('/setting')
@login_required
def setting():
    p = Path()
    settings = p / "config/settings/settings.json"
    with open(settings, "r") as f:
        json_data = json.load(f)
    return render_template('settings.html', title='Settings', data=json_data)


@app.route("/change_settings", methods=["POST"])
@login_required
def change_settings():
    p = Path(__file__).resolve().parent
    settings = p / "config/settings/settings.json"
    with open(settings, "r") as f:
        json_data = json.load(f)

    params = request.form
    chart_type = params["chartType"]
    ret, msg = StatData().check_input_params(params, chart_type)
    if not ret:
        error = {chart_type: msg}
        return render_template(
            'settings.html',
            title='Settings',
            data=json_data,
            msg=error)
    for key, val in params.items():
        if "_" in key:
            k1, k2 = key.split("_")
            json_data["chart"][chart_type][k1][k2] = int(val)

    with open(settings, "w") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    msg = {chart_type: "Successsfully changed."}
    MyLogger().write_log("{} : changed settings".format(request.remote_addr), "success")
    return render_template(
        'settings.html',
        title='Settings',
        data=json_data,
        msg=msg)


@app.route("/chart-data", methods=["POST", "GET"])
def chart_data():
    if app.config["TEST"]:
        json_data = StatData().get_dummydata()
    else:
        json_data = StatData().get_alldata()
    return jsonify(ResultSet=json.dumps(json_data))


@app.route("/read_json", methods=["POST", "GET"])
@login_required
def read_json():
    settings = Path(__file__).resolve().parent / "config/settings/settings.json"
    with open(settings, "r") as f:
        json_data = json.load(f)
    print(json_data)
    return jsonify(ResultSet=json.dumps(json_data))


@app.route("/delete", methods=["POST", "GET"])
@login_required
def delete():
    try:
        username = request.form["user"]
        if username:
            user = User.query.filter_by(username=username).first()
            if user:
                if user.username == current_user.username:
                    flash(f"The user '{username}' is currently logged in", 'danger')
                else:
                    db.session.delete(user)
                    db.session.commit()
                    flash(f"The user '{username}' has been deleted",'success')
                    MyLogger().write_log(f"{request.remote_addr} : deleted account", "success")
            else:
                flash(f"The user '{username}' doesn't exist.")
                MyLogger().write_log(f"{request.remote_addr} : failed to delete account", "error")
            users = User.query.all()
            return render_template("delete.html", title="Delete account", form=users)
    except:
        users = User.query.all()
        return render_template("delete.html", title="Delete account", form=users)



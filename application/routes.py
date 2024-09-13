from flask.templating import render_template_string
from werkzeug.datastructures import RequestCacheControl
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import redirect

from application import app
from flask import render_template, request, redirect, flash, url_for

from bson import ObjectId

from .forms import TodoForm
from application import db
from datetime import datetime


@app.route("/")
def get_todos():
    todos = []
    for todo in db.todo_flask.find().sort("date_created", -1):
        todo["_id"] = str(todo["_id"])
        todo["date_created"] = todo["date_created"].strftime("%b %d %Y %H:%M:%S")
        todos.append(todo)

    return render_template("view_todos.html", todos = todos)
    

@app.route("/add_todo", methods = ['POST', 'GET'])
def add_todo():
    if request.method == "POST":
        form = TodoForm(request.form)
        todo_name = form.name.data
        todo_password = form.password.data
        email = form.email.data

        db.todo_flask.insert_one({
            "name": todo_name,
            "password": todo_password,
            "email": email,
            "date_created": datetime.utcnow()
        })
        flash("Todo successfully added", "success")
        return redirect("/")
    else:
        form = TodoForm()
    return render_template("add_todo.html", form = form)




@app.route("/update_todo/<id>", methods = ['POST', 'GET'])
def update_todo(id):
    if request.method == "POST":
        form = TodoForm(request.form)
        todo_name = form.name.data
        todo_password = form.password.data
        email = form.email.data

        db.todo_flask.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": todo_name,
            "password": todo_password,
            "email": email,
            "date_created": datetime.utcnow()
        }})
        flash("Todo successfully updated", "success")
        return redirect("/")
    else:
        form = TodoForm()

        todo = db.todo_flask.find_one_or_404({"_id": ObjectId(id)})
        form.name.data = todo.get("name", None)
        form.password.data = todo.get("password", None)
        form.email.data = todo.get("email", None)

    return render_template("add_todo.html", form = form)

@app.route("/delete_todo/<id>")
def delete_todo(id):
    db.todo_flask.find_one_and_delete({"_id": ObjectId(id)})
    flash("Todo successfully deleted", "success")
    return redirect("/")
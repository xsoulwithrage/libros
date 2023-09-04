from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import datetime

app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = MySQLConnector(app,'books_db')


@app.route('/')
def index():
    query = "SELECT * FROM books"                           
    book_list = mysql.query_db(query)                           
    return render_template('index.html', books=book_list) 


@app.route('/add', methods=['get'])
def add():
    return render_template("add.html")



@app.route('/destroy/<book_id>', methods=['get'])
def destroy(book_id):
    query = "SELECT * FROM books WHERE id = :id"
    data = {
        'id': book_id,
    }                          
    book_list = mysql.query_db(query, data)   
    return render_template("destroy.html", book=book_list)



@app.route('/edit/<book_id>', methods=['get'])
def edit(book_id):
    query = "SELECT * FROM books WHERE id = :id"
    data = {
        'id': book_id,
    } 
    book_list = mysql.query_db(query, data)   
    return render_template("update.html", book=book_list)


@app.route('/delete/<book_id>', methods=['get'])
def delete(book_id):
    query = "DELETE FROM books WHERE id = :id"
    data = {
        'id': book_id,
    }
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/update', methods=['post'])
def update():

    query = """UPDATE books SET title = :title, author = :author, updated_at = NOW()
                WHERE id = :book_id"""    
    data = {
        'book_id': request.form['book-id'],
        'title': request.form['title'],
        'author': request.form['author'],
    }
    mysql.query_db(query, data)
    return redirect('/')


@app.route('/create', methods=['post'])
def create():
    query = "INSERT INTO books (title, author, created_at, updated_at) VALUES (:title, :author, NOW(), NOW())"    
    data = {
        'title': request.form['title'],
        'author': request.form['author'],
    }
    mysql.query_db(query, data)
    return redirect('/')


@app.route('/process', methods=['post'])
def process():
    if request.form['action'] == "Update":
        return redirect('/edit/' + request.form['book-id'])
    if request.form['action'] == "Delete":
        return redirect('/destroy/' + request.form['book-id'])


@app.route('/verify', methods=['post'])
def verify():
    if request.form['action'] == "Cancel":
        return redirect('/')
    if request.form['action'] == "Delete":
        return redirect('/delete/' + request.form['book-id'])

app.run(debug=True)
from flask import Flask, render_template, session, request, make_response, redirect, url_for
import sqlite3
import datetime

"""
Для создания таблицы в БД blog.sqlite использовал комманду: 
create table posts (id int primary key autoincrement, title varchar(100), description text, date text);

"""




app = Flask(__name__)

app.secret_key = b'1234'

@app.route('/all')
def show_all(): # функция для вывода всех полей таблицы posts из БД
    connection = sqlite3.connect('blog.sqlite') #подключаюсь к БД
    cursor = connection.cursor() #Инициализирую курсор для последующего выполнения действий с БД
    cursor.execute("SELECT * FROM posts") # предаю SQL комманду в курсор на выполнение
    posts = cursor.fetchall() # присваиваю переменной posts результат SQL комманды
    connection.close()#закрываю соединенеи
    return render_template('index.html', posts = posts) # вывожу результат в темплейт

@app.route('/add')
def add(): #эта функция реализует добавление новых записей в таблицу posts
    date = str(datetime.datetime.now())# присавиваю переменной date сегодняшнюю дату
    title = request.args.get('title')#с пмощью get запроса счиатываю значение title
    description = request.args.get('description')#с пмощью get запроса счиатываю значение description
    # ниже выполенена проверка на заполнение значений title и description
    if not title:
        return 'Sorry, you should insert title'
    if not description:
        return 'Sorry, you should insert description'
    connection = sqlite3.connect('blog.sqlite') #соединяюсь с БД
    cursor = connection.cursor() #инициальзирую курсор
    values = (title, description, date) # присваиваю переменной values значения для заполнения, чтобы потом их не писать
    cursor.execute("INSERT INTO  posts (title, description, date) VALUES ( ?, ?, ?)", values) #передаю в курсор запрос к БД
    connection.commit()# отправляю SQL запрос в БД
    connection.close()# закрываю соединение
    return redirect('/all') #после выполнения функции перенаправляю к общему списку


@app.route('/edit')
def edit(): #функция выполняет редактирование полей в таблице posts
    id = request.args.get('id') # с помощью get запросаов считиваю id для обозначения поля, которое нужно редактировать и значения которые нужн озаменить
    title = request.args.get('title')
    description = request.args.get('description')
    if not id: # условия для проверки на заполнение данных
        return 'Sorry, you should insert number of post'
    if not title:
        return 'Sorry, you should insert title'
    if not description:
        return 'Sorry, you should insert description'
    connection = sqlite3.connect('blog.sqlite')
    cursor = connection.cursor()
    values = (title, description, id)
    cursor.execute("UPDATE posts SET title = ?, description = ? WHERE id = ?", values)
    connection.commit()
    connection.close()
    return redirect('/all')

@app.route('/del')
def delete():
    id = request.args.get('id')
    if not id:
        return 'Sorry, you should insert number of post'
    connection = sqlite3.connect('blog.sqlite')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM posts WHERE id=?", id)
    connection.commit()
    connection.close()
    return redirect('/all')



if __name__ == '__main__':
    app.run(debug=True, port = 5001)
# from flask import Flask, request, render_template
# import mysql.connector
#
#
# mydb = mysql.connector.connect (
#     host='localhost',
#     user='root',
#     password='23051368',
#     port='3306',
#     database='user')
#
# mycursor = mydb.cursor()
#
# app = Flask(__name__)
#
# # @app.route("/")
# # def index():
# #     reg()
#
#     # return 'Hello World'
#
# @app.route("/")
# def reg():
#     mycursor.execute("SELECT * FROM students")
#     value = mycursor.fetchall()
#     return render_template("registration.html", data=value)
#
#
#
# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask,render_template, request
# import mysql
from flask_mysqldb import MySQL

app = Flask (__name__)
#
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = "23051368"
# app.config['MYSQL_DB'] = ''

mysql = MySQL(app)


@app.route("/", methods=['POST', 'GET'])
def form():
    bmi = ''
    if request.method == 'POST' and 'Weight' in request.form and 'Height' in request.form:
        w = float(request.form.get('Weight'))
        h = float(request.form.get('Height'))
        bmi = round(w/((h/100)**2),3)

        # cur = mysql.connection.cursor
        # cur.execute("INSERT INTO users_weight (weight) VALUES (%s)",(weight))
        # mysql.connection.commit()
        # cur.close()

    return render_template("index.html", bmi=bmi)


app.run(host='localhost', port=5000)
if __name__ == "__main__":
    app.run(debug=True)



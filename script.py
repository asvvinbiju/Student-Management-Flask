from flask import *
import sqlite3 as sql
app = Flask(__name__)
app.secret_key = "studentmanagement"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/loginpage", methods=["POST", "GET"])
def loginpage():
    if request.method == "POST":
        conn = sql.connect("studentmanage.db")
        conn.row_factory = sql.Row
        cur = conn.cursor()
        username = request.form['username']
        password = request.form['password']
        cur.execute("SELECT PASSWORD, LOGINID, ROLE FROM TBLOGIN WHERE USERNAME=?",(username,))
        db_user = cur.fetchall()
        id = db_user[0]['loginid']
        db_password = db_user[0]['password']
        user_role = db_user[0]['role']
        if db_password == password:
            if user_role == 'student':
                session['username'] = username
                return redirect(url_for("studenthome", id=id))
            elif user_role == 'admin':
                session['username'] = username
                return redirect(url_for("adminhome", id=id))
            elif user_role == 'teacher':
                session['username'] = username
                cur.execute("SELECT APPROVE FROM TBTEACHER WHERE LOGINID=?",(id,))
                approve = cur.fetchall()
                for appr in approve:
                    conv_appr = dict(appr)
                    check_approve = conv_appr['APPROVE']
                if check_approve == "APPROVED" or check_approve == "approved":
                    return redirect(url_for("teacherhome", id=id))
                else:
                    return "Teacher is not approved by admin."
            else:
                return "User not approved!"
        else:
            return "incorrect password or username"
    else:
        return render_template("loginpage.html")
    

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("home"))


@app.route("/signuppage", methods=["POST", "GET"])
def signuppage():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        age = request.form['age']
        department = request.form['department']
        gender = request.form.get("gender")
        conn = sql.connect("studentmanage.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO TBLOGIN(USERNAME, PASSWORD, ROLE) VALUES (?,?,?)",(username, password, "student"))
        cur.execute("SELECT MAX(LOGINID) FROM TBLOGIN;")
        id = cur.fetchone()[0]
        cur.execute("INSERT INTO TBSTUDENT(FULLNAME, EMAIL, AGE, PHONE, GENDER, DEPARTMENT, LOGINID) VALUES (?,?,?,?,?,?,?)", (fullname, email, age, phone, gender, department, id,))
        conn.commit()
        return redirect(url_for("loginpage"))
    else:
        return render_template("signup.html")
    
    
@app.route("/studenthome/<int:id>")
def studenthome(id):
    conn = sql.connect("studentmanage.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM TBSTUDENT WHERE LOGINID=?;",(id,))
    student = cur.fetchone()
    return render_template("studenthome.html", student=student, id=id)


@app.route("/editstudent/<int:id>", methods=["POST", "GET"])
def editstudent(id):
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        age = request.form['age']
        department = request.form['department']
        gender = request.form.get("gender")
        conn = sql.connect("studentmanage.db")
        cur = conn.cursor()
        cur.execute("UPDATE TBLOGIN SET USERNAME=?, PASSWORD=? WHERE LOGINID=?",(username, password, id))
        cur.execute("UPDATE TBSTUDENT SET FULLNAME=?, EMAIL=?, AGE=?, PHONE=?, GENDER=?, DEPARTMENT=? WHERE LOGINID=?", (fullname, email, age, phone, gender, department, id))
        conn.commit()
        return redirect(url_for("studenthome", id=id))
    else:
        conn = sql.connect("studentmanage.db")
        conn.row_factory = sql.Row
        cur = conn.cursor()
        cur.execute("SELECT USERNAME, PASSWORD FROM TBLOGIN WHERE LOGINID=?;",(id,))
        user = cur.fetchone()
        cur.execute("SELECT * FROM TBSTUDENT WHERE LOGINID=?;",(id,))
        student = cur.fetchone()
        return render_template("editstudent.html", user=user, student=student, id=id)


@app.route("/teacherhome/<int:id>")
def teacherhome(id):
    conn = sql.connect("studentmanage.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM TBTEACHER WHERE LOGINID=?;",(id,))
    teacher = cur.fetchone()
    return render_template("teacherhome.html", teacher=teacher, id=id)


@app.route("/teacheredit/<int:id>", methods=["POST", "GET"])
def teacheredit(id):
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        gender = request.form.get("gender")
        conn = sql.connect("studentmanage.db")
        cur = conn.cursor()
        cur.execute("UPDATE TBLOGIN SET USERNAME=?, PASSWORD=? WHERE LOGINID=?",(username, password, id))
        cur.execute("UPDATE TBTEACHER SET FULLNAME=?, EMAIL=?, PHONE=?, GENDER=?, DEPARTMENT=? WHERE LOGINID=?", (fullname, email, phone, gender, department, id))
        conn.commit()
        return redirect(url_for("teacherhome", id=id))
    else:
        conn = sql.connect("studentmanage.db")
        conn.row_factory = sql.Row
        cur = conn.cursor()
        cur.execute("SELECT USERNAME, PASSWORD FROM TBLOGIN WHERE LOGINID=?;",(id,))
        user = cur.fetchone()
        cur.execute("SELECT * FROM TBTEACHER WHERE LOGINID=?;",(id,))
        teacher = cur.fetchone()
        return render_template("editteacher.html", user=user, teacher=teacher, id=id)
    
    
@app.route("/teachstudent/<int:id>")
def teachstudent(id):
    conn = sql.connect("studentmanage.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM TBSTUDENT;")
    students = cur.fetchall()
    return render_template("teachstudents.html", students=students, id=id)


@app.route("/adminhome/<int:id>")
def adminhome(id):
    conn = sql.connect("studentmanage.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM TBADMIN WHERE LOGINID=?;",(id,))
    admin = cur.fetchone()
    cur.execute("SELECT * FROM TBSTUDENT;")
    return render_template('adminhome.html', admin=admin, id=id)


@app.route("/studentview/<int:id>")
def studentview(id):
    conn = sql.connect("studentmanage.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM TBSTUDENT;")
    students = cur.fetchall()
    return render_template('studentview.html', students=students, id=id)


@app.route("/teacherview/<int:id>")
def teacherview(id):
    conn = sql.connect("studentmanage.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM TBTEACHER;")
    teachers = cur.fetchall()
    return render_template('teacherview.html', teachers=teachers, id=id)


@app.route("/approveteacher/<int:id>", methods=["POST", "GET"])
def approveteach(id):
    conn = sql.connect("studentmanage.db")
    cur = conn.cursor()
    cur.execute("UPDATE TBTEACHER SET APPROVE='APPROVE' WHERE LOGINID=?",(id,))
    conn.commit()
    return redirect(url_for("teacherview", id=id))


@app.route("/teachersignup/<int:id>", methods=["POST", "GET"])
def teachersignup(id):
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        gender = request.form.get("gender")
        conn = sql.connect("studentmanage.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO TBLOGIN(USERNAME, PASSWORD, ROLE) VALUES (?,?,?)",(username, password, "teacher"))
        cur.execute("SELECT MAX(LOGINID) FROM TBLOGIN;")
        id = cur.fetchone()[0]
        cur.execute("INSERT INTO TBTEACHER(FULLNAME, EMAIL, PHONE, GENDER, DEPARTMENT,  APPROVE, LOGINID) VALUES (?,?,?,?,?,?)", (fullname, email, phone, gender, department,'not approved', id,))
        conn.commit()
        return redirect(url_for("teacherview", id=id))
    else:
        return render_template("addteacher.html", id=id)


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Gc@19102006'
app.config['MYSQL_DB'] = 'jobportal'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                    (username, email, password, role))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        salary = request.form['salary']
        location = request.form['location']
        company = request.form['company']
        employer_id = 1  # Replace with logged-in user's ID

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO jobs (title, description, salary, location, company, employer_id) VALUES (%s, %s, %s, %s, %s, %s)",
                    (title, description, salary, location, company, employer_id))
        mysql.connection.commit()
        cur.close()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('post_job.html')

@app.route('/jobs')
def job_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jobs")
    jobs = cur.fetchall()
    cur.close()
    return render_template('job_list.html', jobs=jobs)

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
    job = cur.fetchone()
    cur.close()
    return render_template('job_detail.html', job=job)

if __name__ == '__main__':
    app.run(debug=True)
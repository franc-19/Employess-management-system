from flask import Flask, render_template, url_for, request, jsonify, redirect
import firebase_admin
from firebase_admin import credentials, auth, firestore
import pyrebase

app = Flask(__name__)

# initialize firebase
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

# firebase configuration for pyrebase use
firebase_config = {
  "apiKey": "AIzaSyBfy-CXZs1amdH8NI28NOCq3YrqyUIYdj4",
  "authDomain": "employees-management-sys-6b4c6.firebaseapp.com",
  "databaseURL": "YOUR_DATABASE_URL",
  "projectId": "employees-management-sys-6b4c6",
  "storageBucket": "employees-management-sys-6b4c6.appspot.com",
  "messagingSenderId": "948493740051",
  "appId": "1:948493740051:web:e9b34ae24ed107076f37e6",
  "measurementId": "G-FFJZGLXG91"
}
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firestore.client()


@app.route('/')
def landing_page():
    return render_template('homepage.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    # get request body & retrieve submitted email & password
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # verify credentials with those in firebase
        try:
            # authenticate in firebase
            user = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except Exception as e:
            # handle errors
            return jsonify({"message": str(e)}), 400
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    # get user details
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm-password")

    # confirm password
    if password != confirm_password:
        # notify user wrong password
        return "Wrong password"

    try:
        user = auth.create_user_with_email_and_password(email, password)
        
        return redirect(url_for('login'))
    except Exception as e:
        # alert user on errors during signup
        return f"Error: {e}"

    return render_template('signup.html')

@app.route('/home')
def home():
    students_ref = db.collection("Employee's Details")
    students = students_ref.get()  # Retrieve all documents in the collection

    student_data = []
    for student in students:
        student_data.append(student.to_dict())
    return render_template('home.html', students=student_data)

if __name__ == '__main__':
    app.run(debug=True)
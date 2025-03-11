from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Store user data in a text file
USER_FILE = "users.txt"

# Save user data to a text file
def save_user(username, password):
    with open(USER_FILE, "a") as file:
        file.write(f"{username},{password}\n")

# Check if user exists in the text file
def user_exists(username, password):
    try:
        with open(USER_FILE, "r") as file:
            users = file.readlines()
            for user in users:
                saved_username, saved_password = user.strip().split(",")
                if saved_username == username and saved_password == password:
                    return True
    except FileNotFoundError:
        return False
    return False

@app.route("/")
def home():
    if "user" in session:
        return render_template("index.html", username=session["user"])
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if user_exists(username, password):
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return "Invalid Credentials. Try Again!"

    return '''
    <h2>Login</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <a href="/signup">Signup here</a></p>
    '''

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not user_exists(username, password):
            save_user(username, password)
            return redirect(url_for("login"))
        else:
            return "Username already exists!"

    return '''
    <h2>Signup</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Choose Username" required>
        <input type="password" name="password" placeholder="Choose Password" required>
        <button type="submit">Signup</button>
    </form>
    <p>Already have an account? <a href="/login">Login here</a></p>
    '''

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
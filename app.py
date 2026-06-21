from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from pathlib import Path
from dotenv import load_dotenv

# Always load .env from the same folder as this script, regardless of working directory
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)

# Read credentials once at startup so they are always available
MY_EMAIL     = os.getenv("MY_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

app = Flask(__name__)
app.secret_key = 'super_secret_portfolio_key'  # Needed for flashing messages

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/project")
def projects():
    return render_template('project.html')

@app.route('/pictures')
def pictures():
    return render_template("pictures.html")

@app.route('/videos')
def videos():
    return render_template("videos.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name         = request.form.get('name')
        sender_email = request.form.get('email')
        message      = request.form.get('message')

        try:
            # Set up the email message
            msg = MIMEMultipart()
            msg['From']    = MY_EMAIL  # Using your email as the sender
            msg['To']      = MY_EMAIL  # Sending to yourself
            msg['Subject'] = f"New Portfolio Message from {name}"

            body = f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message}"
            msg.attach(MIMEText(body, 'plain'))

            # Connect to Gmail SMTP Server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(MY_EMAIL, APP_PASSWORD)
            server.send_message(msg)
            server.quit()

            flash("Awesome! Your message has been sent successfully. 🚀", "success")
        except Exception as e:
            flash("Oops! Something went wrong. Please check your App Password.", "danger")
            print(e)

        return redirect(url_for('contact'))

    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)
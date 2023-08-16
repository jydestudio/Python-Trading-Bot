from flask import Flask, render_template
from flask_mail import Mail, Message
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

subject = 'HTML Email Template'
to_email = 'fatokilawrence2002@gmail.com'
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'stacktradingassistant@gmail.com'
smtp_password = '@appbrewery1'

@app.route("/")
def home():
    try:
        email_template = render_template('email-template.html', name="John", confirm_url="https://click.me")

        # Create a MIMEText object to represent the email content
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(email_template, 'html'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Use TLS
            server.login(smtp_username, smtp_password)
            print("login successfully")
            server.sendmail(smtp_username, to_email, msg.as_string())
            print('Email sent successfully')

    except Exception as e:
        print(f'Error sending email: {e}')

    return render_template("email-template.html", name="John", confirm_url="https://click.me")


if __name__ == "__main__":
    app.run(port=2000, debug=True)
from flask import Flask, render_template, request
import requests
import smtplib

app = Flask(__name__)
posts = requests.get("https://api.npoint.io/717b2a5aef5c060c7f12").json()
EMAIL = "YOUR_EMAIL"
PASSWORD = "YOUR_PASSWORD"

@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # data = request.form
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


# @app.route('/form-entry', methods=["POST"])
# def receive_data():
#     # name = request.form["name"]
#     # email = request.form["email"]
#     # phone = request.form["phone"]
#
#     data = request.form
#     print(data["name"])
#     print(data["email"])
#     print(data["phone"])
#     print(data["message"])
#
#     return "<h1> Successfully sent a message..</h1>"


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


# def send_email(name, email, phone, message):
#     email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
#     with smtplib.SMTP("smtp.gmail.com") as connection:
#         connection.starttls()
#         connection.login(EMAIL, PASSWORD)
#         connection.sendmail(EMAIL, EMAIL, email_message)

def send_email(name, email, phone, message):
    # Construct the email message
    email_message = f"""\
Subject: New Message from Contact Form

Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}
"""
    try:
        # Connect to the SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()  # Secure the connection
            connection.login(EMAIL, PASSWORD)  # Login to your email account
            # Send the email (From, To, Message)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs="SENDER_EMAIL",  # Send to the recipient email
                msg=email_message
            )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    app.run(debug=True)
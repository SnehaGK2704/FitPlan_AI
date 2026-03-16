import random
from flask_mail import Mail, Message

mail = Mail()


def init_mail(app):

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'snehagkudur@gmail.com'
    app.config['MAIL_PASSWORD'] = 'oeqj uxds unkr wgnp'

    mail.init_app(app)


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp(app, email, otp):

    with app.app_context():

        msg = Message(
            "FitPlan AI Login OTP",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )

        msg.body = f"Your OTP for FitPlan AI login is: {otp}"

        mail.send(msg)
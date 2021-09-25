from flask import (
    Blueprint, render_template, request,
    redirect, url_for, current_app
)

import sendgrid
from sendgrid.helpers.mail import *

bp = Blueprint('portfolio', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index():
    return render_template('portfolio/index.html')


@bp.route('/mail', methods=['GET', 'POST'])
def mail():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if request.method == 'POST':
        send_mail(name, email, message)

        return render_template('portfolio/sent_mail.html')

    return render_template(url_for('portfolio.index'))


def send_mail(name, email, message):
    my_email = current_app.config['MY_EMAIL']
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_KEY'])

    from_email = Email(current_app.config['SEND_EMAIL'])
    to_email = To(my_email, substitutions={
        "-name-": name,
        "-email-": email,
        "-message-": message,
    })

    html_content = """
        <p>Hola Patrick, tienes un nuevo contacto desde la web:</p>
        <p>Name: -name-</p>
        <p>Email: -email-</p>
        <p>Message: -message-</p>
    """

    mail = Mail(from_email, to_email, 'New contact from website', html_content=html_content)

    response = sg.client.mail.send.post(request_body=mail.get())

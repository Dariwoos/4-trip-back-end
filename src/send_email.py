import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def sendEmail(email):
    message = Mail(
        from_email="mgomez+test@4geeks.co",
        to_emails=email,
        subject='has recibido una oferta',
        html_content='<strong>Un profesional te ha enviado una oferta</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print('status code',response.status_code)
        print('body',response.body)
        print('header',response.headers)
    except Exception as e:
        print('error',e)
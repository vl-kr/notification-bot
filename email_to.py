import smtplib, ssl

port = 465  # For SSL
password = ""

smtp_server = "smtp.gmail.com"
sender_email = "example_sender@gmail.com"  # sender address
receiver_email = "example_receiver@gmail.com"  # receiver address


def send_message(message, snd=False):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)

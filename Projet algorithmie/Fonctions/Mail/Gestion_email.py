import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def envoyer_email(email, sujet, message):
    """Envoie un email à un utilisateur."""
    try:
        # Configuration de l'email
        sender_email = "corentinguyard2002@gmail.com"
        sender_password = "hgmp phxw zagn pykg"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Création du message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = sujet
        msg.attach(MIMEText(message, 'plain'))

        # Connexion au serveur SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Envoi de l'email
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()

    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

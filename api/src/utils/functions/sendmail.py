from loguru import logger
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from datetime import datetime
from api.src.utils.logs.index import log_file
from dotenv import load_dotenv

load_dotenv()

def sendmail():
    # Configurações
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    email_origem = os.getenv("EMAIL_ORIGEM")
    email_destino = os.getenv("EMAIL_DESTINO")
    senha_app = os.getenv("EMAIL_SENHA")  # Use a senha de app do Gmail
    
    msg = MIMEMultipart()
    msg["From"] = email_origem
    msg["To"] = email_destino
    msg["Subject"] = f"Quality_rj_ce - Log em anexo ({data_hoje})"

    msg.attach(MIMEText("Segue em anexo o log da automação.", "plain"))

    # Anexo do log como .txt
    with open(log_file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename=automation.txt")
        msg.attach(part)

    # Envio
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email_origem, senha_app)
        server.send_message(msg)
        

    logger.success(f"✅ Log enviado com sucesso para {email_destino}")  
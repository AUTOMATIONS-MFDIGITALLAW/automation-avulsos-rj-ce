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

def sendmail(assunto_extra="Log AUTO_AVULSOS-RJ-CE"):
    from datetime import datetime

    data_hoje = datetime.now().strftime("%d/%m/%Y")
    email_origem = os.getenv("EMAIL_ORIGEM")
    email_destino = os.getenv("EMAIL_DESTINO")
    senha_app = os.getenv("EMAIL_SENHA")

    if not email_origem or not email_destino or not senha_app:
        logger.error("❌ Variáveis de ambiente ausentes.")
        return

    msg = MIMEMultipart()
    msg["From"] = email_origem
    msg["To"] = email_destino
    msg["Subject"] = f"⚠️ ALERTA: {assunto_extra} ({data_hoje})"

    if "ALERTA" in assunto_extra.upper():
        corpo = "⚠️ A automação parece ter parado. Verifique o sistema!"
    else:
        corpo = "Segue em anexo o log da automação NAME_ROBÔ."

    msg.attach(MIMEText(corpo, "plain"))

    try:
        with open(log_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename=automation.txt")
            msg.attach(part)
    except FileNotFoundError:
        logger.warning("📂 Arquivo de log não encontrado, enviando e-mail sem anexo.")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_origem, senha_app)
            server.send_message(msg)
        logger.success(f"✅ E-mail enviado com sucesso para {email_destino}")
    except Exception as e:
        logger.error(f"❌ Falha ao enviar e-mail: {e}")

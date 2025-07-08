from loguru import logger
import os
from datetime import datetime

# Cria a pasta 'logs' se não existir
log_dir = os.path.join("logs")
os.makedirs(log_dir, exist_ok=True)

# Define o padrão da data de hoje (só a data)
today_str = datetime.now().strftime('%Y-%m-%d')

# Procura se já existe um log de hoje
existing_logs = [
    f for f in os.listdir(log_dir)
    if f.startswith(f"automation_{today_str}") and f.endswith(".log")
]

if existing_logs:
    # Usa o log mais recente
    existing_logs.sort(reverse=True)
    log_filename = existing_logs[0]
else:
    # Cria novo log com hora atual
    log_filename = f"automation_{today_str}_{datetime.now().strftime('%H-%M-%S')}.log"
   
    
# Caminho completo
log_file = os.path.join(log_dir, log_filename)
from datetime import datetime

# Cria a pasta 'logs' se não existir
log_dir = os.path.join("logs")
os.makedirs(log_dir, exist_ok=True)

# Define o padrão da data de hoje (só a data)
today_str = datetime.now().strftime('%Y-%m-%d')

# Procura se já existe um log de hoje
existing_logs = [
    f for f in os.listdir(log_dir)
    if f.startswith(f"automation_{today_str}") and f.endswith(".log")
]

if existing_logs:
    # Usa o log mais recente
    existing_logs.sort(reverse=True)
    log_filename = existing_logs[0]
else:
    # Cria novo log com hora atual
    log_filename = f"automation_{today_str}_{datetime.now().strftime('%H-%M-%S')}.log"
   
    
# Caminho completo
log_file = os.path.join(log_dir, log_filename)

# Configurar o arquivo de log
logger.add(log_file, rotation="1 MB", retention="10 days", level="INFO", format="{time} - {level} - {message}")


log = logger


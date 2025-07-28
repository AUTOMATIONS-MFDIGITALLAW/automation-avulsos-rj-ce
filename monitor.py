from datetime import datetime, timedelta
import signal
import subprocess
from time import sleep
import os
from api.src.utils.functions.sendmail import sendmail # Usa sua função já pronta
from api.src.utils.logs.index import log

HEARTBEAT_FILE = "C:/Users/NAME_DIRETORY/Documents/automation-avulsos-rj-ce/api/src/utils/functions/heartbeat.txt"
INTERVALO = 10 # minutos #esse tempo e pra test
INTERVALO_LOOP = 240 #esse tempo e pra test
MAX_ALERTAS_CONSECUTIVOS = 2

def check_heartbeat():
    sleep(60) #o Tempo aqui e de 60 seg
    if not os.path.exists(HEARTBEAT_FILE):
        log.warning("⚠️ Arquivo de heartbeat não encontrado.")
        return False

    try:
        with open(HEARTBEAT_FILE, "r") as f:
            ultima_execucao = datetime.fromisoformat(f.read().strip())
    except Exception as e:
        log.error(f"❌ Erro ao ler o heartbeat: {e}")
        return False

    tempo_passado = datetime.now() - ultima_execucao
    if tempo_passado > timedelta(minutes=INTERVALO):
        return False
    return True

if __name__ == "__main__":
    alertas_consecutivos = 0
    log.info("🟡 Iniciando monitoramento do heartbeat...")
    
    automacao_proc = subprocess.Popen(["python", "app.py"])

    try:
        while True:
            if not check_heartbeat():
                log.error("❌ NAME_ROBÔ parada por mais de 10 minutos. Enviando alerta por e-mail...")
                sendmail("Automação Robô_NAME parada há mais de 10 minutos")
                
                alertas_consecutivos += 1
                
                if alertas_consecutivos >= MAX_ALERTAS_CONSECUTIVOS:
                    log.critical("🛑 Número máximo de alertas consecutivos atingido. Encerrando monitoramento.")
                    automacao_proc.send_signal(signal.SIGINT)
                    break
            else:
                alertas_consecutivos = 0
                log.info("✅ Automação rodando normalmente.")
                
            sleep(INTERVALO_LOOP)
    except KeyboardInterrupt:
        log.info("🛑 Monitoramento interrompido manualmente.")     
        automacao_proc.terminate()

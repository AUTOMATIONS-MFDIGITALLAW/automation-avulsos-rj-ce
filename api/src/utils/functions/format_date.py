from datetime import datetime, time
import pandas as pd

def format_date(raw_date) -> str:
    """
    Recebe qualquer tipo de dado vindo do pandas/openpyxl e retorna apenas a data no formato DD/MM/AAAA.
    """
    if pd.isna(raw_date):
        return ''
    
    # Caso seja datetime completo
    if isinstance(raw_date, datetime):
        return raw_date.strftime('%d/%m/%Y')
    
    # Caso seja string, tenta parsear várias possibilidades
    if isinstance(raw_date, str):
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y %H:%M:%S', '%d/%m/%Y'):
            try:
                dt = datetime.strptime(raw_date, fmt)
                return dt.strftime('%d/%m/%Y')
            except ValueError:
                continue
        # Se nenhuma bater
        return ''
    
    # Caso seja número serial (float ou int) vindo do Excel
    if isinstance(raw_date, (float, int)):
        try:
            excel_date = pd.to_datetime(raw_date, unit='d', origin='1899-12-30')
            return excel_date.strftime('%d/%m/%Y')
        except Exception:
            return ''
    
    # Se não conseguiu interpretar
    return ''
    
def format_hora(raw_date) -> str:
    """
    Recebe qualquer tipo de dado vindo do pandas/openpyxl e retorna só a hora (HH:MM).
    """
    if pd.isna(raw_date):
        return ''
    
    # Caso seja datetime completo
    if isinstance(raw_date, datetime):
        return raw_date.strftime('%H:%M')
    
    # Caso seja só time
    if isinstance(raw_date, time):
        return raw_date.strftime('%H:%M')
    
    # Caso seja string, tenta parsear várias possibilidades
    if isinstance(raw_date, str):
        for fmt in ('%H:%M:%S', '%H:%M', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M:%S'):
            try:
                dt = datetime.strptime(raw_date, fmt)
                return dt.strftime('%H:%M')
            except ValueError:
                continue
        # Se cair aqui, é pq nenhuma bateu
        return ''
    
    # Caso seja número serial (float ou int) vindo do Excel
    if isinstance(raw_date, (float, int)):
        try:
            # Converte número serial do Excel para datetime
            excel_date = pd.to_datetime(raw_date, unit='d', origin='1899-12-30')
            return excel_date.strftime('%H:%M')
        except Exception:
            return ''
    
    # Se não conseguiu interpretar
    return ''
    

from time import sleep
import pyperclip as pyp
import pyautogui as pya
import keyboard as key
from api.src.utils.functions.format_date import format_date, format_hora
from api.src.utils.functions.capture_img import ScreenImage
from api.src.utils.functions.click_position import click_and_fill_novo
from api.src.utils.logs.index import log
from api.src.scripts.base.base_scripts import BaseTask

class AllSeach(BaseTask):
    def __init__(self, row):
        super().__init__(row)
        self.screen = ScreenImage()
        
    def execute(self):
        return super().execute()
    
    
class AudienciaProcess(AllSeach):
    def __init__(self, row):
        super().__init__(row)


    def insert_audiencia(self):
        log.info('🔍 Iniciando Agenda de Audiencia')
        
        try:  
            pya.click(1016, 512, button='right')
            ScreenImage.wait_and_click('novo', "botao novo da agenda",)
            ScreenImage.wait_and_click('audiencia', "Botao Audiencia",)
            
            date_audiencia = format_date(self.row['DATA AUDIENCIA'])
            hora_audiencia = format_hora(self.row['HORA AUDIENCIA'])
            log.info(f'DATA AUDIENCIA:{date_audiencia} HORA AUDIENCIA:{hora_audiencia}')
            pyp.copy(date_audiencia)
            ScreenImage.wait_and_click('nova_nota', 'Nova Nota')
            click_and_fill_novo('data_nota')
            pya.hotkey('ctrl', 'a')
            sleep(2)
            pya.hotkey('ctrl', 'v')
            sleep(2)
            key.press('tab')
            sleep(2)
            pyp.copy(hora_audiencia)
            sleep(2)
            pya.hotkey('ctrl', 'v')
            sleep(2)
            ScreenImage.wait_and_click('etiqueta', "Etiqueta Verde",)
            ScreenImage.wait_and_click('filtrar', "Filtrar",)
            sleep(2)
            key.write('CONCILIACAO')
            sleep(4)
            click_and_fill_novo('conciliacao')
            ScreenImage.wait_and_click('yes_agenda', "Yes",)
            ScreenImage.wait_and_click('ok_azul', "Ok",)
            ScreenImage.wait_and_click('ok_azul', "Ok",)
            if ScreenImage.find_img('yes_agenda', 'Yes', 'click'):
                sleep(2)
            if ScreenImage.find_img('ok_azul', "Ok", 'click'):
                sleep(2)
            
            
            
        except Exception as e:
            log.error(f'❌ ERRO na audiencia: {e}')
        
from time import sleep
import pyperclip as pyp
import pyautogui as pya
import keyboard as key
from api.src.utils.functions.format_date import format_date, format_hora
from api.src.utils.functions.capture_img import ScreenImage
from api.src.utils.functions.click_position import click_and_fill, click_and_fill_novo
from api.src.utils.logs.index import log
from api.src.scripts.base.base_scripts import BaseTask

class AllSeach(BaseTask):
    def __init__(self, row):
        super().__init__(row)
        self.screen = ScreenImage()
        
    def execute(self):
        return super().execute()
    
    
class CitacaoProcess(AllSeach):
    def __init__(self, row):
        super().__init__(row)


    def insert_citacao(self):
        log.info('🔍 Iniciando Citaçao de Processo')     
        
        try:  
            date_citacao = format_date(self.row['DATA DE CITAÇÃO/INTIMAÇÃO'])
            hora_citacao = self.row['HORA DE CITAÇÃO/INTIMAÇÃO']
            log.info(f'DATA DE CITAÇÃO/INTIMAÇÃO:{date_citacao}, HORA :{hora_citacao}')
            pyp.copy(date_citacao)
            sleep(3)
            click_and_fill_novo('data_nota')
            pya.hotkey('ctrl', 'a')
            sleep(2)
            pya.hotkey('ctrl', 'v')
            sleep(2)
            pya.press('tab')
            sleep(2)
            pyp.copy(hora_citacao)
            sleep(2)
            pya.hotkey('ctrl', 'v')
            sleep(2)
            ScreenImage.wait_and_click('etiqueta', "Etiqueta Verde",)
            ScreenImage.wait_and_click('filtrar', "Filtrar",)
            sleep(2)
            key.write('DATA DE CITAÇÃO')
            sleep(2)
            ScreenImage.wait_and_click('checkbox', "Checkbox",)
            ScreenImage.wait_and_click('yes_agenda', "Yes",)
            ScreenImage.wait_and_click('ok_azul', "Ok",)
            ScreenImage.wait_and_click('ok_azul', "Ok",)
            if ScreenImage.find_img('yes_agenda', 'Yes', 'click'):
                sleep(2)
                ScreenImage.wait_and_click('ok_azul', "Ok",)
                
            log.success('Agenda de Citação inserido com sucesso')
            
            
        except Exception as e:
            log.error(f'❌ ERRO na citação: {e}')
        
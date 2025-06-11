from time import sleep
import pyperclip as pyp
import pyautogui as pya
import keyboard as key
from api.src.utils.functions.format_date import format_date
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
    
    
class SentencaProcess(AllSeach):
    def __init__(self, row):
        super().__init__(row)


    def insert_sentenca(self):
        log.info('🔍 Iniciando Agenda de Sentença')     
        
        try:  
            pya.click(1016, 512, button='right')
            ScreenImage.wait_and_click('novo', "botao novo da agenda",)
            ScreenImage.wait_and_click('decisao', "Botao Decisão",)
            
            date_citacao = format_date(self.row['DATA DE CITAÇÃO/INTIMAÇÃO'])
            log.info(f'DATA DE CITAÇÃO/INTIMAÇÃO:{date_citacao}')
            pyp.copy(date_citacao)
            sleep(3)
            click_and_fill_novo('data_tutela')
            pya.hotkey('ctrl', 'a')
            sleep(2)
            pya.hotkey('ctrl', 'v')
            ScreenImage.wait_and_click('etiqueta', "Etiqueta Verde",)
            ScreenImage.wait_and_click('filtrar', "Filtrar",)
            sleep(2)
            key.write('SENTENCA')
            sleep(2)
            ScreenImage.wait_and_click('checkbox', "Checkbox",)
            ScreenImage.wait_and_click('yes_agenda', "Yes",)
            ScreenImage.wait_and_click('ok_azul', "Ok",)
            sleep(2)
            ScreenImage.wait_and_click('ok_azul', "Ok",)
            if ScreenImage.find_img('yes_agenda', 'Yes', 'click'):
                sleep(2)
            if ScreenImage.find_img('ok_azul', "Ok", 'click'):
                sleep(2)
                
            log.success('Agenda de Sentença inserido com sucesso')
            
            
            
        except Exception as e:
            log.error(f'❌ ERRO ao detalhes de  processo: {e}')
        
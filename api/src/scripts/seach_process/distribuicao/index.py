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
    
    
class DistribuicaoProcess(AllSeach):
    def __init__(self, row):
        super().__init__(row)


    def insert_distribuicao(self):
        log.info('🔍 Iniciando Distribuicao de Processo')     
        
        try:  
            ScreenImage.wait_and_click('adv_agenda', "Tela de Agenda",)            
            pya.click(1016, 512, button='right')
            ScreenImage.wait_and_click('novo', "botao novo da agenda",)
            ScreenImage.wait_and_click('prazo', "botao prazo da agenda",)
            date_distribuicao = format_date(self.row['DATA DISTRIBUICAO'])
            log.info(f'📅 Data de Distribuição: {date_distribuicao}')
            pyp.copy(date_distribuicao)
            sleep(3)
            ScreenImage.wait_and_click('nova_nota', "nova nota",)
            click_and_fill_novo('data_nota')
            pya.hotkey('ctrl', 'a')
            sleep(2)
            pya.hotkey('ctrl', 'v')
            sleep(2)           
            ScreenImage.wait_and_click('etiqueta', "Etiqueta Verde",)
            ScreenImage.wait_and_click('filtrar', "Filtrar",)
            sleep(2)
            key.write('DATA DE DISTRIBUIÇÃO')
            sleep(2)
            ScreenImage.wait_and_click('checkbox', "Checkbox",)
            ScreenImage.wait_and_click('yes_agenda', "Yes",)
            ScreenImage.wait_and_click('ok_azul', "Ok",)
            ScreenImage.wait_and_click('ok_azul', "Ok",)
            if ScreenImage.find_img('yes_agenda', 'Yes', 'click'):
                sleep(2)
                ScreenImage.wait_and_click('ok_azul', "Ok",)
                
            log.success('Agenda de distribuicao inserido com sucesso')
            
            
        except Exception as e:
            log.error(f'❌ ERRO na distribuicao: {e}')
        
import cv2
import numpy as np
import pyautogui as pya
import time
from api.src.utils.map_path.index import IMAGE_PATH
from api.src.utils.logs.index import log

class ScreenImage:
    
    def capture_screenshot(filename="screenshot.png"):
        """ Captura uma captura de tela e salva em um arquivo """
        screenshot = pya.screenshot()  # Captura a tela atual
        screenshot.save(filename)      # Salva a captura de tela em um arquivo
        return filename                # Retorna o nome do arquivo salvo

    def find_element_on_screen(element_image_path, threshold=0.8):
        """ Encontra um elemento na tela baseado em uma imagem """
        screenshot_path = ScreenImage.capture_screenshot()  # Captura a tela e obtém o caminho do arquivo
        screenshot = cv2.imread(screenshot_path, 0)  # Lê a captura de tela em grayscale
        template = cv2.imread(element_image_path, 0)  # Lê a imagem do elemento a ser encontrado
        
        if template is None or screenshot is None:
            log.error(f"Erro ao carregar as imagens: {element_image_path} ou screenshot")
            return None, None

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)  
        loc = np.where(result >= threshold)  # Encontra os locais onde há correspondência

        if len(loc[0]) > 0:
            return loc, template.shape  # Retorna as coordenadas dos locais encontrados e as dimensões do template
        return None, None  # Retorna None se nenhum local for encontrado

    def click_element_on_screen(element_image_path, threshold=0.8):
        """ Clica em um elemento na tela baseado em uma imagem """
        loc, template_shape = ScreenImage.find_element_on_screen(element_image_path, threshold)
        if loc:
            for pt in zip(*loc[::-1]):
                center_x = pt[0] + template_shape[1] // 2
                center_y = pt[1] + template_shape[0] // 2
                pya.click(center_x, center_y)
                return True  # Retorna True se o clique foi realizado
        return False  # Retorna False se o clique não foi realizado

    @staticmethod
    def wait_and_click(image_alias, description):
        """ Aguarda até que o elemento apareça na tela e clica nele """
        log.info(f'⌛ Aguardando {description} aparecer na tela...')
        image_path = IMAGE_PATH.get(image_alias)

        if not image_path:
            log.error(f"Imagem '{image_alias}' não encontrada no IMAGE_PATH.")
            return False

        while True:
            try:
                if ScreenImage.click_element_on_screen(image_path):  # Chamado diretamente da classe
                    log.info(f'✅ {description} encontrado e clicado.')
                    time.sleep(2)
                    return True
            except:
                time.sleep(0.5)
                
    @staticmethod
    def wait_and_Doubleclick(image_alias, description):
        """ Aguarda até que o elemento apareça na tela e clica nele """
        log.info(f'⌛ Aguardando {description} aparecer na tela...')
        image_path = IMAGE_PATH.get(image_alias)

        if not image_path:
            log.error(f"Imagem '{image_alias}' não encontrada no IMAGE_PATH.")
            return False

        while True:
            try:
                if ScreenImage.click_element_on_screen(image_path):  # Chamado diretamente da classe
                    pya.click()
                    log.info(f'✅ {description} encontrado e clicado.')
                    time.sleep(2)
                    return True
            except:
                time.sleep(0.5)
                
                
    @staticmethod
    def find_img(image_alias, description, click_type, timeout=8):
        """ Aguarda até que o elemento apareça na tela e clica nele """
        log.info(f'⌛ Aguardando {description} aparecer na tela (Tempo limite: {timeout}s)...')
        image_path = IMAGE_PATH.get(image_alias)
        start_time = time.time()

        if not image_path:
            log.error(f"Imagem '{image_alias}' não encontrada no IMAGE_PATH.")
            return False

        while True:
            try:
                if ScreenImage.click_element_on_screen(image_path):  # Chamado diretamente da classe
                    if click_type == 'right':
                        pya.click(button='right')
                    elif click_type == 'double':
                        pya.doubleClick()
                    elif click_type == 'click':
                        pya.click()
                    elif click_type == '':
                        log.info('Não precisa de click')
                    log.info(f'✅ {description} encontrado e clicado.')
                    time.sleep(2)
                    return True
            except:
                log.warning(f'🚨 {description} não encontrado... Tentando novamente.')
                time.sleep(0.5)
            if time.time() - start_time > timeout:
                log.error(f'⏳ Tempo limite ({timeout}s) atingido! {description} não encontrado.')
                return False
                
 
  
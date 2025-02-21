from api.src.utils.functions.dataframe import DataFrameUtils
from api.src.utils.logs.index import log
import flet as ft
import tkinter as tk
from tkinter import filedialog

def create_app(file_path):
    if not file_path:
        log.error("Nenhum arquivo foi selecionado!")
        return
    log.success("Automaçao Iniciando...")  # Corrigido "sucess" para "success"
    DataFrameUtils.execute_data_frame(file_path)

def main(page: ft.Page):
    page.title = "Avulsos RJ E CE"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf"
    }

    file_path = ft.Ref[ft.Text]()  # Criando uma referência para armazenar o caminho do arquivo

    def select_file(e):
        root = tk.Tk()
        root.withdraw()
        file_selected = filedialog.askopenfilename(
            title="Selecione um arquivo Excel",
            filetypes=[("Excel Files", "*.xlsx;*.xls;*.csv"), ("All Files", "*.*")]
        )

        if file_selected:
            file_path.current.value = f"📂 Arquivo Selecionado: {file_selected}"
        else:
            file_path.current.value = "⚠ Nenhum arquivo selecionado!"

        page.update()

    def execute_script(e):
        if not file_path.current or not file_path.current.value or "Nenhum arquivo selecionado" in file_path.current.value:
            open_dlg(e)  # Mostra o alerta corretamente
        else:
            create_app(file_path.current.value.replace("📂 Arquivo Selecionado: ", ""))

    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    # Definição do diálogo modal corretamente
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Atenção"),
        content=ft.Text("Nenhum arquivo foi selecionado!"),
        actions=[
            ft.TextButton("OK", on_click=close_dlg)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_dlg(e):
        page.dialog = dlg_modal  # Adiciona explicitamente o modal à página
        dlg_modal.open = True
        page.update()

    def home_page():
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.ATTACH_EMAIL_OUTLINED, size=50),
                    ft.Text("AVULSOS RJ E CE", size=40, font_family="Kanit", weight=ft.FontWeight.BOLD)
                ], ft.MainAxisAlignment.CENTER),
                
            ],ft.MainAxisAlignment.CENTER),
            padding=20
        )

    # Adicionando os elementos à página
    page.add(home_page())
    page.add(ft.ElevatedButton(text="Escolher Arquivo", on_click=select_file, width=250))
    page.add(ft.Text(ref=file_path, value="⚠ Nenhum arquivo selecionado!", size=18, italic=True, color="red"))
    page.add(ft.ElevatedButton(text="Executar", on_click=execute_script, width=250))
    
    # Garante que o modal está na página antes de ser chamado
    page.dialog = dlg_modal 

    page.update()

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)


# # Executar a função
# file_path = "avulso.xlsx"
# DataFrameUtils.execute_data_frame(file_path)



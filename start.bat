@echo off
REM Definir o diretório do projeto
cd "%USERPROFILE%\Desktop\automation-avulsos-rj-ce"

REM Ativar o ambiente virtual
call .venv\Scripts\activate

REM Executar o script Python
python app.py

REM Pausar a janela para visualizar mensagens
pause
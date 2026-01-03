import uvicorn
from main import app # Importa sua API do arquivo main.py
import os
import sys

if __name__ == "__main__":
    # Garante que o executável encontre os arquivos na mesma pasta dele
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    
    # Inicia o servidor (ajuste a porta se necessário)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
    # Para desenvolvimento local, você pode usar:
    # Garanta qua a APIs no servidor estão atrás de um proxy (ex. nginx).
    #uvicorn.run("main:app", host="127.0.0.1", port=8000)
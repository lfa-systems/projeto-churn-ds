#!/bin/bash

APP_NAME="run_server"
ENTRY_POINT="run_server.py"

mostrar_ajuda() {
    echo "Uso: ./compilar.sh [OPÇÃO]"
    echo ""
    echo "Opções:"
    echo "  --run          Executa em modo dev (com reload)."
    echo "  --build        Compila o executável (terminal visível)."
    echo "  --build-hide   Compila o executável (modo noconsole)."
    echo "  --start        Inicia o binário em SEGUNDO PLANO (Background)."
    echo "  --stop         Para o servidor que está em background."
    echo "  --status       Verifica se o servidor está rodando."
    echo "  --help         Mostra esta ajuda."
    exit 0
}

copiar_arquivos() {
    cp .env usuarios.json dist/ 2>/dev/null
    cp model_churn.pkl scaler.pkl model_columns.pkl dist/ 2>/dev/null
    cp main.py dist/ 2>/dev/null
    cp df_final.csv dist/ 2>/dev/null
}

# --- LOGICA DE EXECUÇÃO ---

case "$1" in
    --run)
        echo "[DEV] Iniciando com Uvicorn..."
        uvicorn main:app --reload
        ;;
    --build)
        # Recompile usando o "python -m" (isso garante o uso do seu .venv)
        python -m PyInstaller --clean --onefile \
            --hidden-import=uvicorn.logging \
            --hidden-import=sklearn \
            --hidden-import=sklearn.utils._cython_blas \
            --hidden-import=sklearn.neighbors.typedefs \
            run_server.py

        # Copia os arquivos necessários para a pasta dist
        copiar_arquivos
        echo "[OK] Compilação concluída e arquivos copiados para dist/"
        ;;
    --build-hide)

        # Recompile usando o "python -m" (isso garante o uso do seu .venv)
        python -m PyInstaller --clean --onefile --noconsole\
            --hidden-import=uvicorn.logging \
            --hidden-import=sklearn \
            --hidden-import=sklearn.utils._cython_blas \
            --hidden-import=sklearn.neighbors.typedefs \
            run_server.py
        
        # Copia os arquivos necessários para a pasta dist
        copiar_arquivos
        echo "[OK] Compilação concluída e arquivos copiados para dist/"
        ;;

    --start)
        if [ ! -f "dist/$APP_NAME" ]; then
            echo "[ERRO] Executável não encontrado em dist/. Compile primeiro."
            exit 1
        fi
        # O segredo do background real no Linux:
        nohup ./dist/$APP_NAME > /dev/null 2>&1 &
        echo "[OK] Servidor iniciado em background. PID: $!"
        ;;
    --stop)
        PID=$(pgrep -f $APP_NAME)
        if [ -z "$PID" ]; then
            echo "[AVISO] Nenhum servidor encontrado rodando."
        else
            kill $PID
            echo "[OK] Servidor (PID $PID) encerrado."
        fi
        ;;
    --status)
        PID=$(pgrep -f $APP_NAME)
        if [ -z "$PID" ]; then
            echo "[-] Servidor está PARADO."
        else
            echo "[+] Servidor está RODANDO (PID: $PID)."
        fi
        ;;
    *)
        mostrar_ajuda
        ;;
esac
import os # Permite que Python "converse" com o sistema operacional
import json # Permite troca de dados na entre sistemas
import logging # Grava as ações da aplicação no arquivo
import random # Gera números aleatórios
from datetime import datetime # Acessar o relógio do sistema operacional
from dotenv import load_dotenv # Importa o carregador de arquivo .env e injetar as variáveis
from fastapi import FastAPI, Request, Depends, HTTPException, status # Criar APIs
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # Implementação de padrões de segurança
from fastapi.middleware.cors import CORSMiddleware

import signal # Para shutdown
from pydantic import BaseModel # Definir quais campos o Python deve esperar e validar no JSON recebido.

# 1. Carrega as variáveis do arquivo .env para o sistema
load_dotenv()

# 2. Captura as variáveis usando os nomes definidos no .env
APP_TITLE = os.getenv("APP_TITLE")
USERS_FILE = os.getenv("USERS_JSON_PATH")
LOG_FILE = os.getenv("LOG_FILE_PATH")

# Configuração de Log usando a variável do .env
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(message)s'
)

app = FastAPI(title=APP_TITLE) # Criando o "servidor" que vai ouvir as requisições na internet.

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Em produção, substitua pelo domínio do seu frontend
    allow_credentials=True,
    allow_methods=["*"],      # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],      # Permite todos os headers
)

security = HTTPBearer()

# Estrutura dos dados que você vai receber
class ClienteSchema(BaseModel):
    tempoContratoMeses: int
    atrasosDePagamento: int
    usoMensal: float
    plano: str

# --- FUNÇÃO DE CARREGAMENTO USANDO VARIÁVEL DE AMBIENTE ---
def carregar_usuarios():
    try:
        # Usamos a variável USERS_FILE que veio do .env
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Erro: Arquivo {USERS_FILE} não encontrado!")
        return {}

# --- SEGURANÇA E AUDITORIA (Mantendo a lógica anterior) ---
async def get_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    usuarios = carregar_usuarios()
    token_enviado = credentials.credentials
    
    if token_enviado in usuarios:
        nome_usuario = usuarios[token_enviado]
        request.state.user_name = nome_usuario
        return nome_usuario
    else:
        request.state.user_name = "ANÔNIMO/INVÁLIDO"
        raise HTTPException(status_code=401, detail="Token inválido")

@app.middleware("http")
async def audit_log_middleware(request: Request, call_next):
    # (A lógica do middleware permanece a mesma, usando LOG_FILE já configurado)
    response = await call_next(request)
    user_name = getattr(request.state, "user_name", "DESCONHECIDO")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client_host = request.client.host

    log_line = f"[{timestamp}] | {client_host}: {user_name.ljust(20)} | Ação: {request.method} {request.url.path} | Status: {response.status_code}"
    logging.info(log_line)
    return response

@app.post("/predict")
async def predict(dados: ClienteSchema, user: str = Depends(get_current_user)):
    prob = round(random.uniform(0, 1), 2)
    res = "Vai cancelar" if prob > 0.5 else "Não vai cancelar"
    return {"previsao": res, "probabilidade": prob, "cliente_recebido": dados}

@app.get("/shutdown", dependencies=[Depends(get_current_user)])
async def shutdown(user: str = Depends(get_current_user)):
    """
    Endpoint para desligar o servidor remotamente.
    Apenas usuários autenticados com token podem fazer isso.
    """
    # Verifica se o usuário é um admin (exemplo de lógica extra)
    if user != "Luciano": # Ou outro critério de admin que você tenha
        raise HTTPException(status_code=403, detail="Sem permissão para desligar")

    print(f"Desligamento solicitado por {user}")
    
    # Envia um sinal para o próprio processo se encerrar
    os.kill(os.getpid(), signal.SIGTERM)
    return {"message": "Servidor encerrando..."}
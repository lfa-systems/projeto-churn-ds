# 📊 Previsão de Churn - Projeto Churn Insight

Este projeto utiliza técnicas de **Machine Learning** para identificar clientes com alta probabilidade de cancelar serviços (Churn). O modelo foi treinado com base de dados no dataset [*Telco Customer Churn*](https://www.kaggle.com/datasets/mdshoaibaktar/customer-churn-prediction-dataset?resource=download) e disponibilizado através de uma API.

## 📂 Estrutura do Repositório

* **`./projeto-churn-ds/`**: Diretório principal.
    * **`churn-api-ds/`**: Contém o código-fonte da API, modelos treinados, scripts de compilação.
    * **`Dados/`**: Base de dados original em CSV utilizada para o treinamento.
    * **`Hackathon_ONE_8.ipynb`**: Notebook Jupyter com a análise exploratória, tratamento de dados, treinamento e criação do modelo.

## 🧠 O Modelo

### 🤖 Ciclo de Vida do Modelo

1. **Treinamento (Colab):** O arquivo `projeto_churn.ipynb` processa os dados, trata o desbalanceamento com `class_weight='balanced'` e exporta a inteligência do sistema.
2. **Exportação:** Ao final do treino, são gerados 3 arquivos:
   - `model_churn.pkl` (O modelo)
   - `scaler.pkl` (A régua de normalização)
   - `model_columns.pkl` (A ordem oficial das colunas)
3. **Produção (API):** Estes arquivos devem ser colocados na pasta `churn-api-ds` para que o servidor local possa realizar as predições com os mesmos parâmetros do treinamento.


O modelo utiliza **Regressão Logística** com ajuste de `class_weight='balanced'` para lidar com o desequilíbrio das classes. 
#### `class_weight='balanced'` Diz para o modelo
    "Como o dataset tem muito mais gente que FICOU do que gente que SAIU, o modelo
    tende a ficar 'viciado/preguiçoso' em dizer que todo mundo fica (afinal, assim
    ele acerta quase sempre).

    O balanced chega e dá um sacode: 'Ei, não me venha com o caminho mais fácil!
    Acertar quem sai vale 10 pontos, e acertar quem fica vale só 1.
    Agora vira esse jogo!'"

### Métricas Alcançadas:
* **Recall (Classe 1):** ~80% ( Foco em não deixar nenhum cliente em risco escapar ).
* **Acurácia:** Equilibrada para evitar falsos negativos.

### 📈 Performance do Modelo

O modelo foi avaliado utilizando um conjunto de teste independente ( 20% dos dados ). Abaixo estão as métricas detalhadas:

    === Relatório de Performance ===

      Classe  precision    recall  f1-score   support

           0       0.90      0.71      0.80      1033
           1       0.50      0.79      0.61       374

    accuracy                           0.73      1407


### Entedendo o relatório
### 1. O Ponto de Partida: O "Support"
O relatório diz que foram testados 1.407 clientes:

    Classe 0 ( Ficaram ): 1.033 clientes.
    Classe 1 ( Saíram  ):   374 clientes.

### 2. Calculando os Acertos ( Verdadeiros Positivos e Negativos )
Para descobrir os acertos, multiplicamos o Recall pelo Support:

* **Acerto de quem FICA ( Verdadeiro Negativo ):** O Recall da classe 0 é 0.71. logo $1.033 \times 0.71 = \mathbf{733}$ clientes.
* **Acerto de quem SAI ( Verdadeiro Positivo ):** O Recall da classe 1 é 0.79. logo $374 \times 0.79 = \mathbf{296}$ clientes (arredondado).

### 3. Calculando os Erros ( Falsos Positivos e Negativos )

Agora, basta subtrair os acertos do total de cada grupo:

* **Falso Alarme ( Falso Positivo ):** Eram 1.033 que ficaram, mas o modelo acertou 733. Ou seja $1.033 - 733 = \mathbf{300}$ clientes (O modelo disse que iam sair, mas eles ficaram).
* **Falha de Detecção ( Falso Negativo ):** Eram 374 que saíram, mas o modelo acertou 296. Ou seja $374 - 296 = \mathbf{78}$ clientes (Eles saíram e o modelo não percebeu).

💡 Por que esses números importam para o Negócio?

Ao configurar o modelo, priorizamos o Recall em detrimento da Precisão na classe 1.

### O raciocínio é simples:

Custo do Falso Positivo ( Baixa Precisão na classe 1 ): O custo de oferecer um desconto ou ligar para um cliente que não ia sair é baixo.

Custo do Falso Negativo ( Baixo Recall na classe 1 ): O custo de perder um cliente para a concorrência porque o modelo não o detectou é altíssimo ( perda de receita recorrente ).

Com um Recall de 79%, o "Robozinho Detetive" atua como uma rede de proteção eficaz para o faturamento da empresa.


### 🏆 O quão bom é o nosso "Robozinho Detetive"?
Traduzindo os números para o dia a dia da empresa, veja o que o modelo entrega:

🎯 Olhar de Águia para o Risco ( Recall: 79% ): De cada 10 clientes que estão pensando em nos deixar, o modelo consegue "pescar" 8 deles antes de eles irem embora. Isso dá tempo para o time de marketing agir e salvar o contrato!

✅ Certeza de quem está satisfeito ( Precisão: 90% ): Quando o robô diz "esse cliente está feliz e vai ficar", ele acerta 9 em cada 10 vezes. Isso evita gastos desnecessários com promoções para quem já é fiel.

⚖️ Equilíbrio Realista ( Acurácia: 73% ): O modelo não tenta "adivinhar" por sorte. Ele mantém um pé no chão, focando no que realmente importa: não deixar o lucro sair pela porta.

🚀 Por que isso é dinheiro no bolso?
Em vez de disparar descontos para todo mundo, agora a empresa pode ser cirúrgica:

Economia: Não damos bônus para quem já ia ficar ( 90% de acerto aqui! ).

Retenção: Agimos nos 80% de clientes em risco que antes eram "invisíveis".

Estratégia: O modelo foca no prejuízo que dói mais: o cliente que vai embora sem a gente perceber.

---
## 🛠️ Como usar

### Faça um `Fork` do Projeto
Antes de começar, clique no botão Fork (no canto superior direito desta página) para criar uma cópia deste repositório na sua conta do GitHub. Isso permite que você salve suas alterações e modelos.

### Opção 1: O Jeito Rápido (Link Direto)
O Google Colab possui uma integração nativa que permite abrir qualquer arquivo .ipynb do GitHub apenas alterando a URL.

1. Vá até o seu repositório no GitHub.
2. Abra o arquivo .ipynb.
3. Na barra de endereços do navegador, substitua `github.com` por `colab.research.google.com/github`.
4. Dê Enter e o arquivo abrirá magicamente no Colab.

### Opção 2: Dentro do Google Colab (Manual)
Com o Colab aberto, ele deve seguir estes cliques:

1. Acesse [colab.research.google.com](https://colab.research.google.com/).
2. Na janela que abrir (ou em Arquivo > Abrir notebook), clique na aba GitHub.
3. No campo de busca, cole a URL do repositório ou o seu nome de usuário.
4. Pressione a tecla Enter (ou clique na lupa).
5. O Colab listará todos os notebooks do seu projeto. Basta clicar no arquivo desejado para abrir.

----

## 🛠️ Como Executar

### 1. Análise e Treinamento

   Se deseja ver como o "cérebro" foi treinado:

   1. Abra o arquivo `Hackathon_ONE_8.ipynb` no Google Colab ou Jupyter Notebook.
   2. Certifique-se de que o arquivo `WA_Fn-UseC_-Telco-Customer-Churn.csv` está na pasta /Dados.
   3. Execute as células para gerar os arquivos `.pkl` (modelo e scaler).
   
### 2. Rodando a API (Servidor de Predição)

Se deseja colocar o modelo para trabalhar:

    Bash#
    
    # Entre na pasta da API
    cd projeto-churn-ds/churn-api-ds

    # Execute o servidor
    python run_server.py

Acesse http://localhost:8000 para abrir a interface de cadastro e testar novos clientes.

## Autenticação
Observsar os usuarios / token no arquivo `/chrun-api-ds/usuarios.json` para enviar no cabeçalho da requisição.

## O BODY da requisição para CHURN-API-DS:
### [Ver Dicionario de dados](https://github.com/lfa-systems/projeto-churn-ds/tree/main/Dados)

    {
        "tenure": 60,
        "MonthlyCharges": 25.00,
        "TotalCharges": 108.80,
        "gender_Male": 1,
        "Partner_Yes": 0,
        "Dependents_Yes": 0,
        "PhoneService_Yes": 1,
        "MultipleLines_Yes": 0,
        "InternetService_Fiber_optic": 0,
        "InternetService_No": 0,
        "OnlineSecurity_Yes": 1,
        "OnlineBackup_Yes": 0,
        "DeviceProtection_Yes": 0,
        "TechSupport_Yes": 0,
        "StreamingTV_Yes": 0,
        "StreamingMovies_Yes": 0,
        "Contract_One_year": 0,
        "Contract_Two_year": 1,
        "PaperlessBilling_Yes": 1,
        "PaymentMethod_Credit_card_automatic": 0,
        "PaymentMethod_Electronic_check": 1,
        "PaymentMethod_Mailed_check": 0
    }

## 📊 Matriz de Resultados (O que os números dizem)

Para quem prefere ver o "placar" do jogo, aqui está como o modelo se comportou com os 1.407 clientes de teste:

    Realidade\Previsão  Previu FICA           Previu: SAI
    Cliente FICOU       733 (Acerto)          300 (Alarme Falso)
    Cliente SAIU        78 (Não detectado)    296 (Acerto Crítico)

Nota: Perceba que o modelo prefere dar um "Alarme Falso" (300) do que deixar um cliente sair sem aviso (apenas 78). 

---
## 📜 Informações do Documento

| Campo | Detalhe |
| :--- | :--- |
| **Autor Principal** | Luciano Azevedo |
| **Data da Criação** | 26 de Dezembro de 2025 |
| **Última Atualização** | 26 de Dezembro de 2025 |
| **Versão** | 1.0 |
# 📊 Previsão de Churn - Projeto Churn Insight

Este projeto utiliza técnicas de **Machine Learning** para identificar clientes com alta probabilidade de cancelar serviços (Churn). O modelo foi treinado com base de dados no dataset *Telco Customer Churn* e disponibilizado através de uma API.

## 📂 Estrutura do Repositório

* **`./Projeto/`**: Diretório principal.
    * **`churn-api-ds/`**: Contém o código-fonte da API, scripts de compilação e executáveis.
    * **`Dados/`**: Base de dados original em CSV utilizada para o treinamento.
    * **`Hackathon_ONE_8.ipynb`**: Notebook Jupyter com a análise exploratória, tratamento de dados e treinamento do modelo.

## 🧠 O Modelo
O modelo utiliza **Regressão Logística** com ajuste de `class_weight='balanced'` para lidar com o desequilíbrio das classes. 

### Métricas Alcançadas:
* **Recall (Classe 1):** ~80% (Foco em não deixar nenhum cliente em risco escapar).
* **Acurácia:** Equilibrada para evitar falsos negativos.

## 📈 Performance do Modelo
O modelo foi avaliado utilizando um conjunto de teste independente (20% dos dados). Abaixo estão as métricas detalhadas:
---
=== Relatório de Performance ===

      Classe  precision    recall  f1-score   support

           0       0.90      0.71      0.80      1033
           1       0.50      0.79      0.61       374

    accuracy                           0.73      1407

---
# Entedendo o relaótio
### 1. O Ponto de Partida: O "Support"
O relatório diz que foram testados 1.407 clientes:

* **Classe 0 (Ficaram):** 1.033 clientes.
* **Classe 1 (Saíram):**    374 clientes.

### 2. Calculando os Acertos (Verdadeiros Positivos e Negativos)
Para descobrir os acertos, multiplicamos o Recall pelo Support:

* **Acerto de quem FICA (Verdadeiro Negativo):** O Recall da classe 0 é 0.71. logo $1.033 \times 0.71 = \mathbf{733}$ clientes.
* **Acerto de quem SAI (Verdadeiro Positivo):** O Recall da classe 1 é 0.79. logo $374 \times 0.79 = \mathbf{296}$ clientes (arredondado).

### 3. Calculando os Erros (Falsos Positivos e Negativos)

Agora, basta subtrair os acertos do total de cada grupo:

* **Falso Alarme (Falso Positivo):** Eram 1.033 que ficaram, mas o modelo acertou 733.$1.033 - 733 = \mathbf{300}$ clientes (O modelo disse que iam sair, mas eles ficaram).
* **Falha de Detecção (Falso Negativo):** Eram 374 que saíram, mas o modelo acertou 296.$374 - 296 = \mathbf{78}$ clientes (Eles saíram e o modelo não percebeu).
---
💡 Por que esses números importam para o Negócio?
Ao configurar o modelo, priorizamos o Recall em detrimento da Precisão na classe 1.

O raciocínio é simples:

Custo do Falso Positivo (Baixa Precisão na classe 1): O custo de oferecer um desconto ou ligar para um cliente que não ia sair é baixo.

Custo do Falso Negativo (Baixo Recall na classe 1): O custo de perder um cliente para a concorrência porque o modelo não o detectou é altíssimo (perda de receita recorrente).

Com um Recall de 79%, o "Robozinho Detetive" atua como uma rede de proteção eficaz para o faturamento da empresa.
---

## 🏆 O quão bom é o nosso "Robozinho Detetive"?
Traduzindo os números para o dia a dia da empresa, veja o que o modelo entrega:

🎯 Olhar de Águia para o Risco (Recall: 79%): De cada 10 clientes que estão pensando em nos deixar, o modelo consegue "pescar" 8 deles antes de eles irem embora. Isso dá tempo para o time de marketing agir e salvar o contrato!

✅ Certeza de quem está satisfeito (Precisão: 90%): Quando o robô diz "esse cliente está feliz e vai ficar", ele acerta 9 em cada 10 vezes. Isso evita gastos desnecessários com promoções para quem já é fiel.

⚖️ Equilíbrio Realista (Acurácia: 73%): O modelo não tenta "adivinhar" por sorte. Ele mantém um pé no chão, focando no que realmente importa: não deixar o lucro sair pela porta.

🚀 Por que isso é dinheiro no bolso?
Em vez de disparar descontos para todo mundo, agora a empresa pode ser cirúrgica:

Economia: Não damos bônus para quem já ia ficar (90% de acerto aqui!).

Retenção: Agimos nos 80% de clientes em risco que antes eram "invisíveis".

Estratégia: O modelo foca no prejuízo que dói mais: o cliente que vai embora sem a gente perceber.

## 🛠️ Como usar
Para entender o treinamento, abra o arquivo `.ipynb`. Para rodar o sistema de predição em tempo real, acesse a pasta `churn-api-ds`.


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
    cd Projeto/churn-api-ds

    # Execute o servidor
    python run_server.py

Acesse http://localhost:8000 para abrir a interface de cadastro e testar novos clientes.

📊 Matriz de Resultados (O que os números dizem)Para quem prefere ver o "placar" do jogo, aqui está como o modelo se comportou com os 1.407 clientes de teste:Realidade \ PrevisãoPreviu: FICAPreviu: SAICliente FICOU733 (Acerto)300 (Alarme Falso)Cliente SAIU78 (Não detectado)296 (Acerto Crítico)Nota: Perceba que o modelo prefere dar um "Alarme Falso" (300) do que deixar um cliente sair sem aviso (apenas 78). Essa é a nossa estratégia de Recall de 79% em ação!🏗️ Dica para o diretório churn-api-dsComo você tem uma pasta build e arquivos .spec, o seu README de lá já menciona o executável. Isso é ótimo! Mostra que o projeto está pronto para sair da máquina do desenvolvedor e ir para um servidor real.O seu projeto está completíssimo agora! Ele tem:Dados reais filtrados.Modelo inteligente com foco em negócio (Recall).API robusta com tratamentos de erros (try/except).Documentação profissional (READMEs).
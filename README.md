# Análise de Dados Ambientais do Pantanal

Aplicação interativa para leitura, tratamento e visualização de dados 
ambientais em séries temporais. O usuário pode carregar um arquivo CSV 
próprio ou explorar o conjunto de dados de exemplo incluído.

---

## Funcionalidades

- Upload de arquivo CSV com validação automática de colunas
- Diagnóstico de dados faltantes por variável
- Tratamento por interpolação linear (adequado para séries temporais contínuas)
- Cálculo de estatísticas descritivas (média por variável)
- Visualização interativa da evolução temporal de temperatura, nível do rio e NDVI

---

## Formato esperado do CSV

| Coluna         | Tipo     | Descrição                                      |
|----------------|----------|------------------------------------------------|
| data           | datetime | Data da observação                             |
| temperatura_c  | float    | Temperatura em graus Celsius                   |
| nivel_rio_m    | float    | Nível do rio em metros                         |
| ndvi           | float    | Índice de Vegetação por Diferença Normalizada  |

---

## Como executar

**Pré-requisitos:** Python 3.8+

```bash
$ git clone https://github.com/RebecaLameira/inpp-pantanal.git
$ cd inpp-pantanal
$ pip install -r requirements.txt
$ streamlit run app.py
```

Acesse em: `http://localhost:8501`

---

## Estrutura do projeto

```
├── app.py               # Aplicação principal
├── dados_pantanal.csv   # Dataset de exemplo
├── requirements.txt     # Dependências
└── README.md
```

## Decisões técnicas

**Streamlit** — escolhido por ser a opção mais direta para quem trabalha com dados em Python e precisa de uma interface funcional sem abrir mão do tempo de análise. Em vez de construir um frontend separado, o foco ficou no que importa: explorar, tratar e visualizar os dados.

**Interpolação linear** —  adotada para preencher os valores ausentes porque faz sentido para o tipo de dado aqui: séries temporais ambientais variam de forma gradual, então estimar um valor entre dois pontos conhecidos é mais honesto do que substituir pela média geral, que ignoraria completamente a tendência ao longo do tempo.

**Plotly** — escolhido porque gráficos estáticos não são suficientes para análise exploratória. Poder passar o mouse sobre um ponto e ver a data e o valor exato faz diferença na hora de identificar variações relevantes na série, como um pico de temperatura ou uma queda no nível do rio.

---

## Possíveis evoluções

- Detecção automática de anomalias na série temporal
- Exportação dos dados tratados em CSV
- Integração com APIs de dados ambientais em tempo real
- Análise de correlação entre variáveis (temperatura × NDVI × nível do rio)

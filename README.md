Sistema Inteligente de Triagem Laboratorial

Sistema web desenvolvido em Python + Flask para gerenciar filas de atendimento em laboratórios, utilizando regras de prioridade, histórico de atendimentos e Inteligência Artificial para análise operacional.

🚀 Funcionalidades

📋 Cadastro de pacientes na fila de triagem

⚡ Priorização automática (Emergência, Prioritário e Normal)

⏱️ Aging: promoção automática por tempo de espera

🧠 Módulo de Inteligência Artificial para análise gerencial

📊 Dashboard com métricas de atendimento

🗂️ Histórico completo de atendimentos

🖨️ Geração de ficha final do paciente

🧩 Arquitetura do Projeto
📁 projeto/
├── app.py               # Backend Flask (Integração geral)
├── core.py              # Lógica central da fila e prioridades
├── dados.py             # Histórico e métricas
├── inteligencia.py      # Análise com IA (Google Gemini)
├── templates/           # Arquivos HTML
├── static/              # CSS e assets
└── README.md            # Documentação

👥 Organização do Grupo
Responsável	Função	Descrição
Pessoa 1	Backend Web	Integração Flask (app.py)
Pessoa 2	Frontend	HTML e CSS
Pessoa 3	Core Logic	Regras da fila e prioridades
Pessoa 4	Data Handler	Histórico e métricas
Módulo IA	Inteligência Artificial	Análise operacional
🧠 Inteligência Artificial

O sistema utiliza Google Gemini para analisar métricas como:

Média de espera

Horário de pico

Volume de atendimentos

A IA retorna:

Status operacional (Estável / Alerta / Crítico)

Estimativa de tempo

Análise de fluxo

Sugestão de ação imediata

🛠️ Tecnologias Utilizadas

Python 3

Flask

HTML5 / CSS3

Google Gemini API

Programação Orientada a Objetos

Regra de Aging

Pacientes do tipo Normal que ultrapassam 15 minutos de espera são automaticamente promovidos na fila, garantindo mais justiça no atendimento.

📊 Métricas Geradas

Média de tempo de espera

Horário de maior fluxo (hora pico)

Total de atendimentos realizados

📌 Status do Projeto

🚧 Projeto acadêmico — versão funcional para simulação de ambiente laboratorial.

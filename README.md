# 💊 Sistema Web para a Farmácia Escola da UFVJM

[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)]()
[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![Django](https://img.shields.io/badge/Django-5.1-green)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey)]()

Este projeto tem como objetivo o desenvolvimento de uma solução web para auxiliar na organização, atendimento e gestão clínica da Farmácia Escola da Universidade Federal dos Vales do Jequitinhonha e Mucuri (UFVJM).

---

## 🚀 Funcionalidades

- Cadastro completo de pacientes com histórico clínico e social
- Registro e acompanhamento de consultas
- Gestão de problemas de saúde e medicamentos
- Avaliação de RNMs (Resultados Negativos associados a Medicamentos)
- Plano de atuação farmacêutica
- Relatórios dinâmicos e gráficos interativos com uso de Chart.js
- Dashboard com indicadores de atenção farmacêutica

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python + Django
- **Frontend:** HTML5, CSS3, JavaScript
- **Banco de Dados:** SQLite3 (atualmente) | PostgreSQL (planejado)
- **Visualização de Dados:** Chart.js
- **Hospedagem (planejada):** Docker + PythonAnywhere / Fly.io

---

## 🏁 Como Rodar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/EnicarlosJr/TCC.git
   cd TCC
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv env
   source env/bin/activate    # Linux/macOS
   .\env\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Aplique as migrações:
   ```bash
   python manage.py migrate
   ```

5. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

---

## 🧪 Testes

> *Em desenvolvimento*  
Os testes serão adicionados utilizando **pytest** e **Django TestCase**.

---

## 🧠 Autor

**Enicarlos Pereira Gonçalves Júnior**  
Aluno de Sistemas de Informação - UFVJM  

- [LinkedIn](#)
- [GitHub: @EnicarlosJr](https://github.com/EnicarlosJr)

---

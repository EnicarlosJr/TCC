# 💊 Sistema Web para a Farmácia Escola da UFVJM

Este projeto tem como objetivo o desenvolvimento de uma solução web para auxiliar na organização, atendimento e gestão clínica da Farmácia Escola da Universidade Federal dos Vales do Jequitinhonha e Mucuri (UFVJM).

## 🚀 Funcionalidades

- Cadastro completo de pacientes com histórico clínico e social
- Registro e acompanhamento de consultas
- Gestão de problemas de saúde e medicamentos
- Avaliação de RNMs (Resultados Negativos Associados a Medicamentos)
- Plano de atuação farmacêutica
- Relatórios dinâmicos e gráficos interativos com uso de Chart.js
- Dashboard com indicadores de atenção farmacêutica

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python + Django
- **Frontend:** HTML5, CSS3, JavaScript
- **Banco de Dados:** SQLite3 (em desenvolvimento) | PostgreSQL (planejado)
- **Visualização de Dados:** Chart.js
- **Hospedagem (planejada):** Docker + PythonAnywhere/Fly.io

## 🏁 Como Rodar o Projeto

1. Clone o repositório:
   ```bash
     git clone https://github.com/EnicarlosJr/TCC.git
     cd TCC
2. python -m venv env
     source env/bin/activate  # Linux/macOS
     .\env\Scripts\activate   # Windows
3. Instale as dependências:
     pip install -r requirements.txt
4. Execute as migrações:
     python manage.py migrate
5. Inicie o servidor:
     python manage.py runserver

   
🧪 Testes (em desenvolvimento)

Os testes serão adicionados com pytest e Django TestCase.
🧠 Autor

Enicarlos Pereira Gonçalves Júnior
Aluno de Sistemas de Informação - UFVJM
Contato: LinkedIn | GitHub: @EnicarlosJr



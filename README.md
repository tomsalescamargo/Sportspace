## sobre o projeto
Pasta model lida com as classes de dominio e modelos. Arquivo views.py possui funções que geram as telas do sistema.
supabase_client.py lida com as transações com o banco de dados PostgreSQL.

O arquivo main.py possui um loop que controla qual tela está sendo exibida.

# setup de ambiente virtual python pra ficar consistente pra rodar o projeto

### criar um ambiente virtual python, no diretorio do projeto
`python3 -m venv venv`

### ativar
`source venv/bin/activate`

### instalar dependencias
`pip install FreeSimpleGUI supabase python-dotenv`

### sempre que for rodar o projeto:
`source venv/bin/activate`

### ao sair:
`deactivate`



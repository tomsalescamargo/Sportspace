# SportSpace - Sistema de Gerenciamento de Quadras

Este projeto implementa um sistema de gerenciamento de quadras com uma arquitetura de duas camadas (UI e Backend).

## Estrutura do Projeto

-   **`model/`**: Contém as classes de domínio e modelos de dados (ex: `Court.py`).
-   **`views.py`**: Funções responsáveis por gerar as telas da interface do usuário (UI) utilizando FreeSimpleGUI.
-   **`supabase_client.py`**: Lida com todas as transações e comunicação com o banco de dados PostgreSQL via Supabase.
-   **`main.py`**: Contém o loop principal da aplicação que controla a navegação entre as telas.

## Configuração do Ambiente de Desenvolvimento

Para garantir a consistência do ambiente e evitar conflitos de dependências, é **altamente recomendado** utilizar um ambiente virtual Python.

### 1. Criar o Ambiente Virtual

No diretório raiz do projeto, execute o seguinte comando para criar um ambiente virtual chamado `venv`:

```bash
python3 -m venv venv
```

### 2. Ativar o Ambiente Virtual

Antes de instalar as dependências ou executar o projeto, ative o ambiente virtual:

```bash
source venv/bin/activate
```

### 3. Instalar Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install FreeSimpleGUI supabase python-dotenv
```

### 4. Executar o Projeto

Sempre que for rodar o projeto, certifique-se de ativar o ambiente virtual e então execute `main.py`:

```bash
source venv/bin/activate
python3 main.py
```

### 5. Desativar o Ambiente Virtual

Quando terminar de trabalhar no projeto, você pode desativar o ambiente virtual:

```bash
deactivate
```
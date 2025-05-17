# OS Manager Django

Este é um projeto Django para gerenciar sistemas operacionais e seus recursos. Ele utiliza o Django Rest Framework para criar APIs e inclui uma interface administrativa personalizada.

## Estrutura do Projeto

- **core/**: Contém a lógica principal do projeto, incluindo modelos, visualizações e comandos de gerenciamento personalizados.
- **customers/**: Gerencia os dados relacionados aos clientes, incluindo modelos, serializers, sinais e URLs.
- **easy_os_django/**: Configurações principais do projeto, incluindo URLs, WSGI e ASGI.
- **staticfiles/**: Arquivos estáticos usados no projeto, como CSS, JavaScript e imagens.

## Requisitos

- Python 3.12+
- Django
- Django Rest Framework
- Docker (opcional para execução com Docker Compose)

## Configuração

1. Clone o repositório:
   ```bash
   git clone https://github.com/iru-Y/os_mananger-django
   cd os_manager-django
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

4. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

## Uso

- Acesse a interface administrativa em `http://127.0.0.1:8000/admin/`.
- Utilize as APIs REST disponíveis para gerenciar os recursos do sistema operacional.

## Docker

Para executar o projeto usando Docker:

1. Construa a imagem Docker:
   ```bash
   docker-compose build
   ```

2. Inicie os contêineres:
   ```bash
   docker-compose up
   ```

3. Acesse o aplicativo em `http://127.0.0.1:8000/`.

## Licença

Este projeto é licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais informações.

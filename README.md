# API de Tarefas (To-Do List)

Minha primeira API de Tarefas desenvolvida com FastAPI e SQLite.

## Funcionalidades
- Criar tarefa
- Listar tarefas
- Atualizar tarefa
- Deletar tarefa
- Marcar tarefa como concluída

## Como executar
1. Instale as dependências:
   ```bash
   pip install fastapi uvicorn sqlalchemy
   ```
2. Inicie a API:
   ```bash
   uvicorn main:app --reload
   ```
3. Acesse a documentação interativa:
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Estrutura do projeto
- `main.py`: Código principal da API
- `tarefas.db`: Banco de dados SQLite gerado automaticamente

## Observações
Este projeto é ideal para quem está começando com APIs, FastAPI e bancos de dados relacionais.

---

Sinta-se à vontade para contribuir ou adaptar para seus estudos!

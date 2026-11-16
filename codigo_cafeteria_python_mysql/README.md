# E-commerce Cafeteria Gourmet — Aroma & Origem (Arquitetura MVC)

Projeto desenvolvido em **Python (Flask)** no back-end, **HTML5, CSS3 e JavaScript (ES6+)** no front-end e **MySQL 8.0** para persistência relacional.

## Estrutura do Projeto (Padrão MVC)
- `app.py`: Rotas e Controllers da aplicação Flask (API REST + renderização da View).
- `models.py`: Camada Model responsável pela conexão com o MySQL e regras de persistência.
- `templates/index.html`: Camada View (interface responsiva do e-commerce gourmet).
- `database_cafeteria.sql`: Projeto físico do banco de dados MySQL (DDL + dados iniciais).
- `test_app.py`: Suíte de testes automatizados com `pytest`.

## Como Executar Localmente
1. Importe o arquivo `database_cafeteria.sql` no seu servidor **MySQL** (XAMPP, Laragon ou MySQL Workbench).
2. Instale as dependências Python:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure a senha do MySQL em `models.py` (se necessário) e inicie o servidor:
   ```bash
   python app.py
   ```
4. Acesse no navegador: `http://127.0.0.1:5000`
   *(Observação: Caso o MySQL não esteja ativo no momento do teste, o sistema ativa automaticamente o modo fallback em memória para permitir testar toda a interface e checkout sem interrupções).*
5. Para rodar os testes automatizados:
   ```bash
   pytest -v
   ```

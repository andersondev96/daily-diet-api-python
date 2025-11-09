# 🥗 Daily Diet API
API RESTful completa para controle de dieta diária usando Flask. Permite registrar, editar e acompanhar as refeições diárias, incluindo informações detalhadas como nome, descrição, data/hora e se a refeição está dentro da dieta.

## 📌 **Índice**
- [📄 Sobre o Projeto](#-sobre-o-projeto)
- [🔧 Funcionalidades](#-funcionalidades)
- [🚀 Tecnologias utilizadas](#-tecnologias-utilizadas)
- [ ⚙️ Instalação e Execução](#-instalação-e-execução)
- [📄 Documentação da API](#-documentação-da-api)
- [🧪 Testes](#-testes)
- [🤝 Como contribuir](#-como-contribuir)
- [📝 Licença](#-licença)
- [👥 Autor](#-autor)


## 📄 Sobre o Projeto
O Daily Diet API tem como objetivo facilitar o controle de refeições diárias, permitindo ao usuário registrar seus hábitos alimentares e acompanhar se está mantendo a dieta planejada.

A aplicação oferece operações CRUD completas e persistência em banco de dados relacional, com endpoints documentados via Swagger.


## 🔧 Funcionalidades
- Registrar refeições informando nome, descrição, data/hora, dentro/fora da dieta.
- Editar informações das refeições.
- Excluir refeições.
- Listar todas as refeições de um usuário.
- Consultar detalhes de uma refeição específica.
- Persistência dos dados usando banco de dados relacional (MySQL, etc).

## 🚀 Tecnologias utilizadas
[![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)](https://docs.python.org/3)
[![Flask Badge](https://img.shields.io/badge/Flask-3BABC3?logo=flask&logoColor=fff&style=for-the-badge)](https://flask.palletsprojects.com/en/stable)
[![SQLAlchemy Badge](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=fff&style=for-the-badge)](https://www.sqlalchemy.org)
[![MySQL Badge](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=fff&style=for-the-badge)](https://dev.mysql.com/doc)
[![Docker Badge](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=for-the-badge)](https://docs.docker.com)
[![Pytest Badge](https://img.shields.io/badge/Pytest-0A9EDC?logo=pytest&logoColor=fff&style=for-the-badge)](https://docs.pytest.org/en/stable)
[![Swagger Badge](https://img.shields.io/badge/Swagger-85EA2D?logo=swagger&logoColor=000&style=for-the-badge)](https://swagger.io/docs)

## ⚙️ Instalação e Execução
### Pré-requisitos
- Python 3.10+
- Docker (opcional)
- MySQL (ou outro banco compatível com SQLAlchemy)

### Passos para rodar localmente
```bash
# 1. Clone o repositório
git clone https://github.com/seuusuario/daily-diet-api.git
cd daily-diet-api

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas credenciais do banco

# 5. Execute as migrações (se houver)
flask db upgrade

# 6. Inicie a aplicação
flask run --host=0.0.0.0 --port=5000

```
A API estará disponível em:
``http://localhost:5000``

## 📄 Documentação da API
#### Endpoints principais

| Método | Endpoint | Descrição |
|:------:|-----------|-----------|
| `POST` | `/users` | Cria um novo usuário |
| `POST` | `/login` | Autentica um usuário |
| `GET`  | `/logout` | Desloga um usuário |
| `GET` | `/meals` | Lista todas as refeições |
| `POST` | `/meals` | Cria uma nova refeição |
| `GET` | `/meals/<id>` | Retorna uma refeição específica |
| `PUT` | `/meals/<id>` | Atualiza uma refeição existente |
| `DELETE` | `/meals/<id>` | Remove uma refeição |

Acesse a documentação interativa (Swagger UI):

``http://localhost:5000/apidocs``

### Exemplo de requisição (POST/meals)
```json
{
  "name": "Almoço",
  "description": "Peito de frango grelhado com legumes",
  "date_time": "2025-11-06T12:30:00",
  "in_diet": true
}

```

### Exemplo de resposta
```json
{
  "id": 1,
  "name": "Almoço",
  "description": "Peito de frango grelhado com legumes",
  "date_time": "2025-11-06T12:30:00",
  "in_diet": true
}

```

Teste as requisições utilizando o [**Insomnia**](https://insomnia.rest) ou  [**Postman**](https://www.postman.com). 

[![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)](daily_dietpostman_collection.json)

## 🧪 Testes
Execute a suíte de testes com pytest:
```
pytest -v
```

Os testes cobrem as principais funcionalidades da API, garantindo estabilidade e integridade das operações CRUD.

## 🤝 Como contribuir
1. Fork este repositório

2. Crie uma branch para sua funcionalidade:
    ```sh
    git checkout -b minha-feature
    ```

3. Realize suas alterações e comite:
    ```sh
    git commit -m "feature: Minha nova funcionalidade"
    ```

4. Envie para o repositório remoto:
    ```sh
    git push origin minha-feature
    ```

5. Abra um **Pull Request**!


## 📝 Licença
Este projeto está sob a licença [LICENSE](LICENSE).

## 👥 Autor

<div style="display:flex; flex-direction:column; align-items: center;">

<a href="https://www.linkedin.com/in/anderson-fernandes96/">
<img src="https://avatars.githubusercontent.com/u/49786548?v=4" width="64" style="border: 2px solid blue; border-radius: 50px" />
</a>

**Anderson Fernandes Ferreira**

[![Instagram](https://img.shields.io/badge/-Instagram-%23E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/anderson_ff13)
[![Gmail](https://img.shields.io/badge/-Gmail-%23333?style=for-the-badge&logo=gmail&logoColor=white)](mailto:andersonfferreira96@gmail.com.br)
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/anderson-fernandes96/)

---

Feito com 💚 por **Anderson Fernandes** 👋 
[Entre em conanto](https://www.linkedin.com/in/anderson-fernandes96/)

</div>

# Estoque Loja de Açaí

![CI](https://github.com/Igor-C-Lima/Bootcamp_projeto/actions/workflows/ci.yml/badge.svg)

## 🌐 Aplicação publicada

**[https://bootcamp-projeto.onrender.com](https://bootcamp-projeto.onrender.com)**

---

## Descrição do Problema

Pequenos quiosques de açaí, geralmente administrados por uma única pessoa,
enfrentam dificuldades para gerenciar o estoque de forma eficaz. Sem um
controle adequado, é difícil saber o que precisa ser reposto e o que entra
e sai da loja. Este projeto nasceu a partir de uma necessidade real: ajudar
uma conhecida, dona de um quiosque e que trabalha sozinha, a ter mais
controle sobre seu estoque de forma simples e prática.

## Proposta da Solução

Uma aplicação web com interface visual que permite cadastrar e remover
produtos, controlar quantidades e definir um limite mínimo de estoque
para cada item. É possível consultar quais produtos precisam de reposição
e, como diferencial, consultar o clima da cidade para antecipar a demanda
por açaí em dias de calor ou frio. O foco é na simplicidade, para que
qualquer pessoa consiga usar sem dificuldades técnicas.

## Público-Alvo

Pequenos comerciantes que trabalham sozinhos ou com poucos funcionários
e enfrentam dificuldades para controlar seu estoque, muitas vezes
recorrendo a anotações em cadernos ou folhas avulsas. O sistema foi
pensado para ser simples o suficiente para qualquer pessoa usar, sem
necessidade de conhecimento técnico.

## Funcionalidades

- Cadastrar produtos no estoque
- Listar todos os produtos cadastrados
- Atualizar a quantidade de um produto
- Remover produtos do estoque
- Alertar quais produtos estão abaixo do limite mínimo e precisam de reposição
- **Consultar o clima em tempo real** via integração com a API OpenWeather,
  com dica contextual sobre a demanda esperada por açaí
- **Armazenamento em Nuvem:** Dados salvos de forma segura e persistente em um banco de dados relacional.

## Tecnologias Utilizadas

- Python 3.13
- Flask — servidor web e API REST
- Flask-CORS — suporte a requisições cross-origin
- **Supabase (PostgreSQL)** — banco de dados em nuvem (BaaS)
- Requests — consumo da API OpenWeather
- pytest — testes automatizados (unitários, integração e mocks)
- ruff — análise estática e linting
- GitHub Actions — integração contínua (CI)
- Git / GitHub — controle de versão e colaboração
- Render — hospedagem em nuvem (deploy)

---

## Integrações Externas

### API de Clima (OpenWeather)
A aplicação consome a [API OpenWeather](https://openweathermap.org/api)
para exibir as condições climáticas de qualquer cidade. Com base na
temperatura retornada, o sistema sugere se é um bom momento para reforçar
o estoque (dias quentes) ou ser mais conservador na reposição (dias frios).

### Banco de Dados (Supabase)
O sistema utiliza o **Supabase** (baseado em PostgreSQL) para garantir a persistência dos dados em nuvem, permitindo que as informações do estoque sejam acessadas de qualquer lugar com consistência e segurança.

*As chaves de API e credenciais do banco ficam armazenadas exclusivamente no servidor — elas **nunca são expostas ao navegador ou ao código-fonte**, garantindo segurança tanto no ambiente local quanto no deploy em produção.*

---

## Como Rodar Localmente

### Pré-requisitos

- Python 3.13+
- Uma chave de API gratuita do [OpenWeather](https://openweathermap.org/api)
- Um projeto criado no [Supabase](https://supabase.com/) com a tabela `produto` (colunas: nome, quantidade, limite_minimo, status)

### Instalação

```bash
# Clonar o repositório
git clone [https://github.com/Igor-C-Lima/Bootcamp_projeto.git](https://github.com/Igor-C-Lima/Bootcamp_projeto.git)
cd Bootcamp_projeto/projeto

# Instalar dependências
pip install -r requirements.txt
# Projeto avaliado para a faculdade Inteli - Robo Digital
## Objetivo
Esse repositório tem o objetivo de explicar e armazenar os códigos para uma atividade avaliada da minha faculdade, a Inteli.  
Essa atividade consiste na elaboração de um backend integrado à um ambiente virtual criado em GODOT.  
Todos os códigos está armazenados na pasta `src` .

## Backend
O backend é construido em flask, terá MySQL como banco de dados e tudo está conteinerizado. 

### Como rodar o projeto
Podemos rodar o projeto de duas maneiras:
 1. Com python nativo em seu computador 
 2. Com Docker

#### Python nativo
Rode os seguintes comandos em `/src`
```shell
pip install -r requirements.txt
```
Em windows:
```shell
pyp __init__.py
```
Em mac:
```shell
python3 __init__.py
```
Pronto, o projeto já estará rodando em localhost!

#### Docker
Rode os seguintes comando em `/src`
```shell
docker compose up
```
Pronto, o projeto já estará rodando em um container é poderá ser acessado em localhost na porta mencionada no terminal!
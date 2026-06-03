# "Mano" o MiniNano

MiniNano é um editor de texto desenvolvido em **Python** com **Tkinter**, inspirado no GNU Nano. O projeto foi criado para aplicar conceitos de **Estruturas de Dados**, utilizando listas duplamente encadeadas e pilhas em uma aplicação com interface gráfica.

## Funcionalidades

* Interface inspirada no GNU Nano
* Edição de texto em tempo real
* Abrir e salvar arquivos
* Criar novos documentos
* Undo e Redo
* Atalhos de teclado
* Arquitetura modular

## Estrutura do Projeto

```text
MiniNano/
│
├── main.py         # Interface gráfica
├── editor.py       # Lógica do editor
├── structures.py   # Estruturas de dados
└── README.md
```

## Estruturas de Dados

### Lista Duplamente Encadeada

Utilizada para armazenar e manipular o conteúdo textual de forma dinâmica.

### Pilhas (Stacks)

Responsáveis pelo histórico de ações, implementando as operações de **Undo** e **Redo**.

## Atalhos

| Atalho   | Função        |
| -------- | ------------- |
| Ctrl + N | Novo arquivo  |
| Ctrl + O | Abrir arquivo |
| Ctrl + S | Salvar        |
| Ctrl + Z | Desfazer      |
| Ctrl + Y | Refazer       |
| Ctrl + Q | Sair          |

## Execução

```bash
git clone https://github.com/seu-usuario/MiniNano.git
cd MiniNano
python main.py
```

## Tecnologias

* Python
* Tkinter
* Programação Orientada a Objetos
* Estruturas de Dados

## Objetivo

Demonstrar a aplicação prática de conceitos de Estruturas de Dados em uma aplicação real, integrando interface gráfica, manipulação de arquivos e gerenciamento de histórico de alterações.

## Autor

Projeto desenvolvido para a disciplina de **Estruturas de Dados**.

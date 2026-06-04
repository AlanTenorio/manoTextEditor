# MiniNano

## Descrição

O **MiniNano** é um editor de texto desenvolvido em **Python** utilizando a biblioteca **Tkinter** para construção da interface gráfica. O projeto foi inspirado no editor de texto GNU Nano e tem como principal objetivo demonstrar a aplicação prática de conceitos estudados na disciplina de **Estruturas de Dados**.

A aplicação integra estruturas lineares, manipulação de arquivos, programação orientada a objetos e uma interface gráfica funcional, permitindo ao usuário criar, editar, abrir e salvar documentos de texto.

---

## Funcionalidades

* Criação de novos documentos
* Abertura de arquivos existentes
* Salvamento de arquivos
* Edição de texto em tempo real
* Histórico de alterações
* Operações de Undo (Desfazer)
* Operações de Redo (Refazer)
* Atalhos de teclado
* Interface inspirada no GNU Nano
* Estrutura modular para facilitar manutenção e expansão

---

## Estrutura do Projeto

```text
MiniNano/
│
├── main.py
├── editor.py
├── structures.py
└── README.md
```

### main.py

Responsável pela interface gráfica da aplicação.

Implementa:

* Janela principal
* Área de edição de texto
* Barra de status
* Atalhos de teclado
* Integração entre a interface e a lógica do editor

### editor.py

Responsável pelas regras de negócio da aplicação.

Implementa:

* Controle do conteúdo textual
* Gerenciamento do histórico de alterações
* Operações de Undo e Redo
* Controle do arquivo atualmente aberto

### structures.py

Responsável pelas estruturas de dados utilizadas pelo projeto.

Implementa:

* Nó (Node)
* Lista Duplamente Encadeada (DoublyLinkedList)

---

## Estruturas de Dados Utilizadas

### Lista Duplamente Encadeada

A estrutura principal utilizada para armazenamento das linhas do texto é uma Lista Duplamente Encadeada.

Cada nó possui:

* Referência para o elemento anterior
* Referência para o próximo elemento
* Conteúdo textual armazenado

Essa estrutura permite inserções e remoções dinâmicas sem a necessidade de realocação de memória para todos os elementos.

### Pilhas (Stacks)

O histórico de alterações é implementado através de duas pilhas:

#### Undo Stack

Armazena os estados anteriores do documento.

Utilizada para desfazer alterações realizadas pelo usuário.

#### Redo Stack

Armazena estados removidos pela operação de Undo.

Permite restaurar alterações previamente desfeitas.

---

## Atalhos de Teclado

| Atalho   | Função             |
| -------- | ------------------ |
| Ctrl + N | Novo arquivo       |
| Ctrl + O | Abrir arquivo      |
| Ctrl + S | Salvar arquivo     |
| Ctrl + Z | Desfazer           |
| Ctrl + Y | Refazer            |
| Ctrl + Q | Encerrar aplicação |

---

## Tecnologias Utilizadas

* Python 3
* Tkinter
* Programação Orientada a Objetos (POO)
* Estruturas de Dados
* Manipulação de Arquivos

---

## Como Executar

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/MiniNano.git
```

### 2. Acessar a pasta do projeto

```bash
cd MiniNano
```

### 3. Executar a aplicação

```bash
python main.py
```

---

## Objetivos Acadêmicos

Este projeto foi desenvolvido com os seguintes objetivos:

* Aplicar conceitos de Estruturas de Dados estudados em sala de aula
* Utilizar Listas Duplamente Encadeadas em uma aplicação prática
* Implementar Pilhas para gerenciamento de histórico
* Desenvolver uma interface gráfica utilizando Tkinter
* Integrar Programação Orientada a Objetos e Estruturas de Dados em um projeto completo

---

## Possíveis Melhorias Futuras

* Numeração de linhas
* Sistema de busca de texto
* Substituição automática de palavras
* Temas personalizáveis
* Suporte a múltiplas abas
* Barra de menus
* Salvamento automático
* Destaque de sintaxe para código-fonte

---

## Autor

Projeto desenvolvido para a disciplina de **Estruturas de Dados**, com o objetivo de demonstrar a aplicação prática de listas duplamente encadeadas e pilhas em um editor de texto funcional.

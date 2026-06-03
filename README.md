# MiniNano

MiniNano é um editor de texto simples desenvolvido em Python utilizando Tkinter. O projeto foi criado com fins educacionais para demonstrar a aplicação de estruturas de dados, como listas duplamente encadeadas e pilhas, em um sistema de edição de texto com interface gráfica.

## Objetivos do Projeto

* Aplicar conceitos de Estruturas de Dados.
* Implementar uma interface gráfica funcional.
* Utilizar listas duplamente encadeadas para armazenamento do texto.
* Utilizar pilhas para operações de desfazer e refazer.
* Permitir abertura e salvamento de arquivos de texto.

## Funcionalidades

* Interface gráfica com tema escuro inspirado no Nano.
* Edição de texto em tempo real.
* Numeração de linhas.
* Abertura de arquivos (.txt e .py).
* Salvamento de arquivos.
* Criação de novos documentos.
* Barra de status com informações do cursor.
* Operações de desfazer (Undo) e refazer (Redo).
* Atalhos de teclado.

## Estrutura do Projeto

```
MiniNano/
│
├── main.py
├── editor.py
├── structures.py
└── README.md
```

### main.py

Responsável pela interface gráfica do sistema utilizando a biblioteca Tkinter.

### editor.py

Contém a lógica do editor, incluindo:

* Gerenciamento do conteúdo.
* Histórico de alterações.
* Operações de desfazer e refazer.
* Controle do arquivo atualmente aberto.

### structures.py

Implementa as estruturas de dados utilizadas pelo projeto:

* Node
* DoublyLinkedList

## Estruturas de Dados Utilizadas

### Lista Duplamente Encadeada

A lista duplamente encadeada permite armazenar os dados do texto de forma dinâmica, possibilitando inserções e remoções eficientes.

Cada nó possui:

* Referência para o próximo elemento.
* Referência para o elemento anterior.
* Conteúdo armazenado.

### Pilhas

As pilhas são utilizadas para:

* Histórico de desfazer (Undo).
* Histórico de refazer (Redo).

O funcionamento segue a política LIFO (Last In, First Out).

## Requisitos

* Python 3.10 ou superior
* Tkinter (já incluído na instalação padrão do Python)

## Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/MiniNano.git
```

2. Entre na pasta do projeto:

```bash
cd MiniNano
```

3. Execute o programa:

```bash
python main.py
```

## Atalhos de Teclado

| Atalho   | Função         |
| -------- | -------------- |
| Ctrl + S | Salvar arquivo |
| Ctrl + O | Abrir arquivo  |
| Ctrl + N | Novo arquivo   |
| Ctrl + Z | Desfazer       |
| Ctrl + Y | Refazer        |

## Tecnologias Utilizadas

* Python
* Tkinter

## Possíveis Melhorias Futuras

* Destaque de sintaxe.
* Temas personalizáveis.
* Pesquisa e substituição de texto.
* Sistema de abas.
* Contador de palavras.
* Suporte a múltiplos formatos de arquivo.
* Salvamento automático.

## Autor

Projeto desenvolvido para fins acadêmicos na disciplina de Estruturas de Dados.

# MiniNano - WordPad Style Editor

Um editor de texto acadêmico desktop inspirado no clássico editor de terminal *GNU Nano*, mas com uma interface gráfica rica em recursos no estilo *WordPad*. O projeto foi desenvolvido como um estudo prático para disciplinas de **Metodos Computacionais**.

---

## 👥Criadores
### José ALan da Silva Tenório 
### Pedro Henrique Pereira de Albuquerque 

---

## 🚀 Funcionalidades Principais

* **Paginação Estilo Word:** Divisão física e visual de páginas baseada nas dimensões proporcionais de uma folha A4, com limite dinâmico de 32 linhas por página.
* **Algoritmo de Overflow Vertical:** Transbordo automático de texto entre páginas consecutivas durante a digitação em tempo real ou colagem ($Ctrl+V$).
* **Editor Multicamadas:** Barra de ferramentas (*Ribbon*) com suporte a formatação de fontes (Negrito, Itálico, Sublinhado) e alinhamento de parágrafos.
* **Sistema de Zoom Dinâmico:** Controle de escala visual que redimensiona proporcionalmente folhas, fontes, numeração de linhas e tags de estilo de 50% a 200%.
* **Animação de Temas (Fade):** Transição suave entre Modo Escuro e Modo Claro utilizando interpolação linear matemática de cores RGB.
* **Exportação para PDF:** Motor de salvamento que exporta o documento final respeitando estritamente a divisão física das páginas visuais.

---

## 🧠 Arquitetura e Estruturas de Dados

O projeto foi construído seguindo boas práticas de separação de conceitos (Interface / Lógica de Negócios) e aplicando estruturas clássicas da ciência da computação:

### 1. Lista Duplamente Encadeada (`DoublyLinkedList`)
Utilizada no coração do backend do editor para gerenciar as linhas de texto de forma dinâmica na memória RAM.
* **Vantagem Acadêmica:** Permite a inserção de nós (linhas) com complexidade de tempo constante $O(1)$ no final da estrutura através do ponteiro de cauda (`tail`), além de permitir navegação bidirecional eficiente (`next` e `prev`).

### 2. Histórico Baseado em Pilhas (LIFO)
O sistema de **Desfazer (Undo)** e **Refazer (Redo)** foi implementado utilizando duas pilhas distintas.
* **Padrão Memento:** Salva *snapshots* do estado do texto na memória sempre que alterações relevantes são detectadas.
* **Gerenciamento de Memória:** A pilha possui um limitador estrito de 100 estados para evitar o consumo excessivo de memória (estouro de pilha/RAM).

### 3. Interface Assíncrona com Tkinter
O frontend utiliza uma hierarquia complexa de componentes (`Canvas` $\rightarrow$ `Frame` de Centralização $\rightarrow$ `Páginas Text`), onde os eventos de teclado e redimensionamento são monitorados via *Key Bindings* nativos.

---
## 🛠️ Instalação e Dependências
Para executar o MiniNano, é recomendado o uso de um ambiente virtual (.venv) para gerenciar as dependências do projeto de forma isolada. Siga as instruções abaixo de acordo com o seu sistema operacional.

**🪟 Windows:**
A biblioteca Tkinter já vem embutida na instalação padrão do Python no Windows. Sendo assim, basta criar o ambiente virtual e instalar o ReportLab.
* Criar e ativar o ambiente virtual:
```
python -m venv .venv
.\.venv\Scripts\activate
```
* Instalar a biblioteca auxiliar:
```
pip install reportlab
```
**🐧 Linux (Debian/Ubuntu):**
No Linux, o Tkinter precisa ser instalado separadamente através do gerenciador de pacotes do sistema antes de configurar o restante do ambiente.
* **Instalar o Tkinter no sistema:
```
sudo apt-get update
sudo apt-get install python3-tk
```
* Criar e ativar o ambiente virtual:
```
python3 -m venv .venv
source .venv/bin/activate
```
* Instalar a biblioteca auxiliar:
```
pip install reportlab
```

---

## 📁 Estrutura do Projeto

```text
├── main.py              # Ponto de entrada do aplicativo
├── gui.py               # Classe MiniNanoGUI (Interface Gráfica e Eventos)
├── editor.py            # Classe Editor (Backend, histórico e estado do arquivo)
├── structures.py        # Classes Node e DoublyLinkedList (Estrutura de dados)
├── pdf_exporter.py      # Módulo responsável pela conversão e exportação para PDF
└── README.md            # Documentação do projeto

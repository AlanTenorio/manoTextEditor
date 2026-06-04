"""
Módulo responsável pela implementação da estrutura de dados
utilizada pelo editor de texto.

A estrutura escolhida é uma Lista Duplamente Encadeada,
capaz de armazenar linhas de texto de forma dinâmica.

Implementação baseada nos conceitos estudados em aula sobre
listas encadeadas e estruturas lineares.
"""


class Node:
    """
    Representa um nó da lista duplamente encadeada.

    Cada nó armazena uma linha de texto e referências
    para o nó anterior e para o próximo nó da lista.
    """

    def __init__(self, data):
        """
        Inicializa um novo nó.

        Args:
            data (str):
                Conteúdo armazenado no nó.
        """

        self.data = data

        # Referência para o nó anterior.
        self.prev = None

        # Referência para o próximo nó.
        self.next = None


class DoublyLinkedList:
    """
    Implementação de uma Lista Duplamente Encadeada.

    A estrutura permite armazenar elementos de forma
    sequencial, mantendo referências tanto para o
    elemento anterior quanto para o próximo.

    No editor, essa estrutura é utilizada para armazenar
    as linhas do texto carregado.
    """

    def __init__(self):
        """
        Inicializa uma lista vazia.

        Atributos:
            head (Node | None):
                Primeiro nó da lista.

            tail (Node | None):
                Último nó da lista.

            size (int):
                Quantidade de elementos armazenados.
        """

        self.head = None
        self.tail = None
        self.size = 0

    def append(self, text):
        """
        Insere um novo elemento ao final da lista.

        Caso a lista esteja vazia, o novo nó torna-se
        simultaneamente o primeiro e o último elemento.

        Args:
            text (str):
                Conteúdo a ser armazenado.
        """

        node = Node(text)

        if not self.head:

            self.head = self.tail = node

        else:

            node.prev = self.tail

            self.tail.next = node

            self.tail = node

        self.size += 1

    def clear(self):
        """
        Remove todos os elementos da lista.

        Após a execução, a estrutura retorna ao estado
        inicial de lista vazia.
        """

        self.head = None
        self.tail = None
        self.size = 0

    def to_list(self):
        """
        Converte a lista encadeada para uma lista Python.

        Percorre todos os nós da estrutura e copia seus
        conteúdos para uma lista convencional.

        Returns:
            list:
                Lista contendo todos os elementos armazenados.
        """

        result = []

        current = self.head

        while current:

            result.append(current.data)

            current = current.next

        return result

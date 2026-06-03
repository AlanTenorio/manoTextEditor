# aqui fica a estrutura de dados, que é uma lista duplamente encadeada, para armazenar as linhas do texto
# Como mostrado em Aula, codigo copiado das listas de Pilhas e listas duplamente encadeadas.

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, text):
        node = Node(text)

        if not self.head:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

        self.size += 1

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0

    def to_list(self):
        result = []

        current = self.head

        while current:
            result.append(current.data)
            current = current.next

        return result
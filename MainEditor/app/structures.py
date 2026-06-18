"""
Módulo da estrutura de Lista Duplamente Encadeada para o editor de texto.
Garante inserção eficiente de linhas com complexidade O(1).
"""

class Node:
    """Representa um nó individual na memória, encapsulando o dado (a linha de texto) e os ponteiros."""
    def __init__(self, data):
        self.data = data  # Conteúdo utilitário do nó (neste caso, uma string representando a linha)
        self.prev = None  # Ponteiro/Referência para o nó anterior na memória (essencial para navegação bidirecional)
        self.next = None  # Ponteiro/Referência para o próximo nó na memória


class DoublyLinkedList:
    """Estrutura de dados dinâmica que gerencia a coleção de nós na memória RAM."""
    def __init__(self):
        # Sentinelas de controle: Head (início) e Tail (fim). 
        # Mantendo a referência do Tail, conseguimos inserções no final em tempo constante O(1).
        self.head = self.tail = None
        self.size = 0  # Controle interno do tamanho da lista (evita varreduras O(n) apenas para contar linhas)

    def append(self, text):
        """Inserção Dinâmica: Cria um novo nó e ajusta os ponteiros para acoplá-lo no fim da lista."""
        node = Node(text)
        
        # Caso 1: A lista está vazia (primeira linha do documento)
        if not self.head:
            self.head = self.tail = node  # O único nó passa a ser simultaneamente o início e o fim
        
        # Caso 2: A lista já possui elementos (linhas existentes)
        else:
            node.prev = self.tail  # O anterior do novo nó passa a apontar para o antigo último nó
            self.tail.next = node  # O próximo do antigo último nó é atualizado para o novo nó
            self.tail = node       # A referência de fim da lista (Tail) é movida para o novo nó
            
        self.size += 1  # Incremento do tamanho da estrutura após inserção bem-sucedida

    def clear(self):
        """
        Garante a limpeza da estrutura. Em Python, ao cortar as referências dos nós principais (Head e Tail),
        o Garbage Collector limpa automaticamente os nós intermediários da memória por falta de referência ativa.
        """
        self.head = self.tail = None
        self.size = 0

    def to_list(self):
        """Algoritmo de Travessia (Traversal): Percorre a lista sequencialmente do Head ao Tail."""
        result = []
        current = self.head  # Ponteiro temporário de navegação que inicia no primeiro nó
        
        while current:
            result.append(current.data)  # Extrai o dado útil do nó corrente
            current = current.next       # Avança o ponteiro para o próximo endereço de memória
            
        return result
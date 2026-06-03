from tkinter import filedialog
from structures import DoublyLinkedList


class Editor:
    """
    Classe responsável pelo gerenciamento do conteúdo textual do editor.

    Esta classe atua como a camada de lógica da aplicação,
    armazenando o texto através de uma lista duplamente encadeada
    e controlando o histórico de alterações por meio de pilhas
    para operações de desfazer (Undo) e refazer (Redo).
    """

    def __init__(self):
        """
        Inicializa o editor.

        Atributos:
            text_data (DoublyLinkedList):
                Estrutura responsável pelo armazenamento do texto.

            undo_stack (list):
                Pilha que mantém o histórico de estados anteriores
                para permitir operações de desfazer.

            redo_stack (list):
                Pilha utilizada para restaurar estados previamente
                desfeitos através da operação de refazer.

            current_file (str | None):
                Caminho do arquivo atualmente aberto no editor.
        """

        self.text_data = DoublyLinkedList()

        self.undo_stack = []
        self.redo_stack = []

        self.current_file = None

    def load_text(self, content):
        """
        Carrega um conteúdo textual para a estrutura de dados.

        O conteúdo recebido é dividido em linhas e armazenado
        na lista duplamente encadeada.

        Args:
            content (str):
                Texto completo a ser carregado.
        """

        self.text_data.clear()

        for line in content.splitlines():
            self.text_data.append(line)

    def get_text(self):
        """
        Reconstrói e retorna o texto armazenado.

        Returns:
            str:
                Conteúdo completo do editor em formato textual.
        """

        return "\n".join(self.text_data.to_list())

    def save_state(self, content):
        """
        Armazena um estado do texto na pilha de Undo.

        Sempre que uma modificação é realizada, o estado atual
        é salvo para permitir sua recuperação posteriormente.

        Para evitar crescimento excessivo de memória, o histórico
        é limitado a 100 estados.

        Args:
            content (str):
                Conteúdo atual do editor.
        """

        self.undo_stack.append(content)

        if len(self.undo_stack) > 100:
            self.undo_stack.pop(0)

        # Ao registrar uma nova alteração,
        # o histórico de Redo é invalidado.
        self.redo_stack.clear()

    def undo(self, current_content):
        """
        Desfaz a última alteração realizada.

        O estado atual é movido para a pilha de Redo
        e o estado anterior é recuperado da pilha de Undo.

        Args:
            current_content (str):
                Conteúdo atual do editor.

        Returns:
            str:
                Estado anterior do texto.
        """

        if not self.undo_stack:
            return current_content

        self.redo_stack.append(current_content)

        return self.undo_stack.pop()

    def redo(self, current_content):
        """
        Refaz uma alteração previamente desfeita.

        O estado atual é armazenado novamente na pilha de Undo
        e o último estado salvo na pilha de Redo é restaurado.

        Args:
            current_content (str):
                Conteúdo atual do editor.

        Returns:
            str:
                Estado restaurado do texto.
        """

        if not self.redo_stack:
            return current_content

        self.undo_stack.append(current_content)

        return self.redo_stack.pop()

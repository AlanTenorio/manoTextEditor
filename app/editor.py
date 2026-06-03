from structures import DoublyLinkedList

# aqui ta o editor, onde ta a estrutura de dados e as funções de manipulação do texto
class Editor:

    def __init__(self):

        self.text_data = DoublyLinkedList()

        self.undo_stack = []
        self.redo_stack = []

        self.current_file = None

    def load_text(self, content):

        self.text_data.clear()

        for line in content.splitlines():
            self.text_data.append(line)

    def get_text(self):

        return "\n".join(self.text_data.to_list())

    def save_state(self, content):

        self.undo_stack.append(content)

        if len(self.undo_stack) > 100:
            self.undo_stack.pop(0)

        self.redo_stack.clear()

    def undo(self, current_content):

        if not self.undo_stack:
            return current_content

        self.redo_stack.append(current_content)

        return self.undo_stack.pop()

    def redo(self, current_content):

        if not self.redo_stack:
            return current_content

        self.undo_stack.append(current_content)

        return self.redo_stack.pop()
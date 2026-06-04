from structures import DoublyLinkedList


class Editor:
    """
    Classe responsável pela lógica de manipulação do editor de texto.

    Utiliza uma lista duplamente encadeada para armazenar o conteúdo
    textual carregado e duas pilhas para gerenciar o histórico de
    alterações (Undo e Redo).

    A classe não possui interface gráfica; ela apenas controla os
    dados e operações relacionadas ao texto.
    """

    def __init__(self):
        """
        Inicializa os componentes internos do editor.

        Atributos:
            text_data (DoublyLinkedList):
                Estrutura de dados utilizada para armazenar as linhas
                do texto carregado no editor.

            undo_stack (list):
                Pilha responsável por armazenar os estados anteriores
                do texto, permitindo desfazer alterações.

            redo_stack (list):
                Pilha utilizada para armazenar estados removidos pelo
                comando Undo, permitindo restaurá-los posteriormente.

            current_file (str | None):
                Caminho do arquivo atualmente aberto no editor.
                Permanece como None quando nenhum arquivo está associado.
        """

        self.text_data = DoublyLinkedList()
        self.undo_stack = [""]
        self.redo_stack = []
        self.current_file = None

    def load_text(self, content):
        """
        Carrega um conteúdo textual para o editor.

        O texto recebido é dividido em linhas e armazenado na
        lista duplamente encadeada. Além disso, o histórico de
        alterações é reiniciado para refletir o novo conteúdo.

        Args:
            content (str):
                Conteúdo completo do arquivo aberto.
        """

        self.text_data.clear()

        for line in content.splitlines():
            self.text_data.append(line)
        self.undo_stack = [content]
        self.redo_stack.clear()

    def save_state(self, content):
        """
        Registra um novo estado do texto na pilha de Undo.

        Sempre que o conteúdo é alterado, seu estado atual pode
        ser armazenado para permitir operações futuras de desfazer.

        O método evita armazenar estados repetidos consecutivos,
        reduzindo o consumo de memória.

        O histórico é limitado a 100 estados.

        Args:
            content (str):
                Conteúdo atual do editor.
        """

        if not self.undo_stack or self.undo_stack[-1] != content:

            self.undo_stack.append(content)
            if len(self.undo_stack) > 100:
                self.undo_stack.pop(0)
            self.redo_stack.clear()

    def undo(self, current_content):
        """
        Desfaz a última alteração registrada.

        Remove o estado mais recente da pilha de Undo,
        armazenando-o na pilha de Redo para possibilitar
        sua restauração posteriormente.

        Args:
            current_content (str):
                Conteúdo atual exibido no editor.

        Returns:
            str:
                Estado anterior do texto.
        """

        if len(self.undo_stack) <= 1:
            return current_content

        ultimo_estado = self.undo_stack.pop()
        self.redo_stack.append(ultimo_estado)
        return self.undo_stack[-1]

    def redo(self, current_content):
        """
        Refaz uma alteração previamente desfeita.

        Recupera o estado mais recente da pilha de Redo
        e o reinsere na pilha de Undo.

        Args:
            current_content (str):
                Conteúdo atual exibido no editor.

        Returns:
            str:
                Estado restaurado após a operação de Redo.
        """

        if not self.redo_stack:
            return current_content
        estado_restaurado = self.redo_stack.pop()
        self.undo_stack.append(estado_restaurado)

        return estado_restaurado

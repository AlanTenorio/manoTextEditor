from structures import DoublyLinkedList

class Editor:
    """
    Classe de controle lógico (Backend). Responsável pelo gerenciamento do estado dos dados, 
    manipulação de arquivos e implementação do padrão de projeto focado em histórico (Undo/Redo).
    """

    def __init__(self):
        # Uso de uma Lista Duplamente Encadeada própria para armazenar as linhas de texto na memória.
        # Isso demonstra a aplicação prática de Estruturas de Dados disciplinares.
        self.text_data = DoublyLinkedList()
        
        # Implementação do mecanismo de histórico usando o conceito de Pilhas (LIFO - Last In, First Out).
        self.undo_stack = [""]  # Pilha de desfazer (inicia com estado vazio para permitir voltar ao início)
        self.redo_stack = []    # Pilha de refazer (limpa a cada nova ação do usuário)
        self.current_file = None # Armazena o caminho absoluto do arquivo ativo no Sistema Operacional

    def load_text(self, content):
        """Preenche a Lista Duplamente Encadeada com o conteúdo de um arquivo externo linha por linha."""
        self.text_data.clear() # Garante a limpeza da estrutura antes da carga para evitar sobreposição de memória
        for line in content.splitlines():
            self.text_data.append(line) # Alocação dinâmica de nós na lista encadeada para cada linha do texto
            
        # Sincroniza e reinicializa os estados das pilhas de histórico para o novo arquivo carregado
        self.undo_stack = [content]
        self.redo_stack.clear()

    def save_state(self, content):
        """
        Registra snapshots (estados) do texto na pilha de Undo. 
        Implementação simplificada do Design Pattern 'Memento'.
        """
        # Mecanismo de otimização: Só empilha se o estado atual for estritamente diferente do topo da pilha
        if not self.undo_stack or self.undo_stack[-1] != content:
            self.undo_stack.append(content)
            
            # Política de gerenciamento e limitação de memória RAM:
            # Impede estouro de memória limitando o histórico estritamente às últimas 100 ações.
            if len(self.undo_stack) > 100:
                self.undo_stack.pop(0) # Remove o estado mais antigo (base da pilha)
                
            self.redo_stack.clear() # Regra clássica de editores: novas digitações invalidam a árvore de Redo

    def undo(self, current_content):
        """
        Operação Desfazer: Transfere o estado atual do topo da pilha de Undo 
        para a pilha de Redo e retorna o estado imediatamente anterior.
        """
        if len(self.undo_stack) <= 1:
            return current_content # Bloqueio de segurança: impede o esvaziamento total da pilha inicial
        
        # Desempilha o estado atual do Undo e joga para a pilha de Redo
        self.redo_stack.append(self.undo_stack.pop())
        return self.undo_stack[-1] # Retorna o novo topo (o estado anterior que o usuário desejava recuperar)

    def redo(self, current_content):
        """
        Operação Refazer: Recupera estados que foram previamente desfeitos, 
        movendo-os de volta da pilha de Redo para a de Undo.
        """
        if not self.redo_stack:
            return current_content # Bloqueio de segurança: se a pilha de Redo estiver vazia, ignora a ação
            
        estado_restaurado = self.redo_stack.pop() # Remove o estado do topo de Redo
        self.undo_stack.append(estado_restaurado) # Devolve esse estado ao topo de Undo
        return estado_restaurado # Retorna o conteúdo restaurado para atualização imediata na interface gráfica
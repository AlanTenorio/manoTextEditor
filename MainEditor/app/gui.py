import tkinter as tk
from tkinter import filedialog, messagebox
from editor import Editor
from pdf_exporter import exportar_paginas_para_pdf

# pedi pro gemini pro comentar pq tava ilegivel pra documentação
 
class MiniNanoGUI:
    def __init__(self, root):
        self.root = root
        self.editor = Editor() # Instancia o motor lógico/gerenciador de arquivos externo
        self.root.title("MiniNano - WordPad Style")
        
        # --- Configurações de Inicialização e Responsividade da Janela ---
        self.root.state('zoomed') # Inicia a aplicação maximizada (tela cheia no Windows)
        self.root.attributes('-fullscreen', False) 
        
        # --- Variáveis de Controle de Estado e Layout Proporcional (Estilo A4) ---
        self.salvo = True
        self.LIMITE_LINHAS_POR_PAGINA = 32
        self.LARGURA_MAXIMA_CARACTERES = 70
        
        self.largura_base_pagina = 730
        self.altura_base_pagina = 680
        self.tamanho_base_fonte = 12
        self.fator_zoom = 1.0  # Multiplicador matemático para controle do Zoom (1.0 = 100%)
        
        # --- Definição das Paletas de Cores (Design System do App) ---
        self.tema_escuro = True  
        self.cores_escuras = ["#1e222a", "#2f343f", "#e5e9f0", "#1f2430", "#ffffff", "#21252b", "#7f848e"]
        self.cores_claras  = ["#e0e0e0", "#ffffff", "#1e1e1e", "#f0f0f0", "#000000", "#f5f5f5", "#a0a0a0"]
        
        C = self.cores_escuras if self.tema_escuro else self.cores_claras
        root.configure(bg=C[3])
        
        # Intercepta o fechamento da janela para validar se há alterações não salvas
        self.root.protocol("WM_DELETE_WINDOW", self.verificar_salvamento)


        # CONSTRUÇÃO DA INTERFACE GRÁFICA (UI) VIA TKINTER (aqui não tem brincadeira não T-T)

        # BARRA DE ARQUIVO SUPERIOR
        self.menu_top_bar = tk.Frame(root, bg=C[3], height=30, bd=0)
        self.menu_top_bar.pack(fill="x", side="top")
        
        self.file_header = tk.Label(self.menu_top_bar, text="New File", bg=C[3], fg=C[4], font=("Consolas", 10, "bold"), padx=10)
        self.file_header.pack(side="left")

        # SISTEMA DE ABAS (Mockup Visual)
        self.tab_bar = tk.Frame(root, bg=C[3], height=25)
        self.tab_bar.pack(fill="x", side="top")
        
        self.tab_inicio = tk.Label(self.tab_bar, text="Início", font=("Consolas", 9, "bold"), bg=C[0], fg=C[4], padx=15, pady=2, bd=1, relief="solid")
        self.tab_inicio.pack(side="left", padx=(10, 0))
        
        # FAIXA DE OPÇÕES (RIBBON) - Painel de Ferramentas Estilizado
        self.ribbon = tk.Frame(root, bg=C[3], bd=1, relief="solid", highlightthickness=0)
        self.ribbon.pack(fill="x", side="top", ipady=6)

        # Seção de Formatação de Fonte (Negrito, Itálico, Sublinhado)
        self.group_fonte = tk.LabelFrame(self.ribbon, text="Fonte", font=("Consolas", 8), bg=C[3], fg=C[6], padx=6, pady=4, bd=1, relief="groove")
        self.group_fonte.pack(side="left", padx=5, pady=2)

        btn_cfg = {"bg": "#2f343f" if self.tema_escuro else "#f0f0f0", "fg": C[4] if self.tema_escuro else C[2], "relief": "flat", "width": 3, "cursor": "hand2"}
        
        tk.Button(self.group_fonte, text="N", font=("Consolas", 10, "bold"), command=lambda: self.alterar_estilo("bold"), **btn_cfg).pack(side="left", padx=2)
        tk.Button(self.group_fonte, text="I", font=("Consolas", 10, "italic", "bold"), command=lambda: self.alterar_estilo("italic"), **btn_cfg).pack(side="left", padx=2)
        tk.Button(self.group_fonte, text="S", font=("Consolas", 10, "underline", "bold"), command=lambda: self.alterar_estilo("underline"), **btn_cfg).pack(side="left", padx=2)

        # Seção de Alinhamento de Parágrafo
        self.group_paragraph = tk.LabelFrame(self.ribbon, text="Parágrafo", font=("Consolas", 8), bg=C[3], fg=C[6], padx=6, pady=4, bd=1, relief="groove")
        self.group_paragraph.pack(side="left", padx=5, pady=2)

        tk.Button(self.group_paragraph, text="[=", font=("Consolas", 9, "bold"), command=lambda: self.alterar_alinhamento("left"), **btn_cfg).pack(side="left", padx=2)
        tk.Button(self.group_paragraph, text="==", font=("Consolas", 9, "bold"), command=lambda: self.alterar_alinhamento("center"), **btn_cfg).pack(side="left", padx=2)
        tk.Button(self.group_paragraph, text="=]", font=("Consolas", 9, "bold"), command=lambda: self.alterar_alinhamento("right"), **btn_cfg).pack(side="left", padx=2)

        # Seção de Utilitários do Sistema
        self.group_sistema = tk.LabelFrame(self.ribbon, text="Sistema", font=("Consolas", 8), bg=C[3], fg=C[6], padx=6, pady=4, bd=1, relief="groove")
        self.group_sistema.pack(side="left", padx=5, pady=2)

        self.btn_tema = tk.Button(self.group_sistema, text="T", font=("Consolas", 9, "bold"), command=self.alternar_tema, **btn_cfg)
        self.btn_tema.pack(side="left", padx=2)

        # ÁREA DE TRABALHO (WORKSPACE) - Estrutura complexa de Scrollbar + Canvas + Frames
        main_container = tk.Frame(root, bg=C[0])
        main_container.pack(fill="both", expand=True)

        # O Canvas é obrigatório no Tkinter para permitir rolagem de componentes complexos (múltiplas páginas)
        self.workspace_canvas = tk.Canvas(main_container, bg=C[0], highlightthickness=0)
        self.workspace_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(main_container, command=self.workspace_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.workspace_canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno que agrupa os componentes dentro do Canvas
        self.center_frame = tk.Frame(self.workspace_canvas, bg=C[0])
        self.workspace_canvas.create_window((0, 0), window=self.center_frame, anchor="nw")

        # Container onde as folhas (páginas de texto) serão empilhadas verticalmente
        self.pages_container = tk.Frame(self.center_frame, bg=C[0])
        self.pages_container.pack(pady=20)

        # Estruturas de dados (listas) paralelas para rastrear e gerenciar dinamicamente as páginas em tempo de execução
        self.paginas_text_widgets = []
        self.paginas_frames = []
        self.paginas_line_widgets = []

        # Inicializa o editor com a primeira página em branco
        self.criar_nova_pagina_visual()

        # BARRA DE STATUS INFERIOR
        self.bottom_bar = tk.Frame(root, bg="#d8d8d0", bd=1, relief="solid", height=22)
        self.bottom_bar.pack(fill="x", side="bottom")
        
        self.lbl_shortcuts = tk.Label(self.bottom_bar, text="^Z Redo | ^S Save File | ^N New File | Ctrl +/=: Zoom+ | Ctrl -: Zoom-", bg="#d8d8d0", fg="#222222", font=("Consolas", 9), padx=10)
        self.lbl_shortcuts.pack(side="left")
        
        self.lbl_zoom = tk.Label(self.bottom_bar, text="100%", bg="#d8d8d0", fg="#222222", font=("Consolas", 9, "bold"), padx=15)
        self.lbl_zoom.pack(side="right")

        # Vinculação de eventos de redimensionamento para recalcular barras de rolagem e centralização
        self.center_frame.bind("<Configure>", self.ajustar_rolagem_canvas)
        self.workspace_canvas.bind("<Configure>", self.centralizar_folha)
        
        # Atalhos Globais de Teclado (Key Bindings) ---
        root.bind("<Control-s>", lambda e: self.save_file())
        root.bind("<Control-n>", lambda e: self.new_file())
        root.bind("<Control-q>", lambda e: self.verificar_salvamento())
        root.bind("<Control-equal>", lambda e: self.alterar_zoom(0.1))
        root.bind("<Control-plus>", lambda e: self.alterar_zoom(0.1))
        root.bind("<Control-minus>", lambda e: self.alterar_zoom(-0.1))

        self.update_status()

    @property
    def text(self):
        """Retorna o widget de texto que está focado no momento ou o último da lista."""
        focado = self.root.focus_get()
        return focado if focado in self.paginas_text_widgets else self.paginas_text_widgets[-1]

    def alterar_zoom(self, variacao):
        """Altera dinamicamente as proporções de tamanho de folha, fontes e tags com base no fator de zoom."""
        novo_zoom = round(self.fator_zoom + variacao, 1)
        if 0.5 <= novo_zoom <= 2.0: # Limita o zoom entre 50% e 200%
            self.fator_zoom = novo_zoom
            
            # Aplica a regra de três matemática para escalar todos os elementos visuais
            largura_atual = int(self.largura_base_pagina * self.fator_zoom)
            altura_atual = int(self.altura_base_pagina * self.fator_zoom)
            tamanho_fonte_atual = int(self.tamanho_base_fonte * self.fator_zoom)
            
            for frame in self.paginas_frames:
                frame.config(width=largura_atual, height=altura_atual)
                
            for tw in self.paginas_text_widgets:
                tw.config(font=("Consolas", tamanho_fonte_atual))
                # Atualização crucial das TAGS de estilo, caso contrário o texto formatado ignoraria o Zoom
                tw.tag_configure("bold", font=("Consolas", tamanho_fonte_atual, "bold"))
                tw.tag_configure("italic", font=("Consolas", tamanho_fonte_atual, "italic"))
                tw.tag_configure("underline", font=("Consolas", tamanho_fonte_atual, "underline"))

            for ln in self.paginas_line_widgets:
                ln.config(font=("Consolas", tamanho_fonte_atual))
            
            self.lbl_zoom.config(text=f"{int(self.fator_zoom * 100)}%")
            self.root.update_idletasks()
            self.workspace_canvas.configure(scrollregion=self.workspace_canvas.bbox("all"))

    def criar_nova_pagina_visual(self):
        """Gera uma nova folha de papel física e independente na interface do usuário 
."""
        C = self.cores_escuras if self.tema_escuro else self.cores_claras
        
        largura_atual = int(self.largura_base_pagina * self.fator_zoom)
        altura_atual = int(self.altura_base_pagina * self.fator_zoom)
        tamanho_fonte_atual = int(self.tamanho_base_fonte * self.fator_zoom)
        
        # Frame que simula o limite da folha física
        paper_frame = tk.Frame(self.pages_container, bg=C[1], bd=1, relief="solid", highlightthickness=0, width=largura_atual, height=altura_atual)
        paper_frame.pack(pady=15, padx=50)
        paper_frame.pack_propagate(False) # Evita que o Frame encolha ou mude de tamanho baseado no texto interno
        
        text_cfg = {"relief": "flat", "borderwidth": 0, "highlightthickness": 0, "font": ("Consolas", tamanho_fonte_atual)}

        # Barra lateral interna exclusiva da página para renderização dos números de linha
        line_numbers = tk.Text(paper_frame, width=4, padx=5, pady=20, bg=C[5], fg=C[6], state="disabled", **text_cfg)
        line_numbers.pack(side="left", fill="y")

        # Área real de digitação da página
        text_widget = tk.Text(paper_frame, undo=True, wrap="none", bg=C[1], fg=C[2], insertbackground="white" if self.tema_escuro else "black", padx=20, pady=20, **text_cfg)
        text_widget.pack(side="left", fill="both", expand=True)
        
        # Inicialização das Tags de Formatação de Texto dentro deste escopo de widget
        text_widget.tag_configure("bold", font=("Consolas", tamanho_fonte_atual, "bold"))
        text_widget.tag_configure("italic", font=("Consolas", tamanho_fonte_atual, "italic", "bold"))
        text_widget.tag_configure("underline", font=("Consolas", tamanho_fonte_atual, "underline", "bold"))
        text_widget.tag_configure("left", justify="left")
        text_widget.tag_configure("center", justify="center")
        text_widget.tag_configure("right", justify="right")

        # Binds internos monitorando em tempo real ações de teclado e colagem de texto
        text_widget.bind("<KeyRelease>", lambda e, tw=text_widget: self.on_edit(tw, e))
        text_widget.bind("<<Paste>>", lambda e, tw=text_widget: self.on_paste(tw, e))
        
        # Atualiza as estruturas paralelas para que os métodos globais conheçam a existência desta nova folha
        self.paginas_text_widgets.append(text_widget)
        self.paginas_frames.append(paper_frame)
        self.paginas_line_widgets.append(line_numbers)

        self.update_line_numbers_da_pagina(text_widget, line_numbers)
        text_widget.focus_set()

        # Força o recálculo do Canvas de rolagem e rola a tela para focar na nova página criada
        self.root.update_idletasks()
        self.workspace_canvas.configure(scrollregion=self.workspace_canvas.bbox("all"))
        self.root.after(10, lambda: self.workspace_canvas.yview_moveto(1.0))

    def centralizar_folha(self, event):
        """Garante que a folha física permaneça perfeitamente centralizada horizontalmente no Canvas."""
        self.workspace_canvas.itemconfig(self.workspace_canvas.find_all()[0], width=event.width)

    def ajustar_rolagem_canvas(self, event):
        """Recalcula dinamicamente a área interna de scroll do Canvas quando uma nova folha é adicionada."""
        self.workspace_canvas.configure(scrollregion=self.workspace_canvas.bbox("all"))

    def alterar_estilo(self, estilo):
        """Aplica ou remove tags de formatação (Bold/Italic/Underline) no texto selecionado (sel.first a sel.last)."""
        try:
            tw = self.text
            if estilo in tw.tag_names("sel.first"):
                tw.tag_remove(estilo, "sel.first", "sel.last")
            else:
                tw.tag_add(estilo, "sel.first", "sel.last")
            self.salvo = False
        except tk.TclError:
            pass # Silencia exceções geradas se o usuário clicar no botão sem texto selecionado

    def alterar_alinhamento(self, alinhamento):
        """Gerencia tags de alinhamento de parágrafo, limpando seleções anteriores para evitar conflitos na mesma linha."""
        try:
            tw = self.text
            inicio, fmt = "sel.first", "sel.last"
            for align in ["left", "center", "right"]:
                tw.tag_remove(align, inicio, f"{fmt} lineend") # Limpa alinhamentos prévios
            tw.tag_add(alinhamento, inicio, f"{fmt} lineend")
            self.salvo = False
        except tk.TclError:
            pass

    def alternar_tema(self):
        """Inicia a inversão e transição de cores do aplicativo."""
        alvo = self.cores_claras if self.tema_escuro else self.cores_escuras
        self.tema_escuro = not self.tema_escuro
        self.animar_fade(0, 10, alvo) # Dispara motor de interpolação linear em 10 passos

    def animar_fade(self, passo, total_passos, cores_alvo):
        """Executa uma animação de fade (interpolação matemática RGB) para transição suave de temas sem lag na UI."""
        if passo > total_passos: return
        origem = self.cores_escuras if not self.tema_escuro else self.cores_claras
        
        def interpolar_cor(hex_origem, hex_alvo, p, total):
            """Calcula matematicamente o ponto intermediário entre duas cores Hexadecimais."""
            r1, g1, b1 = int(hex_origem[1:3], 16), int(hex_origem[3:5], 16), int(hex_origem[5:7], 16)
            r2, g2, b2 = int(hex_alvo[1:3], 16), int(hex_alvo[3:5], 16), int(hex_alvo[5:7], 16)
            r = int(r1 + (r2 - r1) * (p / total))
            g = int(g1 + (g2 - g1) * (p / total))
            b = int(b1 + (b2 - b1) * (p / total))
            return f"#{r:02x}{g:02x}{b:02x}"

        # Loop de cálculo de cores intermediárias para todos os elementos visuais do app
        bg_space = interpolar_cor(origem[0], cores_alvo[0], passo, total_passos)
        bg_paper = interpolar_cor(origem[1], cores_alvo[1], passo, total_passos)
        fg_text  = interpolar_cor(origem[2], cores_alvo[2], passo, total_passos)
        bg_hdr   = interpolar_cor(origem[3], cores_alvo[3], passo, total_passos)
        fg_hdr   = interpolar_cor(origem[4], cores_alvo[4], passo, total_passos)
        bg_lines = interpolar_cor(origem[5], cores_alvo[5], passo, total_passos)
        fg_lines = interpolar_cor(origem[6], cores_alvo[6], passo, total_passos)

        # Atualização em lote das propriedades visuais dos componentes do Tkinter
        self.root.configure(bg=bg_space)
        self.workspace_canvas.config(bg=bg_space)
        self.center_frame.config(bg=bg_space)
        self.pages_container.config(bg=bg_space)
        self.menu_top_bar.config(bg=bg_hdr)
        self.file_header.config(bg=bg_hdr, fg=fg_hdr)
        self.tab_bar.config(bg=bg_hdr)
        self.ribbon.config(bg=bg_hdr)
        self.group_fonte.config(bg=bg_hdr, fg=fg_lines)
        self.group_paragraph.config(bg=bg_hdr, fg=fg_lines)
        self.group_sistema.config(bg=bg_hdr, fg=fg_lines)

        btn_bg = "#2f343f" if self.tema_escuro else "#f0f0f0"
        btn_fg = fg_hdr if self.tema_escuro else fg_text
        
        for child in self.group_fonte.winfo_children(): child.config(bg=btn_bg, fg=btn_fg)
        for child in self.group_paragraph.winfo_children(): child.config(bg=btn_bg, fg=btn_fg)
        for child in self.group_sistema.winfo_children(): child.config(bg=btn_bg, fg=btn_fg)

        for pf in self.paginas_frames: pf.config(bg=bg_paper)
        for tw in self.paginas_text_widgets: tw.config(bg=bg_paper, fg=fg_text, insertbackground="white" if self.tema_escuro else "black")
        for ln in self.paginas_line_widgets: ln.config(bg=bg_lines, fg=fg_lines)

        # Recursão temporizada (.after) criando o loop de animação assíncrono e não-bloqueante
        self.root.after(20, lambda: self.animar_fade(passo + 1, total_passos, cores_alvo))

    def verificar_salvamento(self):
        """Janela de confirmação para prevenir perda de dados ao fechar a aplicação."""
        if not self.salvo:
            resposta = messagebox.askyesnocancel("Aviso", "Deseja salvar antes de sair?")
            if resposta is True:
                self.save_file()
                if self.salvo: self.root.quit()
            elif resposta is False: self.root.quit()
        else:
            self.root.quit()

    def update_line_numbers_da_pagina(self, text_widget, line_widget):
        """Sincroniza a numeração de linhas lateral baseado na quebra de linhas reais (\n) injetadas no Widget."""
        total_lines = int(text_widget.index("end-1c").split(".")[0])
        numbers = "\n".join(str(i) for i in range(1, total_lines + 1))
        line_widget.config(state="normal")
        line_widget.delete("1.0", tk.END)
        line_widget.insert("1.0", numbers)
        line_widget.config(state="disabled") # Mantém em Read-Only para o usuário não editar os números

    def update_status(self):
        """Atualiza dinamicamente o título e indicador de alteração (*) na barra superior."""
        filename = self.editor.current_file.split("/")[-1] if self.editor.current_file else "New File"
        marcador = " *" if not self.salvo else ""
        self.file_header.config(text=f"nano {filename}{marcador}")

    def formatar_texto_com_quebras_reais(self, texto):
        """Algoritmo de Processamento de Texto: quebra strings longas inserindo caracteres '\\n' reais baseados no limite de largura física."""
        linhas_formatadas = []
        for lambda_line in texto.split("\n"):
            while len(lambda_line) > self.LARGURA_MAXIMA_CARACTERES:
                corte = lambda_line[:self.LARGURA_MAXIMA_CARACTERES]
                ultimo_espaco = corte.rfind(" ")
                # Tenta quebrar a linha de maneira inteligente em um espaço para não cortar palavras ao meio
                if ultimo_espaco != -1 and ultimo_espaco > (self.LARGURA_MAXIMA_CARACTERES - 15):
                    linhas_formatadas.append(lambda_line[:ultimo_espaco])
                    lambda_line = lambda_line[ultimo_espaco + 1:]
                else:
                    linhas_formatadas.append(corte)
                    lambda_line = lambda_line[self.LARGURA_MAXIMA_CARACTERES:]
            linhas_formatadas.append(lambda_line)
        return "\n".join(linhas_formatadas)

    def on_paste(self, text_widget, event):
        """Intercepta e reescreve a rotina de colagem (Ctrl+V) padrão para garantir que o texto colado sofra o algoritmo de quebra de linha real."""
        try:
            texto_clipboard = self.root.clipboard_get()
            texto_processado = self.formatar_texto_com_quebras_reais(texto_clipboard)
            try:
                text_widget.delete("sel.first", "sel.last")
            except tk.TclError:
                pass
            text_widget.insert("insert", texto_processado)
            self.salvo = False
            self.root.after(1, lambda: self._after_edit(text_widget))
            return "break" # Importante: Retorna "break" para anular o evento nativo de colagem do Tkinter e evitar duplicação
        except tk.TclError:
            pass

    def on_edit(self, text_widget, event=None):
        """Algoritmo Dinâmico de Edição: Monitora o fluxo do cursor de digitação em tempo real."""
        self.salvo = False
        idx = self.paginas_text_widgets.index(text_widget)

        # Regra de exclusão de folha física: se apagar tudo e não for a única página, destrói e remove as referências da lista
        if event and event.keysym in ["BackSpace", "Delete"]:
            if not text_widget.get("1.0", "end-1c") and len(self.paginas_text_widgets) > 1:
                self.paginas_frames[idx].destroy()
                self.paginas_text_widgets.pop(idx)
                self.paginas_frames.pop(idx)
                self.paginas_line_widgets.pop(idx)
                
                pagina_anterior = self.paginas_text_widgets[idx - 1]
                pagina_anterior.focus_set()
                pagina_anterior.mark_set("insert", "end-1c")
                
                self.workspace_canvas.configure(scrollregion=self.workspace_canvas.bbox("all"))
                self.update_status()
                return

            self.root.after(1, lambda: self._after_edit(text_widget))
            return

        pos_cursor = text_widget.index("insert")
        linha_num, coluna_num = map(int, pos_cursor.split("."))
        
        # Injeta quebra de linha forçada em tempo de digitação caso atinja a largura máxima horizontal da folha
        if coluna_num >= self.LARGURA_MAXIMA_CARACTERES:
            conteudo_linha = text_widget.get(f"{linha_num}.0", f"{linha_num}.end")
            ultimo_espaco = conteudo_linha.rfind(" ")
            if ultimo_espaco != -1 and ultimo_espaco > (self.LARGURA_MAXIMA_CARACTERES - 15):
                text_widget.delete(f"{linha_num}.{ultimo_espaco}")
                text_widget.insert(f"{linha_num}.{ultimo_espaco}", "\n")
            else:
                text_widget.insert("insert", "\n")

        self.root.after(1, lambda: self._after_edit(text_widget))

    def _after_edit(self, text_widget):
        """Garante o algoritmo de transbordo (overflow) vertical de texto entre páginas consecutivas."""
        if text_widget not in self.paginas_text_widgets: return
        idx = self.paginas_text_widgets.index(text_widget)
        ln_widget = self.paginas_line_widgets[idx]
        
        self.update_line_numbers_da_pagina(text_widget, ln_widget)
        self.update_status()

        linha_atual = int(text_widget.index("insert").split(".")[0])
        total_linhas = int(text_widget.index("end-1c").split(".")[0])
        
        # Algoritmo de Overflow: Se o volume de linhas da folha atual exceder o limite A4 físico (32 linhas)...
        if total_linhas > self.LIMITE_LINHAS_POR_PAGINA:
            conteudo_total = text_widget.get("1.0", "end-1c").split("\n")
            mantido = "\n".join(conteudo_total[:self.LIMITE_LINHAS_POR_PAGINA])
            excedente = "\n".join(conteudo_total[self.LIMITE_LINHAS_POR_PAGINA:])
            
            # Trunca o texto da página atual ao limite exato de 32 linhas
            text_widget.delete("1.0", tk.END)
            text_widget.insert("1.0", mantido)
            self.update_line_numbers_da_pagina(text_widget, ln_widget)
            
            # Se for a última folha visível do app, cria uma folha inteiramente nova embaixo
            if text_widget == self.paginas_text_widgets[-1]:
                self.criar_nova_pagina_visual()
                
            # Joga o texto excedente para o topo (1.0) da folha seguinte, mantendo o encadeamento coerente
            proximo_widget = self.paginas_text_widgets[idx + 1]
            proximo_widget.insert("1.0", excedente + "\n" if proximo_widget.get("1.0", "end-1c") else excedente)
            self._after_edit(proximo_widget) # Processamento recursivo caso ocorra efeito cascata em múltiplas páginas
            
            proximo_widget.focus_set()
            self.workspace_canvas.configure(scrollregion=self.workspace_canvas.bbox("all"))
        elif linha_atual > self.LIMITE_LINHAS_POR_PAGINA:
            if text_widget == self.paginas_text_widgets[-1]:
                self.criar_nova_pagina_visual()
            proximo_widget = self.paginas_text_widgets[idx + 1]
            proximo_widget.focus_set()
            proximo_widget.mark_set("insert", "1.0")

    def new_file(self):
        """Limpa toda a estrutura atual de páginas da memória RAM e reinicia o estado do editor do zero."""
        if not self.salvo and not messagebox.askyesno("Aviso", "Limpar documento atual?"): return
        
        # Varre e destrói fisicamente os objetos gráficos do Tkinter para prevenir Memory Leaks
        for pf in self.paginas_frames: pf.destroy()
        self.paginas_text_widgets.clear()
        self.paginas_frames.clear()
        self.paginas_line_widgets.clear()
        
        self.editor.current_file = None
        self.salvo = True
        self.criar_nova_pagina_visual()
        self.update_status()

    def save_file(self):
        """Invoca a caixa de diálogo nativa do S.O. para exportação dos Widgets de texto estruturados em páginas A4 reais de PDF."""
        if not self.editor.current_file or not self.editor.current_file.endswith(".pdf"):
            path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if not path: return
            self.editor.current_file = path
        try:
            # Passa a lista ordenada de widgets de texto para o módulo de backend processar a geração física das páginas
            exportar_paginas_para_pdf(self.editor.current_file, self.paginas_text_widgets)
            self.salvo = True
            self.update_status()
            messagebox.showinfo("Concluido", "PDF Geradpo com Sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao salvar PDF", f"Falha na exportação: {str(e)}")
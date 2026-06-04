import tkinter as tk
from tkinter import filedialog, messagebox

from editor import Editor

# Aqui ta o main e o tema da GUI


class MiniNanoGUI:

    def __init__(self, root):

        self.root = root
        self.editor = Editor()

        self.root.title("MiniNano")
        self.root.geometry("1000x650")

        BG = "#2f343f"
        FG = "#e5e9f0"

        root.configure(bg=BG)


        # BARRA SUPERIOR
        self.nano_header = tk.Label(
            root,
            text="MiniNano",
            bg="#1f2430",
            fg="#ffffff",
            font=("Consolas", 11, "bold"),
            pady=5
        )
        self.nano_header.pack(fill="x")


        # NOME DO ARQUIVO
        self.file_header = tk.Label(
            root,
            text="New File",
            bg="#2f343f",
            fg="#e5e9f0",
            font=("Consolas", 10),
            pady=3
        )

        self.file_header.pack(fill="x")


        # ÁREA PRINCIPAL
        frame = tk.Frame(root, bg=BG)

        frame.pack(
            fill="both",
            expand=True
        )

        self.line_numbers = tk.Text( # contador de linhas
            frame,
            width=4,
            padx=5,
            bg="#1f2430",
            fg="#7f848e",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            state="disabled",
            font=("Consolas", 12)
        )

        self.line_numbers.pack(
            side="left",
            fill="y"
        )

        self.text = tk.Text(
            frame,
            undo=True,
            wrap="none",
            bg="#2f343f",
            fg="#e5e9f0",
            insertbackground="white",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            font=("Consolas", 12)
        )

        self.text.pack(
            side="left",
            fill="both",
            expand=True
        )
        self.text.edit_modified(False)



       # BARRA INFERIOR ESTILO NANO

        bottom_frame = tk.Frame(
            root,
            bg="#d8d8d0"
        )

        bottom_frame.pack(
            fill="x",
            side="bottom"
        )

        linha1 = [
            "^O Write Out",
            "^R Read File",
            "^N New File"
        ]

        linha2 = [
            "^X Exit",
            "^Z Undo",
            "^Y Redo"
        ]

        for i in range(3):
            bottom_frame.grid_columnconfigure(
                i,
                weight=1
            )

        for col, texto in enumerate(linha1):

            lbl = tk.Label(
                bottom_frame,
                text=texto,
                bg="#d8d8d0",
                fg="#222222",
                font=("Consolas", 9),
                anchor="w"
            )

            lbl.grid(
                row=0,
                column=col,
                sticky="ew",
                padx=5
            )

        for col, texto in enumerate(linha2):

            lbl = tk.Label(
                bottom_frame,
                text=texto,
                bg="#d8d8d0",
                fg="#222222",
                font=("Consolas", 9),
                anchor="w"
            )

            lbl.grid(
                row=1,
                column=col,
                sticky="ew",
                padx=5
            )

        # ATALHOS
        def on_modified(self, event=None):
            if self.text.edit_modified():

                self.editor.save_state(
                    self.text.get("1.0", "end-1c")
                )

                self.update_line_numbers()

                self.text.edit_modified(False)

        self.text.bind(
            "<KeyPress>",
            self.on_edit
        )

        root.bind("<Control-z>", self.undo)
        root.bind("<Control-y>", self.redo)

        root.bind(
            "<Control-s>",
            lambda e: self.save_file()
        )

        root.bind(
            "<Control-o>",
            lambda e: self.open_file()
        )

        root.bind(
            "<Control-n>",
            lambda e: self.new_file()
        )

        root.bind(
            "<Control-q>",
            lambda e: self.root.quit()
        )


        self.update_status()
        self.update_line_numbers()

    # Atualizar linhas
    def update_line_numbers(self):

        total_lines = int(
            self.text.index("end-1c").split(".")[0]
        )

        numbers = "\n".join(
            str(i)
            for i in range(1, total_lines + 1)
        )

        self.line_numbers.config(state="normal")

        self.line_numbers.delete(
            "1.0",
            tk.END
        )

        self.line_numbers.insert(
            "1.0",
            numbers
        )

        self.line_numbers.config(state="disabled")


    # ATUALIZA TÍTULO
    def update_status(self):

        filename = (
            self.editor.current_file.split("/")[-1]
            if self.editor.current_file
            else "New File"
        )

        self.nano_header.config(
            text=f"nano {filename}"
        )

        self.file_header.config(
            text=filename
        )


    # EVENTOS DE EDIÇÃO
    def on_edit(self, event=None):

        self.root.after(
            1,
            self._after_edit
        )


    def _after_edit(self):

        content = self.text.get(
            "1.0",
            "end-1c"
        )

        self.editor.save_state(content)

        self.update_line_numbers()
    # NOVO ARQUIVO
    def new_file(self):

        self.text.delete(
            "1.0",
            tk.END
        )

        self.editor.current_file = None

        self.editor.undo_stack = [""]
        self.editor.redo_stack.clear()

        self.update_line_numbers()
        self.update_status()
        
    # ABRIR
    def open_file(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("All Files", "*.*")
            ]
        )

        if not path:
            return

        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                content = f.read()

            self.text.delete(
                "1.0",
                tk.END
            )

            self.text.insert(
                "1.0",
                content
            )

            self.update_line_numbers()

            self.editor.load_text(content)

            self.editor.current_file = path

            self.update_status()

        except Exception as e:

            messagebox.showerror(
                "Erro",
                str(e)
            )


    # SALVAR
    def save_file(self):

        if not self.editor.current_file:

            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[
                    ("Text Files", "*.txt"),
                    ("Python Files", "*.py"),
                    ("All Files", "*.*")
                ]
            )

            if not path:
                return

            self.editor.current_file = path

        try:

            with open(
                self.editor.current_file,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(
                    self.text.get(
                        "1.0",
                        "end-1c"
                    )
                )

            self.update_status()

        except Exception as e:

            messagebox.showerror(
                "Erro",
                str(e)
            )

    # UNDO
    def undo(self, event=None):

        current = self.text.get(
            "1.0",
            "end-1c"
        )

        previous = self.editor.undo(current)

        self.text.delete(
            "1.0",
            tk.END
        )

        self.text.insert(
            "1.0",
            previous
        )
        self.update_line_numbers()
        return "break"


    # REDO
    def redo(self, event=None):

        restored = self.editor.redo(
            self.text.get("1.0", "end-1c")
        )

        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", restored)

        self.update_line_numbers()
        return "break"

if __name__ == "__main__":

    root = tk.Tk()

    app = MiniNanoGUI(root)

    root.mainloop()

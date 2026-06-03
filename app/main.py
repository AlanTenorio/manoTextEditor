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
            text="nano New File",
            bg="#1d1f21",
            fg="white",
            font=("Consolas", 10, "bold"),
            anchor="center",
            pady=3
        )

        self.nano_header.pack(fill="x")


        # NOME DO ARQUIVO
        self.file_header = tk.Label(
            root,
            text="New File",
            bg="#d8d8d0",
            fg="#222222",
            font=("Consolas", 10),
            pady=1
        )

        self.file_header.pack(fill="x")


        # ÁREA PRINCIPAL
        frame = tk.Frame(
            root,
            bg=BG
        )

        frame.pack(
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(frame)

        scrollbar.pack(
            side="right",
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
            fill="both",
            expand=True
        )

        self.text.config(
            yscrollcommand=scrollbar.set
        )

        scrollbar.config(
            command=self.text.yview
        )


        # BARRAS INFERIORES
        bottom_frame = tk.Frame(
            root,
            bg="#d8d8d0"
        )

        bottom_frame.pack(
            fill="x",
            side="bottom"
        )

        linha1 = [
            "^G Help",
            "^O Write Out",
            "^W Where Is",
            "^K Cut",
            "^T Execute"
        ]

        linha2 = [
            "^X Exit",
            "^R Read File",
            "^\\ Replace",
            "^U Paste",
            "^J Justify"
        ]

        for i in range(5):
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
        self.text.bind(
            "<KeyRelease>",
            self.on_edit
        )

        self.text.bind(
            "<Control-z>",
            self.undo
        )

        self.text.bind(
            "<Control-y>",
            self.redo
        )

        self.text.bind(
            "<Control-s>",
            lambda e: self.save_file()
        )

        self.text.bind(
            "<Control-o>",
            lambda e: self.open_file()
        )

        self.text.bind(
            "<Control-n>",
            lambda e: self.new_file()
        )

        self.text.bind(
            "<Control-q>",
            lambda e: self.root.quit()
        )

        self.update_status()


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


    # EVENTO DE EDIÇÃO
    def on_edit(self, event=None):

        content = self.text.get(
            "1.0",
            "end-1c"
        )

        self.editor.save_state(content)


    # NOVO ARQUIVO
    def new_file(self):

        self.text.delete(
            "1.0",
            tk.END
        )

        self.editor.current_file = None

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

        return "break"


    # REDO
    def redo(self, event=None):

        current = self.text.get(
            "1.0",
            "end-1c"
        )

        restored = self.editor.redo(current)

        self.text.delete(
            "1.0",
            tk.END
        )

        self.text.insert(
            "1.0",
            restored
        )

        return "break"


if __name__ == "__main__":

    root = tk.Tk()

    app = MiniNanoGUI(root)

    root.mainloop()
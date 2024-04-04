import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
from tkinter.scrolledtext import ScrolledText

class NotepadApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Bloco de Notas")
        self.master.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.text_area = ScrolledText(self.master, wrap="word", undo=True)
        self.text_area.pack(expand=True, fill="both")

        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Novo", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Abrir", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Salvar", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.confirm_quit)

        edit_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Editar", menu=edit_menu)
        edit_menu.add_command(label="Desfazer", accelerator="Ctrl+Z", command=self.undo)
        edit_menu.add_command(label="Refazer", accelerator="Ctrl+Shift+Z", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Localizar", accelerator="Ctrl+F", command=self.find_text)
        edit_menu.add_command(label="Substituir", accelerator="Ctrl+R", command=self.replace_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Recuar", accelerator="Tab", command=self.indent_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Contar Palavras", command=self.count_words)
        edit_menu.add_command(label="Contar Caracteres", command=self.count_characters)

        format_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Formatar", menu=format_menu)
        format_menu.add_command(label="Fonte", command=self.change_font)
        format_menu.add_command(label="Cor da Fonte", command=self.change_font_color)
        format_menu.add_command(label="Cor de Fundo", command=self.change_background)
        format_menu.add_separator()
        format_menu.add_command(label="Negrito", accelerator="Ctrl+B", command=lambda: self.apply_tag("bold"))
        format_menu.add_command(label="Itálico", accelerator="Ctrl+I", command=lambda: self.apply_tag("italic"))
        format_menu.add_command(label="Sublinhado", accelerator="Ctrl+U", command=lambda: self.apply_tag("underline"))

        self.master.bind_all("<Control-n>", lambda event: self.new_file())
        self.master.bind_all("<Control-o>", lambda event: self.open_file())
        self.master.bind_all("<Control-s>", lambda event: self.save_file())
        self.master.bind_all("<Control-z>", lambda event: self.undo())
        self.master.bind_all("<Control-Shift-z>", lambda event: self.redo())
        self.master.bind_all("<Control-f>", lambda event: self.find_text())
        self.master.bind_all("<Control-r>", lambda event: self.replace_text())
        self.master.bind_all("<Tab>", lambda event: self.indent_text())
        self.master.bind_all("<Control-b>", lambda event: self.apply_tag("bold"))
        self.master.bind_all("<Control-i>", lambda event: self.apply_tag("italic"))
        self.master.bind_all("<Control-u>", lambda event: self.apply_tag("underline"))

    def new_file(self):
        self.text_area.delete("1.0", tk.END)

    def open_file(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, "r", encoding='utf-8') as file:
                    content = file.read()
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Erro ao abrir o arquivo", str(e))

    def save_file(self):
        try:
            content = self.text_area.get("1.0", tk.END)
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, "w", encoding='utf-8') as file:
                    file.write(content)
        except Exception as e:
            messagebox.showerror("Erro ao salvar o arquivo", str(e))

    def confirm_quit(self):
        if messagebox.askokcancel("Sair", "Tem certeza de que deseja sair?"):
            self.master.quit()

    def undo(self):
        try:
            self.text_area.edit_undo()
        except Exception as e:
            messagebox.showerror("Erro ao desfazer", str(e))

    def redo(self):
        try:
            self.text_area.edit_redo()
        except Exception as e:
            messagebox.showerror("Erro ao refazer", str(e))

    def find_text(self):
        # Implementar lógica para encontrar texto
        pass

    def replace_text(self):
        # Implementar lógica para substituir texto
        pass

    def indent_text(self):
        self.text_area.insert(tk.INSERT, "\t")

    def count_words(self):
        content = self.text_area.get("1.0", tk.END)
        word_count = len(content.split())
        messagebox.showinfo("Contagem de Palavras", f"Total de Palavras: {word_count}")

    def count_characters(self):
        content = self.text_area.get("1.0", tk.END)
        char_count = len(content)
        messagebox.showinfo("Contagem de Caracteres", f"Total de Caracteres: {char_count}")

    def change_font(self):
        font_tuple = tk.font.families()
        selected_font = fontchooser.askfont(font=font_tuple)
        if selected_font:
            self.text_area.configure(font=selected_font)

    def change_background(self):
        color = colorchooser.askcolor(title="Escolha a Cor de Fundo")[1]
        self.text_area.configure(bg=color)

    def change_font_color(self):
        color = colorchooser.askcolor(title="Escolha a Cor da Fonte")[1]
        self.text_area.configure(fg=color)

    def apply_tag(self, tag):
        if tag == "bold":
            self.text_area.tag_add(tag, "sel.first", "sel.last")
            self.text_area.tag_configure(tag, font=("Arial", 12, "bold"))
        elif tag == "italic":
            self.text_area.tag_add(tag, "sel.first", "sel.last")
            self.text_area.tag_configure(tag, font=("Arial", 12, "italic"))
        elif tag == "underline":
            self.text_area.tag_add(tag, "sel.first", "sel.last")
            self.text_area.tag_configure(tag, underline=True)

def main():
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

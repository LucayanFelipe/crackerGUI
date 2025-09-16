import pyzipper
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed


def ataque_dicionario_aes(zip_path, dicionarios, progresso_callback=None, senha_atual_callback=None):
    # Carregar senhas dos dicionários
    senhas = []
    for dic in dicionarios:
        with open(dic, "r", encoding="utf-8", errors="ignore") as f:
            for linha in f:
                palavra = linha.strip()
                if palavra:
                    senhas.append(palavra)

    if not senhas:  # fallback mínimo
        senhas = ["123", "senha", "teste"]

    total = len(senhas)
    encontrado = threading.Event()  # sinal para parar as threads
    resultado = [None]  # container mutável para guardar a senha

    def testar_senha(i, senha):
        if encontrado.is_set():
            return None  # já achou, não precisa mais
        senha_bytes = senha.strip().encode("utf-8")

        # Atualiza senha atual
        if senha_atual_callback:
            senha_atual_callback(senha)

        try:
            with pyzipper.AESZipFile(zip_path) as zf:
                with tempfile.TemporaryDirectory() as tmpdir:
                    zf.extractall(path=tmpdir, pwd=senha_bytes)
                    encontrado.set()
                    resultado[0] = senha
                    return senha
        except RuntimeError:
            pass
        except Exception as e:
            print(f"[!] Erro inesperado com '{senha}': {e}")

        # Atualiza progresso
        if progresso_callback:
            progresso_callback(i, total)
        return None

    # Número de threads = núcleos do SO
    n_threads = os.cpu_count() or 4

    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        futures = [executor.submit(testar_senha, i, senha) for i, senha in enumerate(senhas, 1)]
        for future in as_completed(futures):
            if future.result():
                return future.result()

    return "Senha não encontrada"


class ZipCrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AES ZIP Dictionary Cracker")

        self.zip_path = tk.StringVar()
        self.dicionarios = []

        tk.Label(root, text="Arquivo ZIP:").pack(pady=(10,0))
        tk.Entry(root, textvariable=self.zip_path, width=50).pack()
        tk.Button(root, text="Selecionar ZIP", command=self.selecionar_zip).pack(pady=(5,10))

        tk.Button(root, text="Adicionar Dicionário", command=self.adicionar_dic).pack()
        tk.Button(root, text="Remover Dicionário Selecionado", command=self.remover_dic).pack(pady=(5,5))
        self.dic_listbox = tk.Listbox(root, width=50, height=5)
        self.dic_listbox.pack(pady=(0,10))

        # Barra de progresso
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=(5,5))

        # Label mostrando senha atual testada
        self.senha_atual_var = tk.StringVar(value="Senha atual: -")
        tk.Label(root, textvariable=self.senha_atual_var).pack(pady=(5,10))

        tk.Button(root, text="Iniciar Ataque", command=self.iniciar_ataque).pack(pady=(10,10))

    def selecionar_zip(self):
        path = filedialog.askopenfilename(filetypes=[("Arquivos ZIP", "*.zip")])
        if path:
            self.zip_path.set(path)

    def adicionar_dic(self):
        path = filedialog.askopenfilename(filetypes=[("Textos", "*.txt")])
        if path:
            self.dicionarios.append(path)
            self.dic_listbox.insert(tk.END, os.path.basename(path))

    def remover_dic(self):
        selecionados = self.dic_listbox.curselection()
        if not selecionados:
            return
        for i in reversed(selecionados):
            self.dic_listbox.delete(i)
            del self.dicionarios[i]

    def iniciar_ataque(self):
        if not self.zip_path.get():
            messagebox.showerror("Erro", "Selecione um arquivo ZIP!")
            return
        if not self.dicionarios:
            messagebox.showwarning("Aviso", "Nenhum dicionário adicionado. Será usado dicionário fallback.")

        def progresso(atual, total):
            percent = int((atual / total) * 100)
            self.progress_bar['value'] = percent
            self.root.update_idletasks()

        def senha_atual(senha):
            self.senha_atual_var.set(f"Senha atual: {senha}")
            self.root.update_idletasks()

        def rodar():
            resultado = ataque_dicionario_aes(
                self.zip_path.get(),
                self.dicionarios,
                progresso_callback=progresso,
                senha_atual_callback=senha_atual
            )
            if resultado != "Senha não encontrada":
                messagebox.showinfo("Resultado", f"Hackeado com sucesso meu patrão, senha do arquivo: {resultado}")
            else:
                messagebox.showinfo("Resultado", "Senha não encontrada!")

            # Resetar barra e label
            self.progress_bar['value'] = 0
            self.senha_atual_var.set("Senha atual: -")

        threading.Thread(target=rodar, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = ZipCrackerGUI(root)
    root.mainloop()

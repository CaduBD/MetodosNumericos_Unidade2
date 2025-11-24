import customtkinter as ctk
import numpy as np
import sympy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

# =============================================================================
# LÓGICA MATEMÁTICA
# =============================================================================

def eliminacao_gauss(A, b):
    try:
        n = len(b)
        M = np.hstack((A, b.reshape(-1, 1))).astype(float)
        for i in range(n):
            if M[i, i] == 0: return None
            for j in range(i + 1, n):
                fator = M[j, i] / M[i, i]
                M[j, i:] -= fator * M[i, i:]
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            soma = np.dot(M[i, i+1:n], x[i+1:n])
            x[i] = (M[i, n] - soma) / M[i, i]
        return x
    except:
        return None

# Ajustado: tol=1e-6 e max_iter=160
def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=160):
    n = len(b)
    x = np.zeros(n) if x0 is None else x0
    aviso = ""
    
    diag = np.abs(np.diag(A))
    soma_linhas = np.sum(np.abs(A), axis=1) - diag
    if not np.all(diag > soma_linhas):
        aviso = "⚠️ AVISO: Matriz não é estritamente diagonal dominante.\n"

    for k in range(max_iter):
        x_old = x.copy()
        for i in range(n):
            s1 = np.dot(A[i, :i], x[:i])
            s2 = np.dot(A[i, i+1:], x_old[i+1:])
            try:
                x[i] = (b[i] - s1 - s2) / A[i, i]
            except ZeroDivisionError:
                return None, 0, 0, "Erro: Divisão por zero."
        
        norm_x = np.linalg.norm(x, ord=np.inf)
        if norm_x == 0: norm_x = 1e-10
        erro = np.linalg.norm(x - x_old, ord=np.inf) / norm_x
        
        if erro < tol:
            return x, k+1, erro, aviso
            
    return x, max_iter, erro, aviso

def minimos_quadrados(x, y, tipo):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    n = len(x)
    
    if tipo == "Reta":
        A = np.vstack([x, np.ones(n)]).T
        a, b = np.linalg.lstsq(A, y, rcond=None)[0]
        y_calc = a * x + b
        erro = np.sum((y - y_calc)**2)
        func = lambda v: a * v + b
        return f"y = {a:.4f}x + {b:.4f}", func, erro

    elif tipo == "Parábola":
        A = np.vstack([x**2, x, np.ones(n)]).T
        a, b, c = np.linalg.lstsq(A, y, rcond=None)[0]
        y_calc = a * (x**2) + b * x + c
        erro = np.sum((y - y_calc)**2)
        func = lambda v: a * (v**2) + b * v + c
        return f"y = {a:.4f}x² + {b:.4f}x + {c:.4f}", func, erro

    elif tipo == "Exponencial":
        if np.any(y <= 0): return "Erro: Y deve ser positivo.", None, 0
        Y_ln = np.log(y)
        A_mat = np.vstack([x, np.ones(n)]).T
        B_calc, A_calc = np.linalg.lstsq(A_mat, Y_ln, rcond=None)[0]
        a_final = np.exp(A_calc)
        b_final = B_calc
        y_calc = a_final * np.exp(b_final * x)
        erro = np.sum((y - y_calc)**2)
        func = lambda v: a_final * np.exp(b_final * v)
        return f"y = {a_final:.4f} * e^({b_final:.4f}x)", func, erro
        
    return "Inválido", None, 0

def integrar_numerico(modo, dados, expr="", a=0, b=0, n=0):
    y_vals = []
    h = 0
    
    if modo == 'func':
        try:
            x_sym = sympy.symbols('x')
            f = sympy.lambdify(x_sym, sympy.parse_expr(expr), 'numpy')
            h = (b - a) / n
            x_points = np.linspace(a, b, n + 1)
            y_vals = f(x_points)
        except Exception as e:
            return None, None, f"Erro na função: {e}"
    else:
        y_vals = dados['y']
        h = dados['h']

    soma_t = y_vals[0] + y_vals[-1] + 2 * np.sum(y_vals[1:-1])
    res_trap = (h / 2) * soma_t

    res_simp = None
    if (len(y_vals) - 1) % 2 == 0:
        soma_s = y_vals[0] + y_vals[-1] + 4 * np.sum(y_vals[1:-1:2]) + 2 * np.sum(y_vals[2:-1:2])
        res_simp = (h / 3) * soma_s
    
    return res_trap, res_simp, None

# =============================================================================
# INTERFACE GRÁFICA 
# =============================================================================

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Projeto Numérico - Unidade 2 (Versão Final)")
        self.geometry("1200x900") 
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # --- DEFINIÇÃO DE FONTES ---
        self.font_title = ("Roboto", 24, "bold")
        self.font_std = ("Roboto", 18)
        self.font_btn = ("Roboto", 20, "bold")
        self.font_code = ("Courier New", 18, "bold")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.tabview._segmented_button.configure(font=self.font_btn, height=50) # Abas maiores
        
        self.tab_sis = self.tabview.add("Sistemas Lineares")
        self.tab_mmq = self.tabview.add("Mínimos Quadrados")
        self.tab_int = self.tabview.add("Integração")

        self.setup_sistemas()
        self.setup_mmq()
        self.setup_integracao()

    # --- ABA 1: SISTEMAS LINEARES ---
    def setup_sistemas(self):
        tab = self.tab_sis
        tab.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(tab, text="Matriz A (Linhas separadas por Enter):", font=self.font_title).grid(row=0, column=0, sticky="w", padx=10, pady=(10,0))
        self.txt_A = ctk.CTkTextbox(tab, height=150, font=self.font_code)
        self.txt_A.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.txt_A.insert("0.0", "3 2 4\n1 1 2\n4 3 2")

        ctk.CTkLabel(tab, text="Vetor b (Espaço):", font=self.font_title).grid(row=2, column=0, sticky="w", padx=10, pady=(15,0))
        self.entry_b = ctk.CTkEntry(tab, font=self.font_code, height=40)
        self.entry_b.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.entry_b.insert(0, "1 2 3")

        self.metodo_var = ctk.StringVar(value="Gauss")
        frame_opts = ctk.CTkFrame(tab)
        frame_opts.grid(row=4, column=0, padx=10, pady=15, sticky="ew")
        
        # Radio Buttons
        rb1 = ctk.CTkRadioButton(frame_opts, text="Eliminação de Gauss", variable=self.metodo_var, value="Gauss", font=self.font_std)
        rb1.pack(side="left", padx=30, pady=15)
        rb2 = ctk.CTkRadioButton(frame_opts, text="Gauss-Seidel", variable=self.metodo_var, value="Seidel", font=self.font_std)
        rb2.pack(side="left", padx=30, pady=15)

        ctk.CTkButton(tab, text="Calcular Sistema", command=self.calc_sistema, height=60, font=self.font_btn).grid(row=5, column=0, padx=10, pady=20)

        self.out_sis = ctk.CTkTextbox(tab, font=self.font_code)
        self.out_sis.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")

    def calc_sistema(self):
        self.out_sis.delete("0.0", "end")
        try:
            rows = self.txt_A.get("0.0", "end").strip().split('\n')
            A = np.array([list(map(float, row.split())) for row in rows])
            b = np.array(list(map(float, self.entry_b.get().split())))

            if self.metodo_var.get() == "Gauss":
                res = eliminacao_gauss(A, b)
                res_txt = "Falha: Pivô nulo." if res is None else f"Solução (Gauss):\n{res}"
            else:
                res, k, err, msg = gauss_seidel(A, b)
                if "Erro" in msg: res_txt = msg
                else: res_txt = f"{msg}Solução (após {k} iterações):\n{res}\nErro: {err:.2e}"
            self.out_sis.insert("0.0", res_txt)
        except Exception as e:
            self.out_sis.insert("0.0", f"Erro: {e}")

    # --- ABA 2: MÍNIMOS QUADRADOS ---
    def setup_mmq(self):
        tab = self.tab_mmq
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(tab, text="Valores de X:", font=self.font_std).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_x_mmq = ctk.CTkEntry(tab, font=self.font_code, height=40)
        self.ent_x_mmq.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(tab, text="Valores de Y:", font=self.font_std).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_y_mmq = ctk.CTkEntry(tab, font=self.font_code, height=40)
        self.ent_y_mmq.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(tab, text="Modelo:", font=self.font_std).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.combo_mmq = ctk.CTkComboBox(tab, values=["Reta", "Parábola", "Exponencial"], font=self.font_std, height=40, dropdown_font=self.font_std)
        self.combo_mmq.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkButton(tab, text="Ajustar e Plotar", command=self.calc_mmq, height=60, font=self.font_btn).grid(row=3, column=0, columnspan=2, pady=20)

        self.out_mmq = ctk.CTkTextbox(tab, font=self.font_code, height=100)
        self.out_mmq.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.frame_plot = ctk.CTkFrame(tab)
        self.frame_plot.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.canvas_plot = None

    def calc_mmq(self):
        self.out_mmq.delete("0.0", "end")
        if self.canvas_plot:
            self.canvas_plot.get_tk_widget().destroy()
            self.canvas_plot = None

        try:
            x_raw = list(map(float, self.ent_x_mmq.get().split()))
            y_raw = list(map(float, self.ent_y_mmq.get().split()))
            
            if len(x_raw) != len(y_raw):
                raise ValueError("X e Y devem ter o mesmo tamanho.")

            eq_txt, func_plot, erro = minimos_quadrados(x_raw, y_raw, self.combo_mmq.get())

            if func_plot is None:
                self.out_mmq.insert("0.0", eq_txt)
                return

            self.out_mmq.insert("0.0", f"Modelo: {self.combo_mmq.get()}\n{eq_txt}\nErro Quad: {erro:.6f}")

            # Plotagem
            fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
            fig.patch.set_facecolor('#2b2b2b')
            ax.set_facecolor('#333333')
            
            # Fontes do Gráfico
            ax.tick_params(axis='x', colors='white', labelsize=12)
            ax.tick_params(axis='y', colors='white', labelsize=12)
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            
            for spine in ax.spines.values(): spine.set_edgecolor('white')

            x_min, x_max = min(x_raw), max(x_raw)
            margin = (x_max - x_min) * 0.1 if x_max != x_min else 1.0
            x_line = np.linspace(x_min - margin, x_max + margin, 100)
            y_line = func_plot(x_line)

            ax.plot(x_raw, y_raw, 'ro', label='Dados', markersize=8) # Pontos maiores
            ax.plot(x_line, y_line, 'c-', linewidth=3, label='Ajuste') # Linha mais grossa
            
            ax.set_title(f"Ajuste: {self.combo_mmq.get()}", color='white', fontsize=16, weight='bold')
            ax.legend(facecolor='#333333', edgecolor='white', labelcolor='white', fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.3)

            self.canvas_plot = FigureCanvasTkAgg(fig, master=self.frame_plot)
            self.canvas_plot.draw()
            self.canvas_plot.get_tk_widget().pack(fill="both", expand=True)
            plt.close(fig)

        except Exception as e:
            self.out_mmq.insert("0.0", f"Erro: {e}")

    # --- ABA 3: INTEGRAÇÃO ---
    def setup_integracao(self):
        tab = self.tab_int
        tab.grid_columnconfigure(1, weight=1)

        self.mode_int = ctk.StringVar(value="func")
        frame_mode = ctk.CTkFrame(tab)
        frame_mode.grid(row=0, column=0, columnspan=2, padx=10, pady=15, sticky="ew")
        
        rb1 = ctk.CTkRadioButton(frame_mode, text="Usar Função f(x)", variable=self.mode_int, value="func", command=self.toggle_int, font=self.font_std)
        rb1.pack(side="left", padx=40, pady=15)
        rb2 = ctk.CTkRadioButton(frame_mode, text="Usar Tabela (Pontos)", variable=self.mode_int, value="tab", command=self.toggle_int, font=self.font_std)
        rb2.pack(side="left", padx=40, pady=15)

        # Frame Função
        self.fr_func = ctk.CTkFrame(tab)
        self.fr_func.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.fr_func, text="Função f(x):", font=self.font_std).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_func = ctk.CTkEntry(self.fr_func, placeholder_text="Ex: x**2 + np.sin(x)", width=400, font=self.font_code, height=40)
        self.ent_func.grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(self.fr_func, text="[a, b]:", font=self.font_std).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_lim = ctk.CTkEntry(self.fr_func, placeholder_text="0 1", font=self.font_code, height=40)
        self.ent_lim.grid(row=1, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(self.fr_func, text="Subintervalos (n):", font=self.font_std).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.ent_n = ctk.CTkEntry(self.fr_func, placeholder_text="10", font=self.font_code, height=40)
        self.ent_n.grid(row=2, column=1, padx=10, pady=10)

        # Frame Tabela
        self.fr_tab = ctk.CTkFrame(tab)
        ctk.CTkLabel(self.fr_tab, text="X (espaço):", font=self.font_std).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_xtab = ctk.CTkEntry(self.fr_tab, width=400, font=self.font_code, height=40)
        self.ent_xtab.grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(self.fr_tab, text="Y (espaço):", font=self.font_std).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_ytab = ctk.CTkEntry(self.fr_tab, width=400, font=self.font_code, height=40)
        self.ent_ytab.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkButton(tab, text="Integrar", command=self.calc_int, height=60, font=self.font_btn).grid(row=3, column=0, columnspan=2, pady=30)
        
        self.out_int = ctk.CTkTextbox(tab, font=self.font_code, height=150)
        self.out_int.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def toggle_int(self):
        if self.mode_int.get() == "func":
            self.fr_tab.grid_forget()
            self.fr_func.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        else:
            self.fr_func.grid_forget()
            self.fr_tab.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def calc_int(self):
        self.out_int.delete("0.0", "end")
        try:
            if self.mode_int.get() == "func":
                ab = list(map(float, self.ent_lim.get().split()))
                t, s, err = integrar_numerico("func", None, self.ent_func.get(), ab[0], ab[1], int(self.ent_n.get()))
            else:
                x = list(map(float, self.ent_xtab.get().split()))
                y = list(map(float, self.ent_ytab.get().split()))
                if len(x) < 2: raise ValueError("Poucos pontos.")
                t, s, err = integrar_numerico("tab", {'y': y, 'h': x[1]-x[0]})

            if err: self.out_int.insert("0.0", err)
            else:
                simp_txt = f"{s:.6f}" if s is not None else "N/A"
                self.out_int.insert("0.0", f"Trapézio: {t:.6f}\nSimpson:  {simp_txt}")

        except Exception as e:
            self.out_int.insert("0.0", f"Erro: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
import numpy as np
import sympy
import sys

def eliminacao_gauss(A, b):
    n = len(b)
    # Criar matriz aumentada
    M = np.hstack((A, b.reshape(-1, 1))).astype(float)

    # Eliminação Progressiva (Escalonamento)
    for i in range(n):
        #se o pivô for zero, o método falha
        if M[i, i] == 0:
            return None # Retorna None para indicar erro
        
        # Zerar elementos abaixo do pivô
        for j in range(i + 1, n):
            fator = M[j, i] / M[i, i]
            M[j, i:] -= fator * M[i, i:]

    # Substituição Retroativa
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        soma = np.dot(M[i, i+1:n], x[i+1:n])
        x[i] = (M[i, n] - soma) / M[i, i]
    
    return x

def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=100):
    n = len(b)
    x = np.zeros(n) if x0 is None else x0
    
    # Apenas aviso sobre convergência
    diag = np.abs(np.diag(A))
    soma_linhas = np.sum(np.abs(A), axis=1) - diag
    if not np.all(diag > soma_linhas):
        print("AVISO: A matriz não é estritamente diagonal dominante.")

    for k in range(max_iter):
        x_old = x.copy()
        for i in range(n):
            s1 = np.dot(A[i, :i], x[:i])
            s2 = np.dot(A[i, i+1:], x_old[i+1:])
            x[i] = (b[i] - s1 - s2) / A[i, i]
        
        erro = np.linalg.norm(x - x_old, ord=np.inf) / np.linalg.norm(x, ord=np.inf)
        if erro < tol:
            return x, k+1, erro
            
    return x, max_iter, erro

def minimos_quadrados(x, y, tipo):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    n = len(x)
    erro_quadratico = 0.0

    if tipo == 1: # Reta
        A = np.vstack([x, np.ones(n)]).T
        a, b = np.linalg.lstsq(A, y, rcond=None)[0]
        
        # Calcular erro: soma((y_real - y_calculado)^2)
        y_calc = a * x + b
        erro_quadratico = np.sum((y - y_calc)**2)
        
        return f"y = {a:.4f}x + {b:.4f}", lambda val: a*val + b, erro_quadratico

    elif tipo == 2: # Parábola
        A = np.vstack([x**2, x, np.ones(n)]).T
        a, b, c = np.linalg.lstsq(A, y, rcond=None)[0]
        
        y_calc = a * (x**2) + b * x + c
        erro_quadratico = np.sum((y - y_calc)**2)
        
        return f"y = {a:.4f}x² + {b:.4f}x + {c:.4f}", lambda val: a*(val**2) + b*val + c, erro_quadratico

    elif tipo == 3: # Exponencial
        if np.any(y <= 0): return "Erro: Y deve ser positivo.", None, 0
        Y_ln = np.log(y)
        A_mat = np.vstack([x, np.ones(n)]).T
        B_calc, A_calc = np.linalg.lstsq(A_mat, Y_ln, rcond=None)[0]
        a_final = np.exp(A_calc)
        b_final = B_calc # O b da equação linearizada é o b da exponencial
        
        y_calc = a_final * np.exp(b_final * x)
        erro_quadratico = np.sum((y - y_calc)**2)
        
        return f"y = {a_final:.4f} * e^({b_final:.4f}x)", lambda val: a_final * np.exp(b_final * val), erro_quadratico

def trapezio_repetido(y, h):
    n = len(y) - 1
    soma = y[0] + y[-1]
    soma += 2 * sum(y[1:-1]) 
    return (h / 2) * soma

def simpson_repetido(y, h):
    n = len(y) - 1
    if n % 2 != 0: return None
    soma = y[0] + y[-1]
    soma += 4 * sum(y[1:n:2])
    soma += 2 * sum(y[2:n:2]) 
    return (h / 3) * soma

def main():
    while True:
        print("\n" + "="*40)
        print("   PROJETO UNIDADE 2 - MÉTODOS NUMÉRICOS")
        print("="*40)
        print("1. Sistemas Lineares (Gauss Simples)")
        print("2. Sistemas Lineares (Gauss-Seidel)")
        print("3. Mínimos Quadrados (Reta, Parábola, Exp)")
        print("4. Integração (Trapézio + Simpson)")
        print("0. Sair")
        print("-" * 40)
        
        opcao = input("Escolha: ")

        if opcao == '0': break

        if opcao in ['1', '2']:
            try:
                n = int(input("\nDimensão (n): "))
                print("Matriz A (elementos separados por espaço):")
                A = np.array([list(map(float, input(f"Linha {i+1}: ").split())) for i in range(n)])
                b = np.array(list(map(float, input("Vetor b: ").split())))

                if opcao == '1':
                    res = eliminacao_gauss(A, b)
                    if res is None:
                        print("\nERRO: Pivô nulo encontrado (Gauss simples falhou).")
                    else:
                        print(f"\nSOLUÇÃO (Gauss): {res}")
                else:
                    tol = float(input("Tolerância (ex: 1e-6): ") or 1e-6)
                    it = int(input("Máx Iterações: ") or 100)
                    res, k, err = gauss_seidel(A, b, tol=tol, max_iter=it)
                    print(f"\nSOLUÇÃO (Gauss-Seidel): {res}")
                    print(f"Iterações: {k} | Erro: {err:.2e}")
            except Exception as e: print(f"Erro: {e}")

        elif opcao == '3':
            try:
                print("\nDigite os valores de X (separados por espaço):")
                x_input = list(map(float, input().split()))
                print("Digite os valores de Y (separados por espaço):")
                y_input = list(map(float, input().split()))
                
                print("\nEscolha o modelo:")
                print("1. Reta (Linear)")
                print("2. Parábola (Polinomial grau 2)")
                print("3. Exponencial")
                tipo = int(input("Opção: "))
                
                eq_str, func, erro = minimos_quadrados(x_input, y_input, tipo)
                print(f"\n>>> Equação Ajustada: {eq_str}")
                print(f">>> Erro Quadrático Total: {erro:.6f}")
                
            except Exception as e:
                print(f"Erro no ajuste: {e}")

        elif opcao == '4':
            try:
                print("\n--- Integração Numérica ---")
                modo = input("Modo: (1) Função ou (2) Tabela de Pontos? ")
                
                y_vals = []
                h = 0.0
                
                if modo == '1': # Modo Função
                    expr = input("Digite a função f(x): ")
                    x_sym = sympy.symbols('x')
                    f = sympy.lambdify(x_sym, sympy.parse_expr(expr), 'math')
                    a = float(input("a: "))
                    b = float(input("b: "))
                    n = int(input("n: "))
                    h = (b - a) / n
                    y_vals = [f(a + i*h) for i in range(n + 1)]
                    
                elif modo == '2': # Modo Tabela
                    print("Digite os valores de X separados por espaço:")
                    x_vals = list(map(float, input().split()))
                    print("Digite os valores de Y (ou larguras) separados por espaço:")
                    y_vals = list(map(float, input().split()))
                    
                    if len(x_vals) != len(y_vals):
                        print("ERRO: Quantidade de X e Y deve ser igual.")
                        continue
                    if len(x_vals) < 2:
                        print("ERRO: Precisa de pelo menos 2 pontos.")
                        continue

                    # CÁLCULO AUTOMÁTICO DO PASSO
                    h = x_vals[1] - x_vals[0]
                    print(f"--> Passo calculado (h): {h}")
                
                else:
                    print("Modo inválido.")
                    continue

                res_trap = trapezio_repetido(y_vals, h)
                res_simp = simpson_repetido(y_vals, h)
                
                print(f"\n>>> Trapézio Repetido: {res_trap:.6f}")
                if res_simp is None:
                    print(">>> Simpson Repetido: Não aplicável (n ímpar/lista par).")
                else:
                    print(f">>> Simpson Repetido: {res_simp:.6f}")

            except Exception as e:
                print(f"Erro: {e}")

if __name__ == "__main__":
    main()
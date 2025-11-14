Markdown# 🧮 Projeto de Cálculo Numérico - Unidade 2

Este repositório contém uma aplicação em Python desenvolvida para a disciplina de Cálculo Numérico. O software funciona como uma calculadora de métodos numéricos via linha de comando (CLI), focada na resolução de Sistemas Lineares, Ajuste de Curvas e Integração Numérica.

## 🚀 Funcionalidades

O programa aborda os quatro tópicos principais da Unidade 2:

### 1. Sistemas Lineares (Método Direto)
* **Método:** Eliminação de Gauss Simples.
* **Aplicação:** Resolução de sistemas $Ax = b$ de qualquer dimensão.

### 2. Sistemas Lineares (Método Iterativo)
* **Método:** Gauss-Seidel.
* **Funcionalidades:**
    * Verificação de critério de convergência (Diagonal Dominante).
    * Definição de tolerância ($\epsilon$) e número máximo de iterações.

### 3. Mínimos Quadrados (Ajuste de Curvas)
* Realiza a regressão para três modelos matemáticos:
    * **Reta:** $y = ax + b$
    * **Parábola:** $y = ax^2 + bx + c$
    * **Exponencial:** $y = a \cdot e^{bx}$ (via linearização)
* **Diferencial:** Calcula e exibe o **Erro Quadrático Total** para facilitar a escolha do melhor modelo.

### 4. Integração Numérica
* **Métodos:**
    * Regra do Trapézio Repetida.
    * Regra de Simpson 1/3 Repetida.
* **Modos de Entrada:**
    * **Por Função:** O usuário digita a função $f(x)$ (ex: `x**2 + 1`), os limites e o número de subintervalos.
    * **Por Tabela:** O usuário insere uma lista de pontos experimentais. O programa **calcula o passo ($h$) automaticamente** e aplica as regras de integração.

---

## 📦 Pré-requisitos

Para executar este projeto, você precisará do Python instalado e das seguintes bibliotecas:

* `numpy` (para manipulação de matrizes e arrays)
* `sympy` (para interpretação de expressões matemáticas)

### Instalação

Abra o terminal e execute:

```bash
pip install numpy sympy
🛠️ Como ExecutarClone este repositório:Bashgit clone [https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git](https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git)
Acesse a pasta do projeto:Bashcd NOME-DO-REPOSITORIO
Execute o script principal:Bashpython Projeto_Unidade2.py
📖 Guia de Uso RápidoAo iniciar o programa, escolha uma das opções do menu:Opção 1 e 2 (Sistemas Lineares)Digite a matriz linha por linha, separando os números por espaço.Exemplo: Para uma matriz $2 \times 2$:Plaintext2 1
1 4
Opção 3 (Mínimos Quadrados)Digite todos os valores de $X$ em uma linha e todos os valores de $Y$ na próxima.Exemplo:PlaintextX: 0 1.5 2.6 4.2
Y: 18 13 11 9
Opção 4 (Integração)Modo Função: Digite usando sintaxe Python (ex: exp(x), sin(x), x**3).Modo Tabela: Insira os valores de $X$ e $Y$. O programa detecta o espaçamento ($h$) automaticamente.

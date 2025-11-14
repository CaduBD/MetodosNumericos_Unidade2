🧮 Projeto de Cálculo Numérico - Unidade 2

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

🛠️ Como Executar
Execute o script principal:python Projeto_Unidade2.py

📖 Guia de Uso Rápido
Ao iniciar o programa, escolha uma das opções do menu: 
Opção 1 e 2 (Sistemas Lineares)
   Digite a matriz linha por linha, separando os números por espaço. Exemplo: Para uma matriz de dimensão 2 -->
   linha1: 1 2
   linha 2: 4 3
   Após isso, o programa irá pedir o vetor b, digite os resultados da matriz. Exemplo: 
   vetor b: 5 6
Opção 3 (Mínimos Quadrados)
   Digite todos os valores de X em uma linha e todos os valores de Y na próxima. Exemplo: 
   X: 0 1.5 2.6 4.2
   Y: 18 13 11 9
   Após isso, escolhe o modelo.
Opção 4 (Integração)
   Modo Função: Digite usando sintaxe Python (ex: exp(x), sin(x), x**3).
   Modo Tabela: Insira os valores de X e Y. 
   O programa detecta o passo (h) automaticamente.

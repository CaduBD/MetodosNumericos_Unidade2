# 🖥️ Calculadora de Métodos Numéricos (GUI)

Este repositório contém uma aplicação desktop desenvolvida em Python para a disciplina de Cálculo Numérico. O software oferece uma interface gráfica moderna (baseada em `customtkinter`) para resolver problemas complexos de engenharia e matemática.

## ✨ Funcionalidades

A aplicação é dividida em três módulos principais:

### 1. 🧮 Sistemas Lineares
Resolução de sistemas do tipo $Ax = b$.
* **Método Direto:** Eliminação de Gauss Simples.
* **Método Iterativo:** Gauss-Seidel.
    * *Recursos:* Detecção automática de matriz diagonal dominante, configuração de tolerância ($\epsilon$) e número máximo de iterações.
    * *Entrada:* Matrizes inseridas via caixa de texto (copiar e colar facilitado).

### 2. 📈 Mínimos Quadrados (Ajuste de Curvas)
Encontra a melhor curva que se ajusta a um conjunto de dados experimentais.
* **Modelos Suportados:**
    * Reta ($y = ax + b$)
    * Parábola ($y = ax^2 + bx + c$)
    * Exponencial ($y = a \cdot e^{bx}$)
* **Visualização:** Gera um **gráfico interativo** (matplotlib) mostrando os pontos dados e a curva ajustada.
* **Métrica:** Exibe a equação final e o Erro Quadrático Total.

### 3. ∫ Integração Numérica
Calcula integrais definidas usando métodos repetidos.
* **Métodos:**
    * Regra do Trapézio Repetida.
    * Regra de Simpson 1/3 Repetida.
* **Modos de Entrada Flexíveis:**
    1.  **Por Função:** Digite a expressão (ex: `x**2 + sin(x)`) e os limites.
    2.  **Por Tabela:** Insira listas de pontos $X$ e $Y$ (ideal para dados de campo, como larguras de rios).

---

## 📦 Dependências e Instalação

Este projeto utiliza bibliotecas externas para a interface gráfica, cálculos matemáticos e plotagem.

### Pré-requisitos
Certifique-se de ter o Python instalado. Em seguida, instale as dependências:

```bash
pip install customtkinter numpy sympy matplotlib
```
### customtkinter: Para a interface gráfica moderna.

### numpy: Para operações matriciais e vetoriais.

### sympy: Para interpretação simbólica de funções matemáticas.

### matplotlib: Para geração dos gráficos de ajuste de curvas.


🚀 Como Executar
1. Clone este repositório:
   ```
   git clone https://github.com/CaduBD/MetodosNumericos_Unidade2.git
   ```
3. Acesse a pasta do projeto:
    ```
   cd NOME-DO-REPOSITORIO
   ```
5. Execute o arquivo principal:
   ```
   python Projeto_Unidade2.py
   ```

### 📖 Guia de Uso
# Aba 1: Sistemas Lineares

Insira a Matriz A linha por linha. Exemplo para 3x3:
```
3 2 4
1 1 2
4 3 2
```
Insira o vetor b com números separados por espaço: ```1 2 3 ```.

Escolha o método e clique em Calcular.

# Aba 2: Mínimos Quadrados
Insira os valores de X e Y separados por espaço.

Selecione o modelo (Reta, Parábola ou Exponencial).

Clique em Ajustar e Plotar para ver o resultado numérico e o gráfico.

# Aba 3: Integração
Escolha entre Usar Função (para expressões matemáticas) ou Usar Tabela (para dados discretos).

Preencha os campos e clique em Integrar.

# ✒️ Autores
Projeto desenvolvido pela equipe:

   Carlos Eduardo Batista Diniz

   Thalles Inacio Araujo

   Raimundo Ferreira do Nascimento Junior

# Nota: Projeto desenvolvido para a Unidade 2 da disciplina de Cálculo Numérico (2025.2).

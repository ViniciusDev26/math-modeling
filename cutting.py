from ortools.linear_solver import pywraplp
from read_txt_file import read_txt_file

# valores -> lista dos tamanhos de cada tipo de item
# valor_maximo -> tamanho da barra (a soma das combinações não pode ultrapassar)
# menor_valor -> menor tamanho da lista "valores" -> valor da restrição 
# combinacao_atual-> uma lista com as combinação de itens atuais
# inicio -> indice de inicio
# resultados -> lista vazia que armazenará todos os resultados válidos 

# Função que calcula as combinações válidas (a restrição de soma máxima e a diferença mínima)
def explorar_combinacoes(valores, valor_maximo, menor_valor, combinacao_atual, inicio, resultados):
    soma_atual = sum(combinacao_atual)

    if soma_atual <= valor_maximo and (valor_maximo - soma_atual) < menor_valor:
        padrao = []
        # conta quantas vezes cada tamanho apareceu naquele padrão
        for valor in valores:
            padrao.append(combinacao_atual.count(valor))
        resultados.append(padrao)
    # se a soma ultrapassar o valor máximo, para e o padrão não é adicionado aos resultados   
    elif soma_atual > valor_maximo:
        return

    # se não, continuamos a adicionar elementos para formar novas combinações
    for i in range(inicio, len(valores)):
        combinacao_atual.append(valores[i])
        explorar_combinacoes(valores, valor_maximo, menor_valor, combinacao_atual, i, resultados)
        combinacao_atual.pop()  # Remove o último elemento para explorar outras combinações

# valores -> lista dos tamanhos de cada tipo de item
# valor_maximo -> tamanho da barra (a soma das combinações não pode ultrapassar)

# função gerdora das combinações válidas 
def encontrar_combinacoes_soma_maxima(valores, valor_maximo):
    resultados = []
    menor_valor = min(valores)  # menor tamanho da lista "valores" -> valor da restrição

    # calcula as combinações
    explorar_combinacoes(valores, valor_maximo, menor_valor, [], 0, resultados)
    return resultados

# comprimento_barra -> comprimento máximo da barra.
# tamanhos_itens -> lista de tamanhos de itens.
# quantidades_itens -> lista de quantidades demandadas de cada item.

# Função main
def minimizar_desperdicio(comprimento_barra, tamanhos_itens, quantidades_itens):
    padroes = encontrar_combinacoes_soma_maxima(tamanhos_itens, comprimento_barra)
    desperdicio_por_padrao = []
    for padrao in padroes:
        comprimento_utilizado = 0
        for i in range(len(tamanhos_itens)):
            comprimento_utilizado += padrao[i] * tamanhos_itens[i]
        desperdicio_por_padrao.append(comprimento_barra - comprimento_utilizado)

    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Declara as variáveis de decisão
    variaveis_decisao = []
    for j in range(len(padroes)):
        variavel = solver.IntVar(0, solver.infinity(), f'x[{j}]')
        variaveis_decisao.append(variavel)

    # Declara a função objetivo com SetCoefficient
    funcao_objetivo = solver.Objective()
    for j in range(len(padroes)):
        funcao_objetivo.SetCoefficient(variaveis_decisao[j], desperdicio_por_padrao[j])
    funcao_objetivo.SetMinimization()

    # Declara as restrições para atender à demanda de cada tipo de item com SetCoefficient e SetConstraint
    for i in range(len(tamanhos_itens)):
        restricao = solver.Constraint(quantidades_itens[i], solver.infinity())
        for j in range(len(padroes)):
            restricao.SetCoefficient(variaveis_decisao[j], padroes[j][i])

    # Resolve o modelo
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        desperdicio_total = 0
        for j in range(len(padroes)):
            quantidade_usada = variaveis_decisao[j].solution_value()
            desperdicio_padrao = desperdicio_por_padrao[j] * quantidade_usada
            desperdicio_total += desperdicio_padrao
        print('Desperdício total: ', desperdicio_total)

        print('Padrões de corte utilizados:')
        for j in range(len(padroes)):
            quantidade_usada = int(variaveis_decisao[j].solution_value())
            print(f'Padrão {j + 1}: {padroes[j]}, usado {quantidade_usada} vezes')
    else:
        print('Modelo sem solução ótima.')
    print(solver.ExportModelAsLpFormat(False))

input_file = read_txt_file("input-cutting.txt")

#  Coletando entradas do usuário
[comprimento_barra] = input_file[0]
[quantidade_tipos_itens] = input_file[1]

# Leitura dos tamanhos dos itens em uma única linha
tamanhos_itens = input_file[2]

# Leitura das quantidades necessárias em uma única linha
quantidades_itens = input_file[3]

# Validação peba
if len(tamanhos_itens) != quantidade_tipos_itens or len(quantidades_itens) != quantidade_tipos_itens:
    print("Erro: A quantidade de tipos de itens não corresponde ao número de tamanhos e quantidades informados.")
else:
    minimizar_desperdicio(comprimento_barra, tamanhos_itens, quantidades_itens)
from ortools.linear_solver import pywraplp
from read_txt_file import read_txt_file

# leitura de dados
input_file = read_txt_file("input.txt")

# gravar saída de dados
def write_output(message, file):
    file.write(message + "\n")

# criação do arquivo de saída
file = open("output.txt", "w")

# função para resolução do problema de transporte genérico
def problema_transporte():
    [qtd_origens, qtd_destinos] = input_file[0]
    qtd_producoes = input_file[1]
    qtd_demandas = input_file[2]
    custos = input_file[3:]

    # totais de produção e demanda para verificação de balanceamento
    tot_producoes = sum(qtd_producoes)
    tot_demandas = sum(qtd_demandas)

    # balanceamento do modelo
    if tot_producoes > tot_demandas:
        # produção > demanda -> + destino fictício
        demanda_ficticia = tot_producoes - tot_demandas
        qtd_demandas.append(demanda_ficticia)
        qtd_destinos += 1
        for i in range(qtd_origens):
            custos[i].append(0)

    elif tot_demandas > tot_producoes:
        # demanda > produção -> + origem fictícia
        producao_ficticia = tot_demandas - tot_producoes
        qtd_producoes.append(producao_ficticia)
        qtd_origens += 1
        custos.append([0 for j in range(qtd_destinos)])

    # declara o solver: se PLI, usa-se SCIP; se PL, usa-se GLOP.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # declara um número muito grande caso seja necessário usar no modelo
    infinity = solver.infinity()

    # declara as variáveis do modelo: IntVar para inteira; NumVar para fracionárias; BoolVar para binárias.
    x = []
    for i in range(qtd_origens):
        row = []
        for j in range(qtd_destinos):
            row.append(solver.IntVar(0, infinity, f'x{i+1}{j+1}'))
        x.append(row)

    # declaração de restrições de produção
    for i in range(qtd_origens):
        constraint = solver.RowConstraint(0, qtd_producoes[i], f'linha_prod_{i+1}')
        for j in range(qtd_destinos):
            constraint.SetCoefficient(x[i][j], 1)

    # declaração de restrições de demanda
    for j in range(qtd_destinos):
        constraint = solver.RowConstraint(qtd_demandas[j], qtd_demandas[j], f'linha_dem_{j+1}')
        for i in range(qtd_origens):
            constraint.SetCoefficient(x[i][j], 1)

    # declara a função objetivo (min)
    objective = solver.Objective()
    for i in range(qtd_origens):
        for j in range(qtd_destinos):
            objective.SetCoefficient(x[i][j], custos[i][j])
    objective.SetMinimization()

    # resolve o modelo
    status = solver.Solve()

    # verifica se a solução é ótima e, caso seja, exibe ela
    if status == pywraplp.Solver.OPTIMAL:
        write_output('Política de transporte:', file)
        for i in range(qtd_origens):
            for j in range(qtd_destinos):
                if x[i][j].solution_value() > 0:
                    write_output(f'Transporte de {x[i][j].solution_value()} unidades da origem {i + 1} para o destino {j + 1}.', file)
        write_output(f'Custo mínimo = {solver.Objective().Value()}', file)
    else:
        write_output('Modelo sem solução ótima.', file)
    
    # exibe o modelo
    print(solver.ExportModelAsLpFormat(False))


# Chamar a função para resolver o problema
problema_transporte()



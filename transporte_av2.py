import numpy as np
from ortools.linear_solver import pywraplp
from read_txt_file import read_txt_file

input_file = read_txt_file("input.txt")
file = open("output.txt", "w")
def write_output(message):
    file.write(message + "\n")

def problema_transporte():
    # Leitura do arquivo de entrada:
    [num_origens, num_destinos] = input_file[0]
    producoes = input_file[1]
    demandas = input_file[2]
    custos = []
    for i in range(3, len(input_file)):
        custos.append(input_file[i])

    # Total da produção e demanda para verificar se o problema está balanceado
    total_producao = sum(producoes)
    total_demanda = sum(demandas)

    # Verificar se o problema está balanceado ou não
    if total_producao > total_demanda:
        # Desbalanceado: produção > demanda -> + destino fictício
        demandas.append(total_producao - total_demanda)
        custos = np.hstack((custos, np.zeros((len(custos), 1))))
    elif total_demanda > total_producao:
        # Desbalanceado: demanda > produção -> + origem fictícia
        producoes.append(total_demanda - total_producao)
        custos = np.vstack((custos, np.zeros((1, len(custos[0])))))

    # Declaração do solver: se PLI, usa-se SCIP; se PL, usa-se GLOP. (?)
    solver = pywraplp.Solver.CreateSolver('GLOP')

    # Declaração das variáveis de decisão
    x = {}
    for i in range(num_origens):
        for j in range(num_destinos):
            x[(i, j)] = solver.IntVar(0, solver.infinity(), f'x[{i},{j}]')

    # Função objetivo: minimizar o custo total de transporte
    solver.Minimize(solver.Sum(custos[i, j] * x[(i, j)] for i in range(num_origens) for j in range(num_destinos)))

    # Restrições de produção
    for i in range(num_origens):
        solver.Add(solver.Sum(x[(i, j)] for j in range(num_destinos)) <= producoes[i])

    # Restrições de demanda
    for j in range(num_destinos):
        solver.Add(solver.Sum(x[(i, j)] for i in range(num_origens)) >= demandas[j])

    # Resolver o modelo
    status = solver.Solve()

    # Verifica se a solução é ótima e, caso seja, exibe ela
    if status == pywraplp.Solver.OPTIMAL:
        write_output('Solução ótima encontrada!')
        for i in range(num_origens):
            for j in range(num_destinos):
                if x[(i, j)].solution_value() > 0:
                    message = f'Transporte de {x[(i, j)].solution_value()} unidades da origem {i + 1} para o destino {j + 1}.'
                    write_output(message)
    else:
        print('Modelo sem solução ótima.')


# Executar o modelo
problema_transporte()

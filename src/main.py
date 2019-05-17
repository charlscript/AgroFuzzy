# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import os
import numpy as np
import skfuzzy as fuzz
import time
import json
from skfuzzy import control as ctrl


def main():
    comeco = time.time()  # gravar execução
    current_file_path = __file__
    current_file_dir = os.path.dirname(__file__)
    dataset_path = os.path.join(
        current_file_dir, "dataset", "precipitacao.json")

    # Definição dos controllers fuzzy
    chuva = ctrl.Antecedent(np.arange(0, 51, 1), 'chuva')
    temperatura = ctrl.Antecedent(np.arange(0, 51, 1), 'temperatura')
    crescimento = ctrl.Consequent(np.arange(0, 61, 1), 'crescimento')

    # Definição do universo fuzzy
    chuva['baixa'] = fuzz.trimf(chuva.universe, [0, 0, 25])
    chuva['regular'] = fuzz.trimf(chuva.universe, [0, 25, 50])
    chuva['chuvoso'] = fuzz.trimf(chuva.universe, [25, 50, 50])
    temperatura['baixa'] = fuzz.trimf(temperatura.universe, [0, 0, 25])
    temperatura['media'] = fuzz.trimf(temperatura.universe, [0, 25, 50])
    temperatura['alta'] = fuzz.trimf(temperatura.universe, [25, 50, 50])
    crescimento['baixo'] = fuzz.trimf(crescimento.universe, [0, 0, 30])
    crescimento['medio'] = fuzz.trimf(crescimento.universe, [0, 30, 60])
    crescimento['alto'] = fuzz.trimf(crescimento.universe, [30, 60, 60])

    """
    Definição das regras
    
    >Esta planta precisa de calor e frio moderados para se desenvolver de forma saudável, 
    >em climas secos ela tende a não se desenvolver de forma adequada, causando prejuízos ao produtor.
    >https://novonegocio.com.br/rural/plantio-de-soja/
    
    >A soja se adapta melhor às regiões onde as temperaturas oscilam entre 20ºC e 30ºC
    >sendo que a temperatura ideal para seu desenvolvimento está em torno de 30ºC
    >https://www.agencia.cnptia.embrapa.br/gestor/soja/arvore/CONT000fzr67cri02wx5ok0cpoo6aeh331my.html

    1. Se a chuva é baixa e o temperatura é média, então o crescimento será médio
    2. Se o temperatura é média e a chuva regular, então o crescimento será alto
    3. Se o temperatura é alta e a chuva regular, então o crescimento será medio
    4. Se a chuva é baixa e o temperatura baixo, então o crescimento será baixo 
    """

    regra1 = ctrl.Rule(
        chuva['baixa'] & temperatura['media'], crescimento['medio'])
    regra2 = ctrl.Rule(temperatura['media'] &
                       chuva['regular'], crescimento['alto'])
    regra3 = ctrl.Rule(temperatura['alta'] &
                       chuva['regular'], crescimento['medio'])
    regra4 = ctrl.Rule(
        chuva['baixa'] | temperatura['baixa'], crescimento['baixo'])
    fatorCrescimento_ctrl = ctrl.ControlSystem(
        [regra1, regra2, regra3, regra4])
    fatorCrescimento = ctrl.ControlSystemSimulation(fatorCrescimento_ctrl)

    # Leitura e seleção no dataset
    with open(dataset_path, 'r') as ds:
        dataset = json.loads(ds.read())
        escalaReducao = 0.17605633802
        aux = 0
        for i in dataset['meses']:
            fatorCrescimento.input['chuva'] = (
                i['Precipitacao'] * escalaReducao)
            fatorCrescimento.input['temperatura'] = (i['TemperaturaMed'])
            fatorCrescimento.compute()
            if fatorCrescimento.output['crescimento'] > aux:
                precipitacao = (i['Precipitacao'] * escalaReducao)
                temperaturaAux = (i['TemperaturaMed'])
                mes = (i['Mes'])
                aux = fatorCrescimento.output['crescimento']

    fatorCrescimento.input['chuva'] = precipitacao
    fatorCrescimento.input['temperatura'] = temperaturaAux
    fatorCrescimento.compute()

    # saída do terminal
    print("Saída fuzzy/Fator Crescimento: %f " %
          (fatorCrescimento.output['crescimento']))
    print("O melhor mês para o plantio de soja no DF é %s " % (mes))
    fim = time.time()
    tempoTotalFuzzy = fim - comeco
    print("Tempo de execução da função Fuzzy: %f segundos" % (tempoTotalFuzzy))

    # Gráficos
    temperatura.view(sim=fatorCrescimento)
    chuva.view(sim=fatorCrescimento)
    crescimento.view(sim=fatorCrescimento)
    plt.show()


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import time
import json

    
def main():
    comeco = time.time() # gravar execução

    chuva = ctrl.Antecedent(np.arange(0, 11, 1), 'chuva') # Membership de 0 até 1 e range > 11
    temperatura = ctrl.Antecedent(np.arange(0, 11, 1), 'temperatura') # Membership de 0 até 1 e range > 11
    crescimento = ctrl.Consequent(np.arange(0, 26, 1), 'crescimento') # Membership de 0 até 1 e range > 26

    ## Definição da pertinência de cada gráfico fuzzy
    chuva['baixa'] = fuzz.trimf(chuva.universe, [0, 0, 5])
    chuva['regular'] = fuzz.trimf(chuva.universe, [0, 5, 10])
    chuva['chuvoso'] = fuzz.trimf(chuva.universe, [5, 10, 10])

    temperatura['baixa'] = fuzz.trimf(temperatura.universe, [0, 0, 5])
    temperatura['media'] = fuzz.trimf(temperatura.universe, [0, 5, 10])
    temperatura['alta'] = fuzz.trimf(temperatura.universe, [5, 10, 10])

    crescimento['baixo'] = fuzz.trimf(crescimento.universe, [0, 0, 13])
    crescimento['medio'] = fuzz.trimf(crescimento.universe, [0, 13, 25])
    crescimento['alto'] = fuzz.trimf(crescimento.universe, [13, 25, 25])


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

    regra1 = ctrl.Rule(chuva['baixa'] & temperatura['media'], crescimento['medio'])
    regra2 = ctrl.Rule(temperatura['media'] & chuva['regular'], crescimento['alto'])
    regra3 = ctrl.Rule(temperatura['alta'] & chuva['regular'], crescimento['medio'])
    regra4 = ctrl.Rule(chuva['baixa'] | temperatura['baixa'], crescimento['baixo'])

    #regra1.view()  #arvore fuzzy da regra 1


    ## Definição do nosso ControlSystem, com o array contendo as nossas regras
    fatorCrescimento_ctrl = ctrl.ControlSystem([regra1, regra2, regra3, regra4])
    ## Simulação das nossas regras, com os calculos de cada opção
    fatorCrescimento = ctrl.ControlSystemSimulation(fatorCrescimento_ctrl)

    """
    Agora podemos calcular o fator de crescimento simplesmente populando a pertinencia das duas regras de entrada(chuva/temperatura)
    """
    with open('assets/datasets/precipitacao.json') as json_file
    dataset = json.load(json_file)
    for i in dataset['meses']:
        tempIdeal = i['TemperaturaMed']
        
        chuvaPert = dataset
        temperaturaPert = 4.8
        fatorCrescimento.input['chuva'] = chuvaPert
        fatorCrescimento.input['temperatura'] = temperaturaPert
        # Calculo do fator de crescimento
        fatorCrescimento.compute()
        fatorCrescimento.output['crescimento'

    ## Gráficos
    temperatura.view(sim=fatorCrescimento)
    chuva.view(sim=fatorCrescimento)
    crescimento.view(sim=fatorCrescimento)

    ## saída do terminal
    print "Saída fuzzy/Fator Crescimento: %f " % (fatorCrescimento.output['crescimento'])
    fim = time.time()
    tempoTotalFuzzy = fim - comeco
    print "Tempo da função Fuzzy: %f segundos" % (tempoTotalFuzzy)

    ##Janelas
    plt.show()

if __name__ == '__main__':
    main()
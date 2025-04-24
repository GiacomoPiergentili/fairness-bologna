from probability_toolkit import *

def weight_function(age, weights, values):
    costo = 0
    for key in weights[age].keys():
        costo += min(1,max(weights[age][key]*values['vals'][key],0))
    return min(costo, MAX_VAL)

def get_time_probs(key, t):
    """
    per ogni categoria devo stimare la probabilità di attraversare la porta ad un certo orario
    """
    match key:
        case "bambini":
            return children_prob(t)
        case "ragazzi":
            return guys_prob(t)
        case "adulti":
            return man_prob(t)
        case "adulte":
            return woman_prob(t)
from scipy.special import softmax
from probability_toolkit import *

def get_path(door):
    """
    Returns the relative file path to the CSV file containing flow rate data 
    for a specified door.
    """
    path = 'data/doors_flow_rates/'
    match door:
        case 'saragozza':
            path+='varco-n-59-saragozza-direzione-centro.csv'
        case 'san_isaia':
            path+='varco-n-1-s-isaia-direzione-centro.csv'
        case 'san_felice':
            path+='varco-n-1059-san-felice-direzione-centro.csv'
        case 'lame':
            path+='varco-n-55-lame-direzione-centro.csv'
        case 'galliera':
            path+='varco-n-38-indipendenza-direzione-centro.csv'
        case 'mascarella':
            path+='varco-n-53-mascarella-direzione-sud.csv'
        case 'san_donato':
            path+='varco-n-65.csv'
        case 'san_vitale':
            path+='varco-n-2-s-vitale-direzione-centro.csv'
        case 'santo_stefano':
            path+='varco-n-45-pta-santo-stefano-direzione-centro.csv'
        case 'castiglione':
            path+='varco-n-7-viale-xii-giugno-direzione-centro.csv'
    return path

def get_probs(t, probs):
    """
    used to obtain time-adjusted and normalized probabilities 
    for a set of keys at a given time `t`.

    Parameters:
    - t: time reference (e.g., integer or datetime, depending on get_time_probs)
    - probs: dictionary mapping each key (e.g., gate or option name) to a base probability

    Returns:
    - A tuple of two dictionaries:
        1. Time-scaled (but unnormalized) probabilities
        2. Normalized probabilities (softmaxed to sum to 1)
    """
    keys=probs.keys()
    scaled_probs_dict = {key: probs[key] * get_time_probs(key, t) for key in keys}

    # Estrai i valori nell'ordine corretto delle chiavi per la softmax
    scaled_values = [scaled_probs_dict[key] for key in keys]

    # Applica la softmax per far sommare le probabilità a 1
    softmaxed_probs = softmax(scaled_values)
    return scaled_probs_dict, {key:softmaxed_probs[_] for _,key in enumerate(keys)}

def weight_function(age, weights, values):
    """
    Use this function to compute a weighted cost score for a given `age` group,
    based on predefined weights and input values.

    Parameters:
    - age: key used to select the appropriate weight set from the `weights` dictionary
    - weights: a nested dictionary of the form weights[age][key] = weight
    - values: a dictionary with a 'vals' sub-dictionary mapping each key to a value

    Returns:
    - A float representing the total weighted cost, capped at MAX_VAL
    """
    costo = 0
    for key in weights[age].keys():
        costo += min(1,max(weights[age][key]*values['vals'][key],0))
    return min(costo, MAX_VAL)

def get_time_probs(key, t):
    """
    returns the time-dependent probability of a person 
    in category `key` crossing a gate at time `t`.

    Parameters:
    - key: category of the person (e.g., "bambini", "ragazzi", "adulti", "adulte")
    - t: time input used by the corresponding probability function

    Returns:
    - A float representing the probability for the given category at time `t`
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
        case "family":
            return family_prob(t)
"""
data that will be used in the simulation

weights -> represent how much a certain feature influences a certain category
porte_data -> represent features for each door. this is used for the inzialization of our simulator and those are the values that will change in the simulation

"""

# the following is used as example and is not based on real data.
weights = {
  "bambini": {
    "costo ingresso": 0,
    "aree verdi gratuite": -1,
    "aree verdi pagamento": 1,
    "scuole pubbliche": -1,
    "scuole private": -1,
    "servizi": 0,
    "mobilita": -1,
  },
  "ragazzi": {
    "costo ingresso": 1,
    "aree verdi gratuite": -1,
    "aree verdi pagamento": 1,
    "scuole pubbliche": 0,
    "scuole private": 0,
    "servizi": 0,
    "mobilita": -1,
  },
  "adulti": {
    "costo ingresso": 0,
    "aree verdi gratuite": 0,
    "aree verdi pagamento": 1,
    "scuole pubbliche": 0,
    "scuole private": 0,
    "servizi": -1,
    "mobilita": -1,
  },
  "adulte": {
    "costo ingresso": 0,
    "aree verdi gratuite": 0,
    "aree verdi pagamento": 1,
    "scuole pubbliche": -1,
    "scuole private": -1,
    "servizi": 1,
    "mobilita": -1,
  },
  "family": {
    "costo ingresso": 0,
    "aree verdi gratuite": 1,
    "aree verdi pagamento": 1,
    "scuole pubbliche": 1,
    "scuole private": 1,
    "servizi": 1,
    "mobilita": 1,
  }
}

porte_data = {
  "saragozza": {
    "coords": (44.4912005724502, 11.329863207526603),
    "vals": {
      "costo ingresso": 0.5,
      "aree verdi gratuite": -0.5,
      "aree verdi pagamento": 0.5,
      "scuole pubbliche": -0.5,
      "scuole private": -0.5,
      "servizi": -0.5,
      "mobilita": -0.9,
    }
  },
  "san_isaia": {
    "coords": (44.494722736370974, 11.328817848825718),
    "vals": {
      "costo ingresso": 0.5,
      "aree verdi gratuite": -0.5,
      "aree verdi pagamento": 0.5,
      "scuole pubbliche": -0.5,
      "scuole private": -0.5,
      "servizi": -0.5,
      "mobilita": -0.9,
    }
  },
  "san_felice": {
    "coords": (44.49954001528024, 11.327157797268898),
    "vals": {
      "costo ingresso": 0.5,
      "aree verdi gratuite": -0.5,
      "aree verdi pagamento": 0.5,
      "scuole pubbliche": -0.5,
      "scuole private": -0.5,
      "servizi": -0.5,
      "mobilita": -0.9,
    }
  },
  "lame": {
    "coords": (44.50242902355546, 11.333746465890892),
    "vals": {
      "costo ingresso": 0.5,
      "aree verdi gratuite": -0.5,
      "aree verdi pagamento": 0.5,
      "scuole pubbliche": -0.5,
      "scuole private": -0.5,
      "servizi": -0.5,
      "mobilita": -0.9,
    }
  },
  "galliera": {
    "coords": (44.504122308476425, 11.344755553055865),
    "vals": {
      "costo ingresso": 0.5,
      "aree verdi gratuite": -0.5,
      "aree verdi pagamento": 0.5,
      "scuole pubbliche": -0.5,
      "scuole private": -0.5,
      "servizi": -0.5,
      "mobilita": -0.9,
    }
  },
  "mascarella": {
    "coords": (44.502187603690956, 11.353025162795086),
    "vals": {
      "costo ingresso": 0.5,
      "aree verdi gratuite": -0.5,
      "aree verdi pagamento": 0.5,
      "scuole pubbliche": -0.5,
      "scuole private": -0.5,
      "servizi": -0.5,
      "mobilita": -0.9,
    }
  },
  "san_donato": {
    "coords": (44.49842310195063, 11.356597138637024),
    "vals": {
      "costo ingresso": 0.5,
      "aree verdi gratuite": -0.5,
      "aree verdi pagamento": 0.5,
      "scuole pubbliche": -0.5,
      "scuole private": -0.5,
      "servizi": -0.5,
      "mobilita": -0.9,
    }
  },
  "san_vitale": {
    "coords": (44.49409991185012, 11.356588928248431),
    "vals": {
      "costo ingresso": 0.5,
      "aree verdi gratuite": -0.5,
      "aree verdi pagamento": 0.5,
      "scuole pubbliche": -0.5,
      "scuole private": -0.5,
      "servizi": -0.5,
      "mobilita": -0.9,
    }
  },
  # "maggiore": { # dati sul traffico mancanti
  #   "coords": (44.49020940327005, 11.356963780736049),
  #   "vals": {
  #     "costo ingresso": 0.5,
  #     "aree verdi gratuite": -0.5,
  #     "aree verdi pagamento": 0.5,
  #     "scuole pubbliche": -0.5,
  #     "scuole private": -0.5,
  #     "servizi": -0.5,
  #     "mobilita": -0.9,
  #   }
  # },
  # "san_mammolo": { # dati sul traffico mancanti
  #   "coords": (44.48673817372272, 11.338747595243037),
  #   "vals": {
  #     "costo ingresso": 0.5,
  #     "aree verdi gratuite": -0.5,
  #     "aree verdi pagamento": 0.5,
  #     "scuole pubbliche": -0.5,
  #     "scuole private": -0.5,
  #     "servizi": -0.5,
  #     "mobilita": -0.9,
  #   }
  # },
  "santo_stefano": {
    "coords": (44.48473726216725, 11.355507110876715),
    "vals": {
      "costo ingresso": 0.5,
      "aree verdi gratuite": -0.5,
      "aree verdi pagamento": 0.5,
      "scuole pubbliche": -0.5,
      "scuole private": -0.5,
      "servizi": -0.5,
      "mobilita": -0.9,
    }
  },
  "castiglione": {
    "coords": (44.48578661814331, 11.34880944929151),
    "vals": {
      "costo ingresso": 0.5,
      "aree verdi gratuite": -0.5,
      "aree verdi pagamento": 0.5,
      "scuole pubbliche": -0.5,
      "scuole private": -0.5,
      "servizi": -0.5,
      "mobilita": -0.9,
    }
  },
}
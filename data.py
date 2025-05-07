"""
data that will be used in the simulation

weights -> represent how much a certain feature influences a certain category
porte_data -> represent features for each door. this is used for the inzialization of our simulator and those are the values that will change in the simulation

"""

# the following is used as example and is not based on real data.
weights = {
  "bambini": {
    "costo ingresso": 0.8,         # Increased: Economic factors impact family decisions
    "aree verdi gratuite": -1.5,   # Strengthened: Bologna's parks like Giardini Margherita are crucial for children
    "aree verdi pagamento": 0.7,   # Reduced: Less impact than free spaces
    "scuole pubbliche": -1.7,      # Strengthened: Bologna has 90+ schools in central districts
    "scuole private": -0.8,        # Adjusted: Lower density than public schools
    "servizi": -0.5,               # Added importance: Child-friendly services matter
    "mobilita": -1.2,              # Increased: Safety in Bologna's walkable center is key
  },
  "ragazzi": {
    "costo ingresso": -0.8,        # Reduced: Students are price-sensitive but less than families
    "aree verdi gratuite": -1.2,   # Increased: Important social gathering spaces for Bologna's 80,000+ students
    "aree verdi pagamento": 0.6,   # Reduced slightly
    "scuole pubbliche": -1.2,      # Greatly increased: University presence is defining for Bologna
    "scuole private": -0.5,        # Moderately important
    "servizi": -0.8,               # Increased: Student services are critical
    "mobilita": -0.7,              # Reduced: Bologna's compact center is walkable
  },
  "adulte": {
    "costo ingresso": 0.3,         # Added some importance: Economic considerations
    "aree verdi gratuite": -0.5,   # Slightly higher than men (social gathering spaces)
    "aree verdi pagamento": 0.6,   # Reduced impact
    "scuole pubbliche": -1.3,      # Higher: School proximity affects women disproportionately in Italian society
    "scuole private": -0.7,        # Moderate importance
    "servizi": -1.2,               # Increased: Access to services is highly important (Bologna has 53.3% female population)
    "mobilita": -1.4,              # Increased: Safety and accessibility in transportation
  },
  "adulti": {
    "costo ingresso": 0.3,         # Added some importance: Economic considerations
    "aree verdi gratuite": -0.4,   # Moderate importance
    "aree verdi pagamento": 0.6,   # Reduced: Less impactful
    "scuole pubbliche": -0.2,      # Low direct importance for most
    "scuole private": -0.2,        # Low direct importance for most
    "servizi": -0.9,               # Increased: Employment and city services are key
    "mobilita": -1.3,              # Increased: Commuting patterns in Bologna's limited-traffic center
  },
  "family": {
    "costo ingresso": 0.9,         # Added some importance: Economic factor for multiple people
    "aree verdi gratuite": -1.7,   # Increased: Bologna's parks are central to family activities
    "aree verdi pagamento": 1.0,   # Unchanged: Still a barrier
    "scuole pubbliche": -1.8,      # Increased: Critical for family settlement patterns
    "scuole private": -1.0,        # Moderate importance
    "servizi": -1.5,               # Increased: Family services are essential
    "mobilita": -1.2,              # Bologna's limited traffic center affects family transportation
  },
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
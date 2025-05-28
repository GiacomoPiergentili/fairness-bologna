"""
data that will be used in the simulation

weights -> represent how much a certain feature influences a certain category
porte_data -> represent features for each gate. this is used for the initialization of our simulator and those are the values that will change in the simulation

"""

# the following is used as example and is not based on real data.
weights = {
  "kids": {
    "entry cost": 0.8,         # Increased: Economic factors impact family decisions
    "free green areas": -1.5,   # Strengthened: Bologna's parks like Giardini Margherita are crucial for children
    "paid green areas": 0.7,   # Reduced: Less impact than free spaces
    "public schools": -1.7,      # Strengthened: Bologna has 90+ schools in central districts
    "private schools": -0.8,        # Adjusted: Lower density than public schools
    "services": -0.5,               # Added importance: Child-friendly services matter
    "mobility": -1.2,              # Increased: Safety in Bologna's walkable center is key
  },
  "teenagers": {
    "entry cost": -0.8,        # Reduced: Students are price-sensitive but less than families
    "free green areas": -1.2,   # Increased: Important social gathering spaces for Bologna's 80,000+ students
    "paid green areas": 0.6,   # Reduced slightly
    "public schools": -1.2,      # Greatly increased: University presence is defining for Bologna
    "private schools": -0.5,        # Moderately important
    "services": -0.8,               # Increased: Student services are critical
    "mobility": -0.7,              # Reduced: Bologna's compact center is walkable
  },
  "women": {
    "entry cost": 0.3,         # Added some importance: Economic considerations
    "free green areas": -0.5,   # Slightly higher than men (social gathering spaces)
    "paid green areas": 0.6,   # Reduced impact
    "public schools": -1.3,      # Higher: School proximity affects women disproportionately in Italian society
    "private schools": -0.7,        # Moderate importance
    "services": -1.2,               # Increased: Access to services is highly important (Bologna has 53.3% female population)
    "mobility": -1.4,              # Increased: Safety and accessibility in transportation
  },
  "men": {
    "entry cost": 0.3,         # Added some importance: Economic considerations
    "free green areas": -0.4,   # Moderate importance
    "paid green areas": 0.6,   # Reduced: Less impactful
    "public schools": -0.2,      # Low direct importance for most
    "private schools": -0.2,        # Low direct importance for most
    "services": -0.9,               # Increased: Employment and city services are key
    "mobility": -1.3,              # Increased: Commuting patterns in Bologna's limited-traffic center
  },
  "family": {
    "entry cost": 0.9,         # Added some importance: Economic factor for multiple people
    "free green areas": -1.7,   # Increased: Bologna's parks are central to family activities
    "paid green areas": 1.0,   # Unchanged: Still a barrier
    "public schools": -1.8,      # Increased: Critical for family settlement patterns
    "private schools": -1.0,        # Moderate importance
    "services": -1.5,               # Increased: Family services are essential
    "mobility": -1.2,              # Bologna's limited traffic center affects family transportation
  },
  "others": {
    "entry cost": 0.5,         # Moderate importance: Economic factor
    "free green areas": -0.5,   # Moderate importance: Social gathering spaces
    "paid green areas": 0.5,   # Reduced: Less impactful
    "public schools": -0.5,      # Moderate importance: Not a primary factor
    "private schools": -0.5,        # Moderate importance: Not a primary factor
    "services": -0.5,               # Moderate importance: Access to services matters
    "mobility": -0.5,              # Increased: Safety and accessibility in transportation
  }
}

porte_data = { # Changed variable name to match English terminology
  "saragozza": {
    "coords": (44.4912005724502, 11.329863207526603),
    "vals": {
      "entry cost": 0.5,
      "free green areas": -0.5,
      "paid green areas": 0.5,
      "public schools": -0.5,
      "private schools": -0.5,
      "services": -0.5,
      "mobility": -0.9,
    }
  },
  "san_isaia": {
    "coords": (44.494722736370974, 11.328817848825718),
    "vals": {
      "entry cost": 0.5,
      "free green areas": -0.5,
      "paid green areas": 0.5,
      "public schools": -0.5,
      "private schools": -0.5,
      "services": -0.5,
      "mobility": -0.9,
    }
  },
  "san_felice": {
    "coords": (44.49954001528024, 11.327157797268898),
    "vals": {
      "entry cost": 0.5,
      "free green areas": -0.5,
      "paid green areas": 0.5,
      "public schools": -0.5,
      "private schools": -0.5,
      "services": -0.5,
      "mobility": -0.9,
    }
  },
  "lame": {
    "coords": (44.50242902355546, 11.333746465890892),
    "vals": {
      "entry cost": 0.5,
      "free green areas": -0.5,
      "paid green areas": 0.5,
      "public schools": -0.5,
      "private schools": -0.5,
      "services": -0.5,
      "mobility": -0.9,
    }
  },
  "galliera": {
    "coords": (44.504122308476425, 11.344755553055865),
    "vals": {
      "entry cost": 0.5,
      "free green areas": -0.5,
      "paid green areas": 0.5,
      "public schools": -0.5,
      "private schools": -0.5,
      "services": -0.5,
      "mobility": -0.9,
    }
  },
  "mascarella": {
    "coords": (44.502187603690956, 11.353025162795086),
    "vals": {
      "entry cost": 0.5,
      "free green areas": -0.5,
      "paid green areas": 0.5,
      "public schools": -0.5,
      "private schools": -0.5,
      "services": -0.5,
      "mobility": -0.9,
    }
  },
  "san_donato": {
    "coords": (44.49842310195063, 11.356597138637024),
    "vals": {
      "entry cost": 0.5,
      "free green areas": -0.5,
      "paid green areas": 0.5,
      "public schools": -0.5,
      "private schools": -0.5,
      "services": -0.5,
      "mobility": -0.9,
    }
  },
  "san_vitale": {
    "coords": (44.49409991185012, 11.356588928248431),
    "vals": {
      "entry cost": 0.5,
      "free green areas": -0.5,
      "paid green areas": 0.5,
      "public schools": -0.5,
      "private schools": -0.5,
      "services": -0.5,
      "mobility": -0.9,
    }
  },

  # We commented out the following because they are missing traffic data
  # "maggiore": { # traffic data missing
  #   "coords": (44.49020940327005, 11.356963780736049),
  #   "vals": {
  #     "entry cost": 0.5,
  #     "free green areas": -0.5,
  #     "paid green areas": 0.5,
  #     "public schools": -0.5,
  #     "private schools": -0.5,
  #     "services": -0.5,
  #     "mobility": -0.9,
  #   }
  # },
  # "san_mammolo": { # traffic data missing
  #   "coords": (44.48673817372272, 11.338747595243037),
  #   "vals": {
  #     "entry cost": 0.5,
  #     "free green areas": -0.5,
  #     "paid green areas": 0.5,
  #     "public schools": -0.5,
  #     "private schools": -0.5,
  #     "services": -0.5,
  #     "mobility": -0.9,
  #   }
  # },
  "santo_stefano": {
    "coords": (44.48473726216725, 11.355507110876715),
    "vals": {
      "entry cost": 0.5,
      "free green areas": -0.5,
      "paid green areas": 0.5,
      "public schools": -0.5,
      "private schools": -0.5,
      "services": -0.5,
      "mobility": -0.9,
    }
  },
  "castiglione": {
    "coords": (44.48578661814331, 11.34880944929151),
    "vals": {
      "entry cost": 0.5,
      "free green areas": -0.5,
      "paid green areas": 0.5,
      "public schools": -0.5,
      "private schools": -0.5,
      "services": -0.5,
      "mobility": -0.9,
    }
  },
}
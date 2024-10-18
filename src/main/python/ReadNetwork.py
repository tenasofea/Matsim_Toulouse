import matsim
import pandas as pd
import geopandas as gpd
from collections import defaultdict
import matplotlib.pyplot as plt
# Commenter cette ligne dans IntelliJpip install matplotlib geopandas

# %matplotlib inline

# -------------------------------------------------------------------
# 1. NETWORK: Read a MATSim network:
net = matsim.read_network('C:/Users/User/IdeaProjects/matsim-example-project-modified/output/output_network.xml.gz')

# Afficher les noeuds du réseau sous forme de dataframe
print(net.nodes)
# Afficher les liens du réseau sous forme de dataframe
print(net.links)

# Extra: create a Geopandas dataframe with LINESTRINGS for our network
geo = net.as_geo()

# Afficher le réseau dans une fenêtre matplotlib
geo.plot()
plt.show()

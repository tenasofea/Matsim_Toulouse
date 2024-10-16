# -----------------------------------------------------------------------------------------------------------
# Pour extraite des position des agents(par minute) sans la colonne motif - ca marche

# import xml.etree.ElementTree as ET
# import gzip
# from collections import defaultdict

# # Fonction pour lire le fichier réseau et récupérer les coordonnées des nœuds et les liens
# def lire_reseau(fichier_network):
#     coordonnees_noeuds = {}
#     liens = {}
    
#     with gzip.open(fichier_network, 'rt', encoding='utf-8') as f:
#         tree = ET.parse(f)
#         root = tree.getroot()
        
#         # Récupérer les nœuds et leurs coordonnées
#         for node in root.findall('.//node'):
#             node_id = node.get('id')
#             x = float(node.get('x'))
#             y = float(node.get('y'))
#             coordonnees_noeuds[node_id] = (x, y)
        
#         # Récupérer les liens et leurs nœuds de départ et d'arrivée
#         for link in root.findall('.//link'):
#             link_id = link.get('id')
#             from_node = link.get('from')
#             to_node = link.get('to')
#             liens[link_id] = (from_node, to_node)
    
#     return coordonnees_noeuds, liens

# # Fonction pour lire les événements de véhicule et écrire les positions des agents dans un fichier CSV
# def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv):
#     # Lire le réseau pour récupérer les coordonnées des nœuds et les liens
#     coordonnees_noeuds, liens = lire_reseau(fichier_network)
    
#     # Dictionnaire pour stocker les positions des agents à chaque minute
#     positions_par_vehicule = defaultdict(list)
#     dernier_temps_par_vehicule = defaultdict(lambda: -60)  # Dernier temps enregistré pour chaque véhicule (initialisé à -60 pour la première minute)

#     # Ouvrir output_detaillees_car.xml (fichier non gzippé)
#     tree = ET.parse(fichier_events)
#     root = tree.getroot()

#     # Itérer sur tous les éléments "event"
#     for event in root.findall('event'):
#         event_type = event.get('type')
#         vehicle_id = event.get('vehicle')

#         # Se concentrer uniquement sur les événements "entered link" et "left link"
#         if event_type in ['entered link', 'left link']:
#             link_id = event.get('link')
#             time = float(event.get('time'))

#             # Vérifier si ce lien existe dans le réseau
#             if link_id not in liens:
#                 continue  # Si le lien n'existe pas, passer au prochain événement

#             # Récupérer le nœud de départ "from" du lien
#             from_node, _ = liens[link_id]

#             # Récupérer les coordonnées du nœud "from"
#             if from_node in coordonnees_noeuds:
#                 x, y = coordonnees_noeuds[from_node]
#             else:
#                 continue  # Si les coordonnées ne sont pas trouvées, passer au prochain événement

#             # Calculer la prochaine minute à enregistrer
#             if time - dernier_temps_par_vehicule[vehicle_id] >= 60:
#                 # Enregistrer la position pour le véhicule à cette minute
#                 positions_par_vehicule[vehicle_id].append((int(time // 60), x, y))
#                 dernier_temps_par_vehicule[vehicle_id] = time

#     # Écrire le fichier CSV avec les positions des véhicules
#     with open(fichier_sortie_csv, 'w') as f_out:
#         f_out.write("AgentId,Temps_minute,x,y\n")
#         for vehicle_id, positions in positions_par_vehicule.items():
#             # Trier les positions par temps
#             positions_triees = sorted(positions, key=lambda x: x[0])
#             for time_minute, x, y in positions_triees:
#                 f_out.write(f"{vehicle_id},{time_minute},{x},{y}\n")

# # Spécifier les fichiers d'entrée et de sortie
# fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car.xml"
# fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_network.xml.gz"
# fichier_sortie_csv = "agent_positions.csv"

# # Appeler la fonction pour écrire les positions des véhicules dans le fichier CSV
# ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv)

# -----------------------------------------------------------------------------------------------------------
# Pour extraite des position des agents(par minute) avec Motif_Orig & Motif_Dest

import xml.etree.ElementTree as ET
import gzip
from collections import defaultdict

# Fonction pour lire le fichier réseau et récupérer les coordonnées des nœuds et les liens
def lire_reseau(fichier_network):
    coordonnees_noeuds = {}
    liens = {}
    
    with gzip.open(fichier_network, 'rt', encoding='utf-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        
        # Récupérer les nœuds et leurs coordonnées
        for node in root.findall('.//node'):
            node_id = node.get('id')
            x = float(node.get('x'))
            y = float(node.get('y'))
            coordonnees_noeuds[node_id] = (x, y)
        
        # Récupérer les liens et leurs nœuds de départ et d'arrivée
        for link in root.findall('.//link'):
            link_id = link.get('id')
            from_node = link.get('from')
            to_node = link.get('to')
            liens[link_id] = (from_node, to_node)
    
    return coordonnees_noeuds, liens

# Fonction pour lire les événements de véhicule et écrire les positions des agents dans un fichier CSV avec motifs
def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv):
    # Lire le réseau pour récupérer les coordonnées des nœuds et les liens
    coordonnees_noeuds, liens = lire_reseau(fichier_network)
    
    # Dictionnaire pour stocker les positions des agents à chaque minute
    positions_par_vehicule = defaultdict(list)
    dernier_temps_par_vehicule = defaultdict(lambda: -60)  # Dernier temps enregistré pour chaque véhicule (initialisé à -60 pour la première minute)
    
    # Variables to track motifs
    motif_orig = None
    motif_dest = None

    # Ouvrir output_detaillees_car.xml (fichier non gzippé)
    tree = ET.parse(fichier_events)
    root = tree.getroot()

    # Itérer sur tous les éléments "event"
    for event in root.findall('event'):
        event_type = event.get('type')
        vehicle_id = event.get('vehicle')

        # Gérer les événements "actend" pour capturer le motif d'origine
        if event_type == 'actend':
            motif_orig = event.get('actType')  # On retient le motif d'origine
        # Gérer les événements "actstart" pour capturer le motif de destination
        elif event_type == 'actstart':
            motif_dest = event.get('actType')  # On retient le motif de destination

            # Lorsque l'on a à la fois le Motif_Orig et Motif_Dest, on peut écrire les positions correspondantes
            for vehicle, positions in positions_par_vehicule.items():
                # Pour chaque enregistrement déjà accumulé, on associe le motif
                for (time_minute, x, y) in positions:
                    with open(fichier_sortie_csv, 'a') as f_out:
                        f_out.write(f"{vehicle},{time_minute},{x},{y},{motif_orig},{motif_dest}\n")
            positions_par_vehicule.clear()  # Une fois écrit, on efface les positions pour un nouveau trajet

        # Se concentrer uniquement sur les événements "entered link" et "left link"
        if event_type in ['entered link', 'left link']:
            link_id = event.get('link')
            time = float(event.get('time'))

            # Vérifier si ce lien existe dans le réseau
            if link_id not in liens:
                continue  # Si le lien n'existe pas, passer au prochain événement

            # Récupérer le nœud de départ "from" du lien
            from_node, _ = liens[link_id]

            # Récupérer les coordonnées du nœud "from"
            if from_node in coordonnees_noeuds:
                x, y = coordonnees_noeuds[from_node]
            else:
                continue  # Si les coordonnées ne sont pas trouvées, passer au prochain événement

            # Calculer la prochaine minute à enregistrer
            if time - dernier_temps_par_vehicule[vehicle_id] >= 60:
                # Accumuler la position pour le véhicule à cette minute
                positions_par_vehicule[vehicle_id].append((int(time // 60), x, y))
                dernier_temps_par_vehicule[vehicle_id] = time

    # Si des positions restent après la dernière boucle, on les écrit
    if motif_orig and motif_dest:
        for vehicle, positions in positions_par_vehicule.items():
            for (time_minute, x, y) in positions:
                with open(fichier_sortie_csv, 'a') as f_out:
                    f_out.write(f"{vehicle},{time_minute},{x},{y},{motif_orig},{motif_dest}\n")

# Spécifier les fichiers d'entrée et de sortie
fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car.xml"
fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_network.xml.gz"
fichier_sortie_csv = "agent_positions_motif.csv"

# Créer l'en-tête du fichier CSV avant d'écrire
with open(fichier_sortie_csv, 'w') as f_out:
    f_out.write("AgentId,Temps_minute,x,y,Motif_Orig,Motif_Dest\n")

# Appeler la fonction pour écrire les positions des véhicules dans le fichier CSV avec motifs
ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv)

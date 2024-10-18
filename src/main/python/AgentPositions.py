# -----------------------------------------------------------------------------------------------------------
# Pour extraite des position des agents(par minute) sans la colonne motif - ca marche

# import xml.etree.ElementTree as ET
# import gzip
# from collections import defaultdict

# def lire_reseau(fichier_network):
#     coordonnees_noeuds = {}
#     liens = {}
    
#     with gzip.open(fichier_network, 'rt', encoding='utf-8') as f:
#         tree = ET.parse(f)
#         root = tree.getroot()
        
#         for node in root.findall('.//node'):
#             node_id = node.get('id')
#             x = float(node.get('x'))
#             y = float(node.get('y'))
#             coordonnees_noeuds[node_id] = (x, y)
        
#         for link in root.findall('.//link'):
#             link_id = link.get('id')
#             from_node = link.get('from')
#             to_node = link.get('to')
#             liens[link_id] = (from_node, to_node)
    
#     return coordonnees_noeuds, liens

# def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv):
#     coordonnees_noeuds, liens = lire_reseau(fichier_network)
#     positions_par_vehicule = defaultdict(list)
#     dernier_temps_par_vehicule = defaultdict(lambda: -60)  

#     tree = ET.parse(fichier_events)
#     root = tree.getroot()

#     for event in root.findall('event'):
#         event_type = event.get('type')
#         vehicle_id = event.get('vehicle')

#         if event_type in ['entered link', 'left link']:
#             link_id = event.get('link')
#             time = float(event.get('time'))

#             if link_id not in liens:
#                 continue  

#             from_node, _ = liens[link_id]
#             if from_node in coordonnees_noeuds:
#                 x, y = coordonnees_noeuds[from_node]
#             else:
#                 continue  

#             if time - dernier_temps_par_vehicule[vehicle_id] >= 60:
#                 positions_par_vehicule[vehicle_id].append((int(time // 60), x, y))
#                 dernier_temps_par_vehicule[vehicle_id] = time

#     with open(fichier_sortie_csv, 'w') as f_out:
#         f_out.write("AgentId,Temps_minute,x,y\n")
#         for vehicle_id, positions in positions_par_vehicule.items():
#             # Trier les positions par temps
#             positions_triees = sorted(positions, key=lambda x: x[0])
#             for time_minute, x, y in positions_triees:
#                 f_out.write(f"{vehicle_id},{time_minute},{x},{y}\n")

# fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car.xml"
# fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_network.xml.gz"
# fichier_sortie_csv = "agent_positions.csv"

# ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv)

# -----------------------------------------------------------------------------------------------------------
# Pour extraite des position des agents(par minute) avec Motif_Orig & Motif_Dest

import xml.etree.ElementTree as ET
import gzip
from collections import defaultdict

# lire le fichier reseau et recuperer les coordonnees des nœuds et les liens
def lire_reseau(fichier_network):
    coordonnees_noeuds = {}
    liens = {}
    
    with gzip.open(fichier_network, 'rt', encoding='utf-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        
        # recuperer les noeuds et leurs coordonnees
        for node in root.findall('.//node'):
            node_id = node.get('id')
            x = float(node.get('x'))
            y = float(node.get('y'))
            coordonnees_noeuds[node_id] = (x, y)       
        # recuperer les liens et leurs noeuds de depart et d'arrivee
        for link in root.findall('.//link'):
            link_id = link.get('id')
            from_node = link.get('from')
            to_node = link.get('to')
            liens[link_id] = (from_node, to_node)
    
    return coordonnees_noeuds, liens

# Lire les events de vehicule et ecrire les positions des agents dans un fichier CSV avec motifs
def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv):
    # lire le reseau 
    coordonnees_noeuds, liens = lire_reseau(fichier_network)
    
    # dictionnaire pour stocker les positions des agents à chaque minute
    positions_par_vehicule = defaultdict(list)
    dernier_temps_par_vehicule = defaultdict(lambda: -60)  # dernier temps enregistre pour chaque véhicule (initialise à -60 pour la premiere minute)
    
    motif_orig = None
    motif_dest = None
    tree = ET.parse(fichier_events)
    root = tree.getroot()

    # itrer sur tous les elements "event"
    for event in root.findall('event'):
        event_type = event.get('type')
        vehicle_id = event.get('vehicle')

        # gerer les events actend pour capturer le motif d'origine
        if event_type == 'actend':
            motif_orig = event.get('actType')  
        # gerer les events actstart pour capturer le motif de destination
        elif event_type == 'actstart':
            motif_dest = event.get('actType')  
            # lorsque l'on a à la fois le Motif_Orig et Motif_Dest, on peut ecrire les positions correspondantes
            for vehicle, positions in positions_par_vehicule.items():
                # Pour chaque enregistrement deja accumule, on associe le motif
                for (time_minute, x, y) in positions:
                    with open(fichier_sortie_csv, 'a') as f_out:
                        f_out.write(f"{vehicle},{time_minute},{x},{y},{motif_orig},{motif_dest}\n")
            positions_par_vehicule.clear()  # Une fois ecrit, on efface les positions pour un nouveau trajet

        # se concentrer uniquement sur les events "entered link" et "left link"
        if event_type in ['entered link', 'left link']:
            link_id = event.get('link')
            time = float(event.get('time'))

            # verif si ce lien existe dans le reseau
            if link_id not in liens:
                continue  # si le lien n'existe pas, passer au prochain evenement

            # recuperer le noeud de depart "from" du lien
            from_node, _ = liens[link_id]

            # recuper les coordonnees du nœud "from"
            if from_node in coordonnees_noeuds:
                x, y = coordonnees_noeuds[from_node]
            else:
                continue  # si les coordonnees ne sont pas trouvees, passer au prochain avents

            # calculer la prochaine minute à enregistrer
            if time - dernier_temps_par_vehicule[vehicle_id] >= 60:
                # Accumuler la position pour le vehicule à cette minute
                positions_par_vehicule[vehicle_id].append((int(time // 60), x, y))
                dernier_temps_par_vehicule[vehicle_id] = time

    # Si des positions restent apres la derniere boucle, on les ecrit
    if motif_orig and motif_dest:
        for vehicle, positions in positions_par_vehicule.items():
            for (time_minute, x, y) in positions:
                with open(fichier_sortie_csv, 'a') as f_out:
                    f_out.write(f"{vehicle},{time_minute},{x},{y},{motif_orig},{motif_dest}\n")

fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car.xml"
fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_network.xml.gz"
fichier_sortie_csv = "agent_positions_motif.csv"

# l'en-tete du fichier CSV avant d'ecrire
with open(fichier_sortie_csv, 'w') as f_out:
    f_out.write("AgentId,Temps_minute,x,y,Motif_Orig,Motif_Dest\n")

ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv)

# -----------------------------------------------------------------------------------------------------------
# Pour extraite des position des agents sans interpolation (par minute) avec Motif_Orig & Motif_Dest

# import xml.etree.ElementTree as ET
# import gzip
# from collections import defaultdict 

# # lire le fichier reseau et recuperer les coordonnees des noeuds et les liens
# def lire_reseau(fichier_network): 
#     coordonnees_noeuds = {}        # dict ou chaque cle : un id de noeud,  la valeur : un tuple des coordonnees (x, y)
#     liens = {}                     # dict ou chaque cle : un id de lien, la valeur : un tuple des noeuds de depart et d'arrivee de ce lien
    
#     with gzip.open(fichier_network, 'rt', encoding='utf-8') as f:
#         tree = ET.parse(f)
#         root = tree.getroot()
        
#         # recuperer les noeuds et leurs coordonnees
#         for node in root.findall('.//node'):
#             node_id = node.get('id')
#             x = float(node.get('x'))
#             y = float(node.get('y'))
#             coordonnees_noeuds[node_id] = (x, y)
        
#         # recuperer les liens et leurs noeuds de depart et d'arrivee
#         for link in root.findall('.//link'):
#             link_id = link.get('id')
#             from_node = link.get('from')
#             to_node = link.get('to')
#             liens[link_id] = (from_node, to_node)
    
#     return coordonnees_noeuds, liens

# # lire les events vehicule et ecrire les positions des agents dans un fichier CSV avec motifs
# def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv):
#     coordonnees_noeuds, liens = lire_reseau(fichier_network)
    
#     # dict pour stocker les positions des agents à chaque minute : vehicle_id, liste des positions du vehicule (temps,x,y)
#     positions_par_vehicule = defaultdict(list)
#     # dict qui stocke le dernier temps enregistre pour chaque vehicule (initialise à -60 pour 1er minute)
#     dernier_temps_par_vehicule = defaultdict(lambda: -60)  
    
#     motif_orig = None
#     motif_dest = None

#     # ouvrir output_detaillees_car.xml (fichier non gzippe)
#     tree = ET.parse(fichier_events)
#     root = tree.getroot()

#     # iterer sur tous les elements "event"
#     for event in root.findall('event'):
#         event_type = event.get('type')
#         vehicle_id = event.get('vehicle')

#         # gerer les events "actend" pour capturer le motif d'origine
#         if event_type == 'actend':
#             motif_orig = event.get('actType') 
#         # gerer les events "actstart" pour capturer le motif de destination
#         elif event_type == 'actstart':
#             motif_dest = event.get('actType')  

#             # lorsque l'on a à la fois le Motif_Orig et Motif_Dest, on peut ecrire les positions correspondantes
#             for vehicle, positions in positions_par_vehicule.items():
#                 for (time_minute, x, y) in positions:
#                     with open(fichier_sortie_csv, 'a') as f_out:
#                         f_out.write(f"{vehicle},{time_minute},{x},{y},{motif_orig},{motif_dest}\n")
#             positions_par_vehicule.clear()  # on efface les positions pour un nouveau trajet

#         # se concentrer uniquement sur les events "entered link" et "left link"
#         if event_type in ['entered link', 'left link']:
#             link_id = event.get('link')
#             time = float(event.get('time'))

#             # verifier si ce lien existe dans le reseau
#             if link_id not in liens:
#                 continue  # si le lien n'existe pas, passer au prochain events

#             # recuperer le noeud de depart "from" du lien
#             from_node, _ = liens[link_id]

#             # recuperer les coordonnees du noeud "from"
#             if from_node in coordonnees_noeuds:
#                 x, y = coordonnees_noeuds[from_node]
#             else:
#                 continue  # si les coordonnees ne sont pas trouvees, passer au prochain events

#             # calculer la prochaine minute à enregistrer
#             # si une minute s'est scoulse depuis le dernier enregistrement pour ce vehicule, on stocke sa position à ce moment
#             if time - dernier_temps_par_vehicule[vehicle_id] >= 60:
#                 # accumuler la position pour le vehicule à cette minute
#                 positions_par_vehicule[vehicle_id].append((int(time // 60), x, y))
#                 dernier_temps_par_vehicule[vehicle_id] = time

#     # si des positions restent apres la derniere boucle, on les ecrit
#     if motif_orig and motif_dest:
#         for vehicle, positions in positions_par_vehicule.items():
#             for (time_minute, x, y) in positions:
#                 with open(fichier_sortie_csv, 'a') as f_out:
#                     f_out.write(f"{vehicle},{time_minute},{x},{y},{motif_orig},{motif_dest}\n")

# fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car.xml"
# fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_network.xml.gz"
# fichier_sortie_csv = "agent_positions_motif.csv"

# with open(fichier_sortie_csv, 'w') as f_out:
#     f_out.write("AgentId,Temps_minute,x,y,Motif_Orig,Motif_Dest\n")

# ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv)

# -----------------------------------------------------------------------------------------------------------
# Pour extraite des position exactes avec interpolation des agents (par minute) avec Motif_Orig & Motif_Dest

import xml.etree.ElementTree as ET
import gzip
from collections import defaultdict

# lire le fichier reseau et recupere les coordonnees des noeuds et les liens
def lire_reseau(fichier_network):
    coordonnees_noeuds = {}  # dict ou chaque cle : un id de noeud, la valeur : un tuple des coordonnees (x, y)
    liens = {}               # dict ou chaque cle : un id de lien, la valeur : un tuple des noeuds de depart et d'arrivee de ce lien

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

# interpolation des positions entre le temps d'entree et le temps de sortie
def interpoler_positions(enterTime, leaveTime, coordStart, coordEnd):
    interpolated_positions = []
    duration = leaveTime - enterTime

    # interpolation à chaque minute entre enterTime et leaveTime
    for t in range(int(enterTime), int(leaveTime) + 1, 60): 
        ratio = (t - enterTime) / duration
        x = coordStart[0] + ratio * (coordEnd[0] - coordStart[0])
        y = coordStart[1] + ratio * (coordEnd[1] - coordStart[1])
        interpolated_positions.append((t // 60, x, y))  
    return interpolated_positions

# lire les events de vehicule, ecrire les positions des agents dans un fichier CSV avec motifs et interpolation
def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv):
    coordonnees_noeuds, liens = lire_reseau(fichier_network)
    positions_par_vehicule = defaultdict(list)  # stocke les positions des vehicules apres interpolation. cle : vehicle_id, valeur : liste de positions interpole
    # dernier_temps_par_vehicule = defaultdict(lambda: -60)  # dernier temps enregistre pour chaque vehicule
    motif_orig = None
    motif_dest = None
    enter_time = None
    leave_time = None
    coord_start = None
    coord_end = None

    tree = ET.parse(fichier_events)
    root = tree.getroot()

    # iterer sur tous les events
    for event in root.findall('event'):
        event_type = event.get('type')
        vehicle_id = event.get('vehicle')

        # pour capturer le motif d'origine
        if event_type == 'actend':
            motif_orig = event.get('actType')

        # pour capturer le motif de destination
        elif event_type == 'actstart':
            motif_dest = event.get('actType')

            # lorsque l'on a à la fois Motif_Orig et Motif_Dest, on ecrire les positions correspondantes
            if motif_orig and motif_dest:
                for vehicle, positions in positions_par_vehicule.items():
                    for (time_minute, x, y) in positions:
                        with open(fichier_sortie_csv, 'a') as f_out:
                            f_out.write(f"{vehicle},{time_minute},{x},{y},{motif_orig},{motif_dest}\n")
                # effacer les positions pour un nouveau trajet            
                positions_par_vehicule.clear()  

        if event_type == 'entered link':
            link_id = event.get('link')
            enter_time = float(event.get('time'))

            # recuper le noeud de depart "from" et d'arrivee "to" du lien
            if link_id in liens:
                from_node, to_node = liens[link_id]
                coord_start = coordonnees_noeuds.get(from_node)
                coord_end = coordonnees_noeuds.get(to_node)

        elif event_type == 'left link':
            leave_time = float(event.get('time'))

            # si toutes les donnees sont disponibles, effectuer l'interpolation
            if enter_time and leave_time and coord_start and coord_end:
                interpolated_positions = interpoler_positions(enter_time, leave_time, coord_start, coord_end)

                # accumuler les positions interpolees
                positions_par_vehicule[vehicle_id].extend(interpolated_positions)

            # reinitialiser les valeurs pour le prochain lien
            enter_time = None
            leave_time = None
            coord_start = None
            coord_end = None

    # si des positions restent apres la derniere boucle, on les ecrit
    if motif_orig and motif_dest:
        for vehicle, positions in positions_par_vehicule.items():
            for (time_minute, x, y) in positions:
                with open(fichier_sortie_csv, 'a') as f_out:
                    f_out.write(f"{vehicle},{time_minute},{x},{y},{motif_orig},{motif_dest}\n")

fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car.xml"
fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_network.xml.gz"
fichier_sortie_csv = "agent_positions_motif.csv"

with open(fichier_sortie_csv, 'w') as f_out:
    f_out.write("AgentId,Temps_minute,x,y,Motif_Orig,Motif_Dest\n")

ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv)

# -----------------------------------------------------------------------------------------------------------
# Pour extraite des evenement importants qui utilises tous les mode exist (ex. bike, pt, car, )

# import xml.etree.ElementTree as ET
# import gzip
# from collections import defaultdict

# # fonction pour lire et ecrire les events filtres pour tous les agents dans un nouveau fichier XML
# def ecrire_evenements_filtre(fichier_entree, fichier_sortie):
#     # dictionnaire pour stocker les events de chaque agent, tries par temps
#     evenements_par_agent = defaultdict(list)
    
#     with gzip.open(fichier_entree, 'rt', encoding='utf-8') as f:
#         # parse le fichier XML
#         tree = ET.parse(f)
#         root = tree.getroot()

#         # iterer sur tous les elements "event"
#         for event in root.findall('event'):
#             event_type = event.get('type')
#             person_id = event.get('person')
#             vehicle_id = event.get('vehicle')
#             facility = event.get('facility')
#             mode = event.get('mode', 'unknown')  # on recupere le mode de transport s'il est present

#             # identifier la personne concernee par l'evenement, soit via l'ID de la personne, soit via le vehicule
#             if person_id:
#                 person_or_vehicle_id = person_id
#             elif vehicle_id:
#                 # si c'est un vehicule, extraire la partie avant ":car", etc., pour l'ID de la personne
#                 person_or_vehicle_id = vehicle_id.split(':')[0] if ':' in vehicle_id else vehicle_id
#             else:
#                 continue

#             # filtrer les events avec condition pour actstart et actend
#             if (event_type in ['actend', 'actstart'] and facility) or \
#                event_type in ['left link', 'entered link', 'vehicle enters traffic', 'vehicle leaves traffic', 'travelled']:
#                 # extraire le temps de l'events pour le tri ultérieur
#                 time = float(event.get('time'))
                
#                 # stocker l'events avec son temps et son mode de transport dans le dictionnaire pour la personne ou son vehicule
#                 evenements_par_agent[person_or_vehicle_id].append((time, event, mode))

#     # creer un nouvel element racine pour le fichier de sortie
#     root_sortie = ET.Element('events')

#     # traiter les events agent par agent
#     for person_id, events in evenements_par_agent.items():
#         # Trier les événements par temps pour chaque agent
#         events_triees = sorted(events, key=lambda x: x[0])

#         # ajouter les events trie à la racine du fichier de sortie
#         for _, event, mode in events_triees:
#             # Ajouter l'attribut 'mode' si necessaire
#             if mode != 'unknown':
#                 event.set('mode', mode)
#             root_sortie.append(event)

#     # creer un nouvel arbre XML à partir des events filtres et tries
#     tree_sortie = ET.ElementTree(root_sortie)

#     # ecrire le nouvel arbre dans un fichier XML
#     with open(fichier_sortie, 'wb') as f_out:
#         tree_sortie.write(f_out, encoding='utf-8', xml_declaration=True)

# fichier_entree = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_events.xml.gz"
# fichier_sortie = "output_detaillees.xml"

# # Appeler la fonction pour ecrire les events filtres et tries dans le fichier de sortie
# ecrire_evenements_filtre(fichier_entree, fichier_sortie)

# -----------------------------------------------------------------------------------------------------------
# Pour extraite des personnes evenement importants qui utilises des voiture seulement (walk trajet un peu ca va mais on ne visualise pas)

import xml.etree.ElementTree as ET
import gzip
from collections import defaultdict

def ecrire_evenements_filtre(fichier_entree, fichier_sortie):
    # dict pour stocker les events de chaque agent par temps
    evenements_par_agent = defaultdict(list)
    agents_qui_utilisent_voiture = set()  # set pour les agents utilsie voiture
    agents_qui_nutilisent_pas_voiture = set()  # set pour les agents utilise walk seulement
    
    with gzip.open(fichier_entree, 'rt', encoding='utf-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()

        # examine all the components of the events
        for event in root.findall('event'):
            event_type = event.get('type')
            person_id = event.get('person')
            vehicle_id = event.get('vehicle')

            # si events concerne une personne ou un vehicule de type person_id:car
            if person_id:
                person_or_vehicle_id = person_id
            elif vehicle_id and vehicle_id.endswith(':car'):
                person_or_vehicle_id = vehicle_id.split(':')[0]
            else:
                continue  

            # verifier si cet agent utilise car ou walk
            leg_mode = event.get('legMode')
            if leg_mode == 'car':
                agents_qui_utilisent_voiture.add(person_or_vehicle_id) 
            elif leg_mode == 'walk':
                # ajouter cet agent au set des agents qui n'utilisent que walk si on n'a pas vu d'utilisation de la car
                if person_or_vehicle_id not in agents_qui_utilisent_voiture:
                    agents_qui_nutilisent_pas_voiture.add(person_or_vehicle_id)

            # ajouter les events si l'agent utilise la voiture ou est autorise a marcher
            if event_type in ['actend', 'actstart'] and event.get('facility'):
                time = float(event.get('time'))
                evenements_par_agent[person_or_vehicle_id].append((time, event))
            elif event_type in ['left link', 'entered link', 'vehicle enters traffic', 'vehicle leaves traffic']:
                time = float(event.get('time'))
                evenements_par_agent[person_or_vehicle_id].append((time, event))

    root_sortie = ET.Element('events')

    # traiter les events agent par agent
    for person_id, events in evenements_par_agent.items():
        # si l'agent utilise car
        if person_id in agents_qui_utilisent_voiture:
            # organise les events par temps pour chaque agent
            events_triees = sorted(events, key=lambda x: x[0])
            # ajouter cette events a output fichier
            for _, event in events_triees:
                root_sortie.append(event)

    tree_sortie = ET.ElementTree(root_sortie)

    # ecrire le nouvel arbre dans un fichier XML
    with open(fichier_sortie, 'wb') as f_out:
        tree_sortie.write(f_out, encoding='utf-8', xml_declaration=True)

fichier_entree = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_events.xml.gz"
fichier_sortie = "output_detaillees_car.xml"
ecrire_evenements_filtre(fichier_entree, fichier_sortie)

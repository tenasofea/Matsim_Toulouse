# -----------------------------------------------------------------------------------------------
# Lister les evenement(facility, vehic enter traffic, vehic leaves traffic, left link, entered link) qui se produit pour agent specifique 

import xml.etree.ElementTree as ET
import gzip

# Fonction pour lire et écrire les événements filtrés d'un agent spécifique dans un nouveau fichier XML
def ecrire_evenements_agent_filtre(fichier, agent_id, fichier_sortie):
    with gzip.open(fichier, 'rt', encoding='utf-8') as f:
        # Parse le fichier XML
        tree = ET.parse(f)
        root = tree.getroot()
        
        # Créer un nouvel élément racine pour le fichier de sortie
        root_sortie = ET.Element('events')
        
        # Itérer sur tous les éléments "event"
        for event in root.findall('event'):
            event_type = event.get('type')
            # Vérifier si l'événement correspond à l'agent spécifié
            if (event.get('person') == str(agent_id)) or (event.get('vehicle') == str(agent_id)+':car'):
                # Filtrer pour les événements "facility", "vehicle enters/leaves traffic", "left link" et "entered link"
                if 'facility' in event.attrib or event_type in ['vehicle enters traffic', 'vehicle leaves traffic', 'left link', 'entered link']:
                    # Ajouter l'événement au fichier de sortie
                    root_sortie.append(event)

        # Créer un nouvel arbre XML à partir des événements filtrés
        tree_sortie = ET.ElementTree(root_sortie)
        # Écrire le nouvel arbre dans un fichier XML
        tree_sortie.write(fichier_sortie, encoding='utf-8', xml_declaration=True)

# Spécifier le fichier d'entrée, l'ID de l'agent et le fichier de sortie
fichier = ("C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_events.xml.gz")
agent_id = "1150695"  # Remplacer par l'ID de l'agent souhaité
fichier_sortie = "TrajetAgentSpecifique.xml"

# Appeler la fonction pour écrire les événements filtrés de l'agent dans le fichier de sortie
ecrire_evenements_agent_filtre(fichier, agent_id, fichier_sortie)

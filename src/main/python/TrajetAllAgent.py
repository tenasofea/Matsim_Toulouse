# -----------------------------------------------------------------------------------------------
# Lister tous les evenements (toutes les lignes) qui se produit pour agent specifique 

import xml.etree.ElementTree as ET
import gzip

# Fonction pour lire les événements d'un agent spécifique depuis output_events.xml.gz et les écrire dans TrajetAllAgent.xml
def ecrire_evenements_agent(fichier_entree, agent_id, fichier_sortie):
    with gzip.open(fichier_entree, 'rt', encoding='utf-8') as f:
        # Parse le fichier XML d'entrée
        tree = ET.parse(f)
        root = tree.getroot()
        
        # Créer la racine pour le nouveau fichier XML
        root_sortie = ET.Element('events')
        
        # Itérer sur tous les éléments "event"
        for event in root.findall('event'):
            # Vérifier si l'événement correspond à l'agent spécifié
            if (event.get('person') == str(agent_id)) or (event.get('vehicle') == str(agent_id)+':car'):
                # Ajouter l'événement correspondant à la racine du nouveau fichier XML
                root_sortie.append(event)
        
        # Créer l'arbre avec les événements filtrés
        tree_sortie = ET.ElementTree(root_sortie)
        
        # Écrire dans le fichier XML de sortie
        with open(fichier_sortie, 'wb') as f_out:
            tree_sortie.write(f_out, encoding='utf-8', xml_declaration=True)

# Spécifier le fichier d'entrée, l'ID de l'agent et le fichier de sortie
fichier_entree = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_events.xml.gz"
agent_id = "763545"  # Remplacer par l'ID de l'agent souhaité
fichier_sortie = "TrajetAllAgent.xml"

# Appeler la fonction pour écrire les événements de l'agent dans le fichier de sortie
ecrire_evenements_agent(fichier_entree, agent_id, fichier_sortie)

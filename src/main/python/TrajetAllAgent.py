# -----------------------------------------------------------------------------------------------
# Lister tous les evenements (toutes les lignes) qui se produit pour agent specifique 

import xml.etree.ElementTree as ET
import gzip

# lire les eventss d'un agent specifique depuis output_events.xml.gz et les ecrire dans TrajetAllAgent.xml
def ecrire_evenements_agent(fichier_entree, agent_id, fichier_sortie):
    with gzip.open(fichier_entree, 'rt', encoding='utf-8') as f:
        # parse le fichier XML d'entree
        tree = ET.parse(f)
        root = tree.getroot()
        
        # creer la racine pour le nouveau fichier XML
        root_sortie = ET.Element('events')
        
        # iterer sur tous les elements "event"
        for event in root.findall('event'):
            # verifier si les events correspond à l'agent specifie
            if (event.get('person') == str(agent_id)) or (event.get('vehicle') == str(agent_id)+':car'):
                # Ajouter events correspondant à la racine du nouveau fichier XML
                root_sortie.append(event)
        
        tree_sortie = ET.ElementTree(root_sortie)
        
        with open(fichier_sortie, 'wb') as f_out:
            tree_sortie.write(f_out, encoding='utf-8', xml_declaration=True)

fichier_entree = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_events.xml.gz"
agent_id = "763545" 
fichier_sortie = "TrajetAllAgent.xml"

ecrire_evenements_agent(fichier_entree, agent_id, fichier_sortie)

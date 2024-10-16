package org.matsim.analysis;

import org.w3c.dom.*;
import javax.xml.parsers.DocumentBuilderFactory;
import java.util.*;

public class ActivityPreprocessor {

    // Stockage des changements de motif pour chaque agent, trié par temps
    private final Map<String, List<ActivityChange>> activityTimeline;

    public ActivityPreprocessor() {
        activityTimeline = new HashMap<>();
    }

    // Classe interne pour représenter un changement de motif
    private static class ActivityChange {
        double time;
        String motif;

        public ActivityChange(double time, String motif) {
            this.time = time;
            this.motif = motif;
        }
    }

    // Méthode pour analyser le fichier output_events.xml et pré-calculer les motifs
    public void parseActivityChanges(String filePath) {
        try {
            Document doc = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(filePath);
            doc.getDocumentElement().normalize();

            NodeList eventList = doc.getElementsByTagName("event");

            for (int i = 0; i < eventList.getLength(); i++) {
                Element eventElement = (Element) eventList.item(i);
                String eventType = eventElement.getAttribute("type");

                // On s'intéresse seulement aux actstart et actend
                if (eventType.equals("actstart") || eventType.equals("actend")) {
                    String personId = eventElement.getAttribute("person");
                    double time = Double.parseDouble(eventElement.getAttribute("time"));
                    String actType = eventElement.getAttribute("actType");

                    String motif;
                    if (eventType.equals("actstart")) {
                        motif = "going to " + actType;
                    } else {
                        motif = "moving after " + actType;
                    }

                    // Ajouter cet événement de changement de motif à la timeline de l'agent
                    activityTimeline.computeIfAbsent(personId, k -> new ArrayList<>()).add(new ActivityChange(time, motif));
                }
            }

            // Trier chaque timeline d'agent par le temps pour une recherche efficace plus tard
            for (List<ActivityChange> changes : activityTimeline.values()) {
                changes.sort(Comparator.comparingDouble(a -> a.time));
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Méthode pour obtenir le motif actuel d'un agent en fonction du temps
    public String getCurrentMotif(String personId, double currentTime) {
        List<ActivityChange> changes = activityTimeline.get(personId);
        if (changes == null || changes.isEmpty()) {
            return "unknown";  // Pas de données pour cet agent
        }

        // Chercher le dernier changement avant ou à l'instant actuel
        for (int i = changes.size() - 1; i >= 0; i--) {
            if (changes.get(i).time <= currentTime) {
                return changes.get(i).motif;
            }
        }

        return "unknown";  // Si aucune activité ne correspond
    }
}

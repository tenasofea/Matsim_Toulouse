package org.matsim.analysis;

import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.events.*;
import org.matsim.api.core.v01.events.handler.LinkEnterEventHandler;
import org.matsim.api.core.v01.events.handler.LinkLeaveEventHandler;
import org.matsim.api.core.v01.network.Network;
import org.matsim.api.core.v01.network.Link;
import org.matsim.api.core.v01.Coord;

import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

// pour capturer deux types evenement matsim lorsqu’un agent entre sur un lien et quitte ce lien
public class SimpleLinkEventHandler implements LinkEnterEventHandler, LinkLeaveEventHandler {

    //pour obtenir des informations comme les coordonnees des liens
    //pour ecrire les donnees de position des agents dans un fichier csv
    private final Network network;
    private final FileWriter csvWriter;
    private final Map<String, String> currentMotifs;  // Current motif for each agent

    private final Map<String, String> personToVehicleMap; // Map person ID to vehicle ID

    // structure temporaire pour stocker les donnees d'entree des agent - permet d'acceder rapidement aux values via sa cle
    private final Map<String, AgentData> agentLinkEntry = new HashMap<>();

    // class pour stocker les informations necessaires pour chaque agent
    private static class AgentData {
        double enterTime;
        Coord coordStart;
        Coord coordEnd;
        double linkLength;
        String motif;  // ajout du motif

        public AgentData(double enterTime, Coord coordStart, Coord coordEnd, double linkLength, String motif) {
            this.enterTime = enterTime;
            this.coordStart = coordStart;
            this.coordEnd = coordEnd;
            this.linkLength = linkLength;
            this.motif = motif;
        }
    }

    // constructeur pour initialiser le fichier CSV
    public SimpleLinkEventHandler(Network network) throws IOException {
        this.network = network;
        this.currentMotifs = new HashMap<>();
        this.personToVehicleMap = new HashMap<>();
        csvWriter = new FileWriter("agent_positions_toulouse.csv");
        csvWriter.append("AgentId,Temps,X,Y,Motif\n");
    }

    //methode vient de l'interface LinkEnterEventHandler
    //une interpolation donc on a besoin le temps sur chaque lien
    //appele par le manager chaque fois qu'un events LinkEnterEvent se produit dans la simulation
    //1er methode
    @Override
    public void handleEvent(LinkEnterEvent event) {
        // get agentid, linkid and temps quand il entrer sur lien
        String vehicleId = event.getVehicleId().toString();
        Id<Link> linkId = event.getLinkId();
        double enterTime = event.getTime();

        // recupere les coordonnees du lien
        Link link = network.getLinks().get(linkId);
        Coord coordStart = link.getFromNode().getCoord();
        Coord coordEnd = link.getToNode().getCoord();

        // Retrieve the person ID associated with this vehicle
        String personId = personToVehicleMap.get(vehicleId);
        String motif = currentMotifs.getOrDefault(personId, "unknown");

        // stocker les informations de l'agent pour l'interpolation future
        agentLinkEntry.put(personId, new AgentData(enterTime, coordStart, coordEnd, link.getLength(), motif));
    }

    //2eme methode
    @Override
    public void handleEvent(LinkLeaveEvent event) {
        // get agentid and temps quand il sort de lien
        String vehicleId = event.getVehicleId().toString();
        double leaveTime = event.getTime();
        String personId = personToVehicleMap.get(vehicleId);

        // recupere les donnees d'entree de l'agent dans la forme AgentData
        AgentData agentData = agentLinkEntry.get(personId);
        if (agentData == null) {
            return;  // agent n'a pas ete trouve, donc pas d'interpolation possible, il sort de la methode
        }

        //calcule la duratiom pendant l'agent a ete sur le lien
        double duration = leaveTime - agentData.enterTime;

        // interpolation lineaire pour chaque seconde entre l'entree et la sortie
        // pour estimer la position d'un agent a chaque seconde pendant qu'il se deplace entre deux points sur un lien
        for (double t = agentData.enterTime; t <= leaveTime; t++) {
            double ratio = (t - agentData.enterTime) / duration;
            double x = agentData.coordStart.getX() + ratio * (agentData.coordEnd.getX() - agentData.coordStart.getX());
            double y = agentData.coordStart.getY() + ratio * (agentData.coordEnd.getY() - agentData.coordStart.getY());


            // write les coordonnees pour chaque seconde dans le fichier .csv
            writeToCSV(personId, t, x, y, agentData.motif);
        }

        // remove l'agent de la structure temporaire
        agentLinkEntry.remove(personId);
    }

    // Handle actstart and actend from output_events.xml manually
    public void handleActivityEvent(String personId, String actType, boolean isStart) {
        String motif = currentMotifs.getOrDefault(personId, "unknown");

        // If it's an actstart, update the motif
        if (isStart) {
            switch (actType) {
                case "work":
                    motif = "work";
                    break;
                case "home":
                    motif = "home";
                    break;
                case "education":
                    motif = "education";
                    break;
                case "shop":
                    motif = "shop";
                    break;
                case "leisure":
                    motif = "leisure";
                    break;
//                default:
//                    motif = "moving after " + actType;
//                    break;
            }
            currentMotifs.put(personId, motif);
        } else {
            motif = "moving after " + actType;
        }

//        currentMotifs.put(personId, motif);
    }

    // Add method to map person ID to vehicle ID during departure
    public void mapPersonToVehicle(String personId, String vehicleId) {
        personToVehicleMap.put(vehicleId, personId);
    }

    // methode pour ecrire vers csv
    private void writeToCSV(String agentId, double time, double x, double y, String motif) {
        try {
            csvWriter.append(agentId)
                    .append(",")
                    .append(String.valueOf(time))
                    .append(",")
                    .append(String.valueOf(x))
                    .append(",")
                    .append(String.valueOf(y))
                    .append(",")
                    .append(motif)
                    .append("\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // ferme fichi csv apres l'ecriture
    // flush() s'assure que tout est bien écrit sur le disque avant de fermer le fichier
    public void closeFile() throws IOException {
        csvWriter.flush();
        csvWriter.close();
    }
}


//package org.matsim.analysis;
//
//import org.matsim.api.core.v01.Id;
//import org.matsim.api.core.v01.events.handler.LinkEnterEventHandler;
//import org.matsim.api.core.v01.events.handler.LinkLeaveEventHandler;
//import org.matsim.api.core.v01.network.Network;
//import org.matsim.api.core.v01.events.LinkEnterEvent;
//import org.matsim.api.core.v01.events.LinkLeaveEvent;
//import org.matsim.api.core.v01.network.Link;
//import java.io.FileWriter;
//import java.io.IOException;
//
//public class SimpleLinkEventHandler implements LinkEnterEventHandler, LinkLeaveEventHandler {
//
//    private final Network network;
//    private final FileWriter csvWriter;
//
//    // Constructeur pour initialiser le fichier CSV
//    public SimpleLinkEventHandler(Network network) throws IOException {
//        this.network = network;
//        csvWriter = new FileWriter("agent_positions.csv");
//        csvWriter.append("AgentId,Temps,Event,LinkId,X,Y\n");
//    }
//
//    @Override
//    public void handleEvent(LinkEnterEvent event) {
//        writeEventToCSV(event.getVehicleId().toString(), event.getTime(), "LinkEnter", event.getLinkId());
//    }
//
//    @Override
//    public void handleEvent(LinkLeaveEvent event) {
//        writeEventToCSV(event.getVehicleId().toString(), event.getTime(), "LinkLeave", event.getLinkId());
//    }
//
//    private void writeEventToCSV(String personId, double time, String eventType, Id<Link> linkId) {
//        try {
//            Link link = network.getLinks().get(linkId);
//            double x = link.getCoord().getX();
//            double y = link.getCoord().getY();
//
//            csvWriter.append(personId)
//                    .append(",")
//                    .append(String.valueOf(time))
//                    .append(",")
//                    .append(eventType)
//                    .append(",")
//                    .append(linkId.toString())
//                    .append(",")
//                    .append(String.valueOf(x))
//                    .append(",")
//                    .append(String.valueOf(y))
//                    .append("\n");
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//    }
//
//    public void closeFile() throws IOException {
//        csvWriter.flush();
//        csvWriter.close();
//    }
//}

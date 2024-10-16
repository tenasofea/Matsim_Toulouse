package org.matsim.analysis;

import org.matsim.api.core.v01.network.Network;
import org.matsim.core.events.EventsUtils;
import org.matsim.core.network.NetworkUtils;
import org.matsim.core.network.io.MatsimNetworkReader;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.IOException;
import java.util.zip.GZIPInputStream;
import java.io.FileInputStream;
import org.w3c.dom.Document;

//chargement du reseau et du traitement des evenements dans le fichier output_events.xml genere par MATSim.
public class SimpleAnalysis {
    public static void main(String[] args) {
        try {
            // charger network
            Network network = NetworkUtils.createNetwork();
//            new MatsimNetworkReader(network).readFile("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\output\\output_network.xml.gz");
            new MatsimNetworkReader(network).readFile("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\simulation_output_toulouse\\output_network.xml.gz");

            var manager = EventsUtils.createEventsManager();

// -------------------------------------------------------------------------------------------------------

            // creer un gestionnaire pour capturer events de type "LinkEnter" et "LinkLeave"
            SimpleLinkEventHandler handler = new SimpleLinkEventHandler(network);
            manager.addHandler(handler);

// ----------------------------------------------------------------------------------------------------------------------------

//            // creer un gestionnaire pour capturer les evenements de type "LinkEntrer" et "LinkLeaves"
//            // network est passe en parametre au SimpleLinkEventHandler dans le constructeur
//            // Si on decide un jour de suivre des événements supplémentaires (comme la congestion), on n'a pas à modifier le SimpleLinkEventHandler. Il suffit de créer un nouveau handler et de le connecter au manager
//            // (handler) pour suivre les evenement qui se produisent sur les liend du reseau
//            // (manager) coordonner la gestion des événements tels que le moment ou les agents se deplacent sur reseau
//            var handler = new SimpleLinkEventHandler(network, agentMotifs);
//            var manager = EventsUtils.createEventsManager();
//
//            // a chaque fois events se produisent, handler s'en occuper
//            manager.addHandler(handler);

// ------------------------------------------------------------------------------------------------------------------------------

            //output_events.xml.gz est lu manuellement et tous les events sont extraits en utilisant un analyseur DOM XML
            GZIPInputStream gzipInputStream = new GZIPInputStream(new FileInputStream("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\simulation_output_toulouse\\output_events.xml.gz"));
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse(gzipInputStream);
            doc.getDocumentElement().normalize();
            gzipInputStream.close();

            // get all events from xml
            NodeList eventList = doc.getElementsByTagName("event");

            //En fonction des events captures (debut ou fin d'activites, departs), le gestionnaire SimpleLinkEventHandler est appele pour mettre a jour les motifs des agent
            for (int i = 0; i < eventList.getLength(); i++) {
                Element eventElement = (Element) eventList.item(i);
                String eventType = eventElement.getAttribute("type");

                if (eventType.equals("actstart")) {
                    String personId = eventElement.getAttribute("person");
                    String actType = eventElement.getAttribute("actType");
                    handler.handleActivityEvent(personId, actType, true);  // true for actstart
                } else if (eventType.equals("actend")) {
                    String personId = eventElement.getAttribute("person");
                    String actType = eventElement.getAttribute("actType");
                    handler.handleActivityEvent(personId, actType, false);  // false for actend
                } else if (eventType.equals("departure")) {
                    String personId = eventElement.getAttribute("person");
                    String vehicleId = personId + ":" + eventElement.getAttribute("legMode");  // Create a vehicle ID with person ID and legMode
                    handler.mapPersonToVehicle(personId, vehicleId);
                }
            }


            // lire le fichier d'evenements et traite events avec gestionnaire manager. chaque events est capture et transmis au handler
//            EventsUtils.readEvents(manager, "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\output\\output_events.xml.gz");
            EventsUtils.readEvents(manager, "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\simulation_output_toulouse\\output_events.xml.gz");

            // ferme le fichier apres l'ecriture
            handler.closeFile();

        } catch (IOException e) {
            e.printStackTrace();
        } catch (SAXException e) {
            throw new RuntimeException(e);
        } catch (ParserConfigurationException e) {
            throw new RuntimeException(e);
        }
    }
}

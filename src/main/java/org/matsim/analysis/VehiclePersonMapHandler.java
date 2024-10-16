package org.matsim.analysis;

import org.matsim.api.core.v01.events.PersonEntersVehicleEvent;
import org.matsim.api.core.v01.events.handler.PersonEntersVehicleEventHandler;

import java.util.Map;

public class VehiclePersonMapHandler implements PersonEntersVehicleEventHandler {

    // Map pour associer vehicleId à personId
    private Map<String, String> vehicleToPersonMap;

    public void VehicleToPersonMappingHandler(Map<String, String> vehicleToPersonMap) {
        this.vehicleToPersonMap = vehicleToPersonMap;
    }

    public VehiclePersonMapHandler(Map<String, String> vehicleToPersonMap) {
        this.vehicleToPersonMap = vehicleToPersonMap;
    }

    @Override
    public void handleEvent(PersonEntersVehicleEvent event) {
        String vehicleId = event.getVehicleId().toString();
        String personId = event.getPersonId().toString();

        // Associer le vehicleId au personId
        vehicleToPersonMap.put(vehicleId, personId);
        System.out.println("Mapped vehicleId=" + vehicleId + " to personId=" + personId);
    }
}
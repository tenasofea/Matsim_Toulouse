package org.matsim.analysis;

import org.matsim.api.core.v01.Coord;
import org.matsim.api.core.v01.events.LinkEnterEvent;
import org.matsim.api.core.v01.events.LinkLeaveEvent;
import org.matsim.api.core.v01.events.handler.LinkEnterEventHandler;
import org.matsim.api.core.v01.events.handler.LinkLeaveEventHandler;
import org.matsim.api.core.v01.network.Link;
import org.matsim.api.core.v01.network.Network;

public class TrackPosition implements LinkEnterEventHandler, LinkLeaveEventHandler {

    private final Network network;

    // Constructor to accept the network object
    public TrackPosition(Network network) {
        this.network = network;
    }

    @Override
    public void handleEvent(LinkEnterEvent event) {
        Link link = network.getLinks().get(event.getLinkId());
        Coord coord = link.getCoord(); // Get the coordinates of the link
        System.out.println("Agent " + event.getVehicleId() + " entered link " + event.getLinkId() +
                " at time " + event.getTime() +
                " with position x: " + coord.getX() + ", y: " + coord.getY());
        // You can store or broadcast this position (x, y) in real time
    }

    @Override
    public void handleEvent(LinkLeaveEvent event) {
        Link link = network.getLinks().get(event.getLinkId());
        Coord coord = link.getCoord(); // Get the coordinates of the link
        System.out.println("Agent " + event.getVehicleId() + " left link " + event.getLinkId() +
                " at time " + event.getTime() +
                " with position x: " + coord.getX() + ", y: " + coord.getY());
        // You can track and broadcast the position when the agent leaves the link as well
    }

    @Override
    public void reset(int iteration) {
        // Reset any data for the new iteration if needed
    }
}

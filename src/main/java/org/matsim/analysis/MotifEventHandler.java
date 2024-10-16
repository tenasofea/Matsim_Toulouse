package org.matsim.analysis;

import org.matsim.api.core.v01.events.ActivityEndEvent;
import org.matsim.api.core.v01.events.ActivityStartEvent;
import org.matsim.api.core.v01.events.handler.ActivityEndEventHandler;
import org.matsim.api.core.v01.events.handler.ActivityStartEventHandler;

import java.util.Map;

public class MotifEventHandler implements ActivityStartEventHandler, ActivityEndEventHandler {

    // Map for storing the current motif (destination purpose) for each agent
    private final Map<String, String> agentMotifs;

    public MotifEventHandler(Map<String, String> agentMotifs) {
        this.agentMotifs = agentMotifs;
    }

    @Override
    public void handleEvent(ActivityEndEvent event) {
        String personId = event.getPersonId().toString();
        String actType = event.getActType();

        // When an agent ends an activity (e.g., "home"), the motif will be set to the next activity
        // For example, if leaving home, the motif will be "going to work"
        if ("home".equals(actType)) {
            agentMotifs.put(personId, "work");
        } else if ("work".equals(actType)) {
            agentMotifs.put(personId, "home");

        } else {
            agentMotifs.put(personId, "other trip");
        }
        System.out.println("Updated motif for personId=" + personId + ": " + agentMotifs.get(personId));
    }

    @Override
    public void handleEvent(ActivityStartEvent event) {
        String personId = event.getPersonId().toString();
        String actType = event.getActType();

        // Once the agent starts a new activity, we can clear or update the motif
        agentMotifs.put(personId, "at " + actType);
    }
}

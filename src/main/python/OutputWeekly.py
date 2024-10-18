import xml.etree.ElementTree as ET
import gzip
import random
import os

def process_events(input_file, output_file, percentage_monday):
    # Open and parse the gzipped XML file
    with gzip.open(input_file, 'rb') as f_in:
        tree = ET.parse(f_in)
        root = tree.getroot()

        agents = set()  # Store agents for random sampling
        events = []  # Store all events
        for event in root:
            person = event.attrib.get('person')
            if person:
                agents.add(person)
            events.append(event)

        # Convert agents set to a list for sampling
        agent_list = list(agents)

        # Randomly assign 20% of agents to Monday
        monday_agents = set(random.sample(agent_list, int(len(agent_list) * percentage_monday)))

        # Update event times for agents not traveling on Monday
        for event in events:
            person = event.attrib.get('person')
            if person and person not in monday_agents:
                time = float(event.attrib['time'])
                # Shift time by adding 1 day, 2 days, etc., to distribute across the week
                event.attrib['time'] = str(time + random.choice([86400, 2*86400, 3*86400]))

        # Write the modified events back to a new gzipped XML file
        with gzip.open(output_file, 'wb') as f_out:
            tree.write(f_out, encoding='utf-8', xml_declaration=True)

# Define file paths
input_file = ('C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\simulation_output_toulouse\\output_events.xml.gz')
output_file = ('C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\output_events_week.xml.gz')

# Example usage
process_events(input_file, output_file, percentage_monday=0.20)

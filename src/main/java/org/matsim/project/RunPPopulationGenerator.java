package org.matsim.project;

import org.matsim.api.core.v01.Coord;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.Scenario;
import org.matsim.api.core.v01.TransportMode;
import org.matsim.api.core.v01.population.*;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.scenario.ScenarioUtils;
import org.matsim.core.utils.geometry.CoordinateTransformation;
import org.matsim.core.utils.geometry.transformations.TransformationFactory;

import java.util.HashMap;
import java.util.Map;

/**
 * "P" has to do with "Potsdam" and "Z" with "Zurich", but P and Z are mostly used to show which classes belong together.
 */
public class RunPPopulationGenerator implements Runnable {

	private Map<String, Coord> zoneGeometries = new HashMap<>();

	private CoordinateTransformation ct = TransformationFactory.getCoordinateTransformation(TransformationFactory.WGS84, TransformationFactory.WGS84_UTM33N);

	private Scenario scenario;

	private Population population;

	public static void main(String[] args) {
		RunPPopulationGenerator potsdamPop = new RunPPopulationGenerator();
		potsdamPop.run();
	}

	@Override
	public void run() {
		scenario = ScenarioUtils.createScenario(ConfigUtils.createConfig());
		population = scenario.getPopulation();
		fillZoneData();
		generatePopulation();
		PopulationWriter populationWriter = new PopulationWriter(scenario.getPopulation(), scenario.getNetwork());
		populationWriter.write("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\scenarios\\equil\\population-belfort.xml");
	}

//	private void fillZoneData() {
//		// Add the locations you want to use here.
//		// (with proper coordinates as in WGS84)
//		zoneGeometries.put("home1", new Coord((double) 0, (double) 1));
//		zoneGeometries.put("work1", new Coord((double) 50, (double) 0));
//	}
	private void fillZoneData() {
		zoneGeometries.put("home1", new Coord((double) 6.838324, (double) 47.646046));    // Home location
		zoneGeometries.put("work1", new Coord((double) 6.846274, (double) 47.646739));   // Work location
		zoneGeometries.put("school1", new Coord((double) 6.84401, (double) 47.64578)); // School location
		zoneGeometries.put("market1", new Coord((double) 6.84676, (double) 47.64568)); // Market location
	}


//	private void generatePopulation() {
//		generateHomeWorkHomeTrips("home1", "work1", 20); // create 20 trips from zone 'home1' to 'work1'
//		//... generate more trips here
//	}
	private void generatePopulation() {
		// Generate trips for home-work-home for 5 people
		generateHomeWorkHomeTrips("home1", "work1", 5);

		// Generate trips for home-school-market-home for 3 people
		generateHomeSchoolMarketHomeTrips("home1", "school1", "market1", 3);
	}


	private void generateHomeWorkHomeTrips(String from, String to, int quantity) {
		for (int i=0; i<quantity; ++i) {
			Coord source = zoneGeometries.get(from);
			Coord sink = zoneGeometries.get(to);
			Person person = population.getFactory().createPerson(createId(from, to, i, TransportMode.car));
			Plan plan = population.getFactory().createPlan();
			Coord homeLocation = shoot(ct.transform(source));
			Coord workLocation = shoot(ct.transform(sink));
			plan.addActivity(createHome(homeLocation));
			plan.addLeg(createDriveLeg());
			plan.addActivity(createWork(workLocation));
			plan.addLeg(createDriveLeg());
			plan.addActivity(createHome(homeLocation));
			person.addPlan(plan);
			population.addPerson(person);
		}
	}

	private void generateHomeSchoolMarketHomeTrips(String home, String school, String market, int quantity) {
		for (int i = 0; i < quantity; ++i) {
			Coord homeLocation = zoneGeometries.get(home);
			Coord schoolLocation = zoneGeometries.get(school);
			Coord marketLocation = zoneGeometries.get(market);

			Person person = population.getFactory().createPerson(createId(home, school, i, TransportMode.car));
			Plan plan = population.getFactory().createPlan();

			// Transform coordinates
			Coord transformedHome = shoot(ct.transform(homeLocation));
			Coord transformedSchool = shoot(ct.transform(schoolLocation));
			Coord transformedMarket = shoot(ct.transform(marketLocation));

			// Create the plan: home -> school -> market -> home
			plan.addActivity(createHome(transformedHome));
			plan.addLeg(createDriveLeg());
			plan.addActivity(createSchool(transformedSchool));
			plan.addLeg(createDriveLeg());
			plan.addActivity(createMarket(transformedMarket));
			plan.addLeg(createDriveLeg());
			plan.addActivity(createHome(transformedHome));

			// Add the plan to the person and add the person to the population
			person.addPlan(plan);
			population.addPerson(person);
		}
	}


	private Leg createDriveLeg() {
		Leg leg = population.getFactory().createLeg(TransportMode.car);
		return leg;
	}

	private Coord shoot(Coord source) {
		// Insert code here to blur the input coordinate.
		// For example, add a random number to the x and y coordinates.
		return source;
	}

	private Activity createWork(Coord workLocation) {
		Activity activity = population.getFactory().createActivityFromCoord("work", workLocation);
		activity.setEndTime(17*60*60);
		return activity;
	}

	private Activity createHome(Coord homeLocation) {
		Activity activity = population.getFactory().createActivityFromCoord("home", homeLocation);
		activity.setEndTime(9*60*60);
		return activity;
	}

	private Activity createSchool(Coord schoolLocation) {
		Activity activity = population.getFactory().createActivityFromCoord("school", schoolLocation);
		activity.setEndTime(15 * 60 * 60); // School ends at 3 PM
		return activity;
	}

	private Activity createMarket(Coord marketLocation) {
		Activity activity = population.getFactory().createActivityFromCoord("market", marketLocation);
		activity.setEndTime(18 * 60 * 60); // Market visit ends at 6 PM
		return activity;
	}

	private Id<Person> createId(String source, String sink, int i, String transportMode) {
		return Id.create(transportMode + "_" + source + "_" + sink + "_" + i, Person.class);
	}

}

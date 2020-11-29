import java.util.ArrayList;
import java.util.HashMap;

public class Utils {
    /**
     * Function to print out the population
     * @param population is a ArrayList that containts all the creatures
     */
    public printPopulation(ArrayList<HashMap> population) {
        int count = 0;
        // Loop through all the creatures
        for (HashMap creature: population) {
            ++count;
            // Print all the attributes and their values
            for (String attribute: creature.keySet()) {
                System.out.println(count + ": key: " + attribute + " value: " + creature.get(attribute));
            }
        }
    }
}

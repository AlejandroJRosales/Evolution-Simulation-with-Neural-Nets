import java.util.ArrayList;
import java.util.HashMap;

/**
 * Class that contains functions to generate populations,
 * creatures, weights for the environment, and neural network weight
 * @author aleja
 *
 */
public class Generate {
    private int[] populationSizes;
    private String[] speciesList = {"Charlen", "Gritis", "Drakonian"};
    private StartingAttributes attributes = new StartingAttributes();
    

    /**
     * Constructor function to initialize popuation sizes variable
     */
    Generate(int[] populationSizes) {
        this.populationSizes = populationSizes;
    }

    /**
     * This is a helper function generates a
     * Charlen to be added to the overall population
     * @return returns a hasmap contaning the charlen
     */
    public HashMap<String, Object> generateCharlen() {
        HashMap<String, Object> charlenAttributes = new HashMap<String, Object>();
        double randomHeight = attributes.CHARLENMINHEIGHT + (attributes.CHARLENMAXHEIGHT - attributes.CHARLENMINHEIGHT) * r.nextDouble();
        charlenAttributes.put("Height", randomHeight);
        return charlenAttributes;
    }
    
    /**
     * This is a helper function generates a 
     * Gritis to be added to the overall population
     * @return returns a hasmap contaning the charlen
     */
    public HashMap<String, Object> generateGritis() {
        HashMap<String, Object> gritisAttributes = new HashMap<String, Object>();
        double randomHeight = attributes.GRITISMINHEIGHT + (attributes.GRITISMAXHEIGHT - attributes.GRITISMINHEIGHT) * r.nextDouble();
        gritisAttributes.put("Height", randomHeight);
        return gritisAttributes;
    }
    
    /**
     * This is a helper function generates a
     * Drakonian to be added to the overall population
     * @return returns a hasmap contaning the charlen
     */
    public HashMap<String, Object> generateDrakonian() {
        HashMap<String, Object> drakonianAttributes = new HashMap<String, Object>();
        double randomHeight = attributes.DRAKONIANMINHEIGHT + (attributes.DRAKONIANMAXHEIGHT - attributes.DRAKONIANMINHEIGHT) * r.nextDouble();
        drakonianAttributes.put("Height", randomHeight);
        return drakonianAttributes;
    }
    
    /**
     * Helper function to chose which creature to generate based on
     * species index
     * @param speciesIndex is an int and is the position in the index for species list
     * @return returns a HashMap which is the creature
     */
    private HashMap<String, String> generateCreature(int speciesIndex) {
        if (speciesList[speciesIndex] == "Charlen") return generateCharlen();
        if (speciesList[speciesIndex] == "Gritis") return generateGritis();
        if (speciesList[speciesIndex] == "Drakonian") return generateDrakonian();
    }
    
    /**
     * This function generates the entire population when starting a new
     * population. It calls the other functions that generate the creatures
     * for the population
     * @return returns a list of hashmaps containing the different creatures pops
     */
    public ArrayList<HashMap> generatePopulation() {
        /*
            * Generate an ArrayList of hashmaps. The arraylist is the population
            * while the hashmaps contains the individual creatures
            */
        ArrayList<HashMap> population = new ArrayList<HashMap>();
        for (int speciesIndex = 0; speciesIndex < population.size(); ++speciesIndex) {
            population.add(generateCreature(speciesIndex));
        }
        return population;
    }
}

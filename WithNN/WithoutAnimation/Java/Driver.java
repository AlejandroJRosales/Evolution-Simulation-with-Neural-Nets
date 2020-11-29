import java.util.ArrayList;
import java.util.HashMap;

class Driver {
    private int[] populationSizes = {11, 11, 11};
    private Generate generate = new Generate(populationSizes);
    private Utils utils = new Utils();

    public static void main(String[] args) {
        ArrayList<HashMap> population = generate.generatePopulation();
        utils.printPopulation(population);
    }
}
using System;
using System.Collections.Specialized;
using System.Collections.Generic;

namespace Csharp
{
    class Program
    {
        static void Main(string[] args)
        {
            // dotnet new console
            // dotnet run

            // intialize main variables
            Dictionary<string, int> populationSizes = new Dictionary<string, int>();  
            // Adding key/value pairs
            populationSizes.Add("Drakonian", 10); 
            populationSizes.Add("Gritis", 10); 
            populationSizes.Add("Charlen", 10);

            // prints every x iteration
            int printEvery = 2;
            bool pause = true;

            Utils utils = new Utils();
            GeneratePopulation generatePopulation = new GeneratePopulation();

            // intialize the population as a list of dictionaries using the overloaded generatePopulation function
            ListDictionary population = generatePopulation.generateInitialPopulation(populationSizes);
            int iteration = 0;
            while (true){
                if (iteration % printEvery == 0){
                    Console.WriteLine("Hello World!");
                    utils.PrintKeysAndValues(population);
                    if (pause){
                        Console.WriteLine("PRESS ENTER TO CONTINUE");
                        Console.ReadLine();
                    }
                }

                iteration++;
            }
        }
    }
}

using System;
using System.Collections;
using System.Collections.Specialized;
using System.Collections.Generic;

namespace Csharp
{
    class GeneratePopulation
    {
        public Dictionary<string, double[]> traitsList = new Dictionary<string, double[]>();

        // public GeneratePopulation(){
        //     double[] ageRange = new double[2]{0, 21};
        //     traitsList.Add("Age", ageRange);
        //     double[] genRange = new double[2]{0, 1};
        //     traitsList.Add("Gen", tempRanges); 
        //     double[] healthRange = new double[2]{0, 21};
        //     traitsList.Add("Health", tempRanges);
        //     double[] ageRange = new double[2]{0, 21};
        //     traitsList.Add("Resources", tempRanges); 
        //     double[] ageRange = new double[2]{0, 21};
        //     traitsList.Add("Height", tempRanges); 
        //     double[] ageRange = new double[2]{0, 21};
        //     traitsList.Add("Weight", tempRanges);
        //     double[] ageRange = new double[2]{0, 21};
        //     traitsList.Add("Speed", tempRanges);
        //     double[] ageRange = new double[2]{0, 21}; 
        //     traitsList.Add("Power", tempRanges);
        // }

        public ListDictionary generateInitialPopulation(Dictionary<string, int> populationSizes){
            /**
            * @fn	ListDictionary generateInitialPopulation()
            * @brief	generates initial creates
            * @param	populationSizes
            * @return	ListDictionary of population containg creatures
            */
            ListDictionary population = new ListDictionary();
            // run through the list of species and population size for each species
            foreach(KeyValuePair<string, int> populationInfo in populationSizes){ 
              generatePopulation(populationInfo.Key, populationInfo.Value); 
            } 
            return population;
        }

        public ListDictionary generatePopulation(string species, int populationSize){
            /**
            * @fn	ListDictionary generatePopulation()
            * @brief	generates creates
            * @param	populationSize
            * @return	ListDictionary of population containg creatures
            */
            ListDictionary population = new ListDictionary();
            // create the individuals
            // for(int individual = 0; individual < populationSize; individual++) populationSize.Add(species, );
            return population;
        }
    }
}

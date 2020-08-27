using System;
using System.Collections;
using System.Collections.Specialized;

namespace Csharp
{
    class Utils 
    {
        public void PrintKeysAndValues(ListDictionary myCol){
            // Copies the ListDictionary to an array with DictionaryEntry elements.
            DictionaryEntry[] myArr = new DictionaryEntry[myCol.Count];
            myCol.CopyTo( myArr, 0 );

            Console.WriteLine( "   KEY                       VALUE" );
            foreach ( DictionaryEntry de in myCol )
                Console.WriteLine( "   {0,-25} {1}", de.Key, de.Value );
            Console.WriteLine();
        }
    }
}

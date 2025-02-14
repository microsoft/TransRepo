using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.IO;

namespace Com.Iluwatar.TypeObject
{
    /// <summary>
    /// The JsonParser class helps parse the json file candy.json to get all the different candies.
    /// </summary>
    public class JsonParser
    {
        private readonly Dictionary<string, Candy> candies;

        public JsonParser()
        {
        }

        public void Parse()
        {
            // Implement parsing logic here.
        }

        public void SetParentAndPoints()
        {
            // Implement logic here
        }

        public Dictionary<string, Candy> Candies => candies;
    }

    public class Candy
    {
        public enum Type
        {
            Chocolate,
            Lollipop
        }
    }
}
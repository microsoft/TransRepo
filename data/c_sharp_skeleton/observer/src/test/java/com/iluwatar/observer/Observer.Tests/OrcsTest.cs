using System;
using System.Collections.Generic;
using NUnit.Framework;

using Observer;

namespace Observer
{
    public class OrcsTest : WeatherObserverTest<Orcs>
    {
        public OrcsTest() : base(() => new Orcs())
        {
        }
    }
}

public class Orcs
{
    public string UpdateWeather(WeatherType weather)
    {
        return $"The orcs are facing {weather} weather now";
    }
}
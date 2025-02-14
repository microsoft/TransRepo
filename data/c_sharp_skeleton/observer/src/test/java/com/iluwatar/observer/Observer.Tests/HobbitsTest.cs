using System;
using System.Collections.Generic;
using NUnit.Framework;

namespace Observer
{
    public class HobbitsTest : WeatherObserverTest<Hobbits>
    {
        public HobbitsTest() : base(() => new Hobbits())
        {
        }
    }
}
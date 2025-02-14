using System;
using System.Collections.Generic;
using NUnit.Framework;
using Observer;

namespace Observer.Generic
{
    [TestFixture]
    public class GHobbitsTest : ObserverTest<GenHobbits>
    {
        public GHobbitsTest() : base(() => new GenHobbits())
        {
        }
    }
}
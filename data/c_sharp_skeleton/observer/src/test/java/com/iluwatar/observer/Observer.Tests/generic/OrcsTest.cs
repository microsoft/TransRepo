using System;
using System.Collections.Generic;
using NUnit.Framework;

namespace Observer.Generic
{
    class OrcsTest : ObserverTest<GenOrcs>
    {
        public OrcsTest() : base(() => new GenOrcs())
        {
        }
    }
}
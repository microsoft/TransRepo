using System;
using NUnit.Framework;

using Gameloop;

namespace Com.Iluwatar.Gameloop
{
    /// <summary>
    /// App unit test class.
    /// </summary>
    public class AppTest
    {
        [Test]
        
        [Category("ShouldExecuteApplicationWithoutException")]
        public void ShouldExecuteApplicationWithoutException()
        {
            Assert.DoesNotThrow(() => App.Main(new string[] { }));
        }
    }
}

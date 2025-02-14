using System;
using NUnit.Framework;

namespace Observer
{
    /// <summary>
    /// Application test.
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
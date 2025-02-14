using System;
using NUnit.Framework;


namespace Com.Iluwatar.Caching
{
    [TestFixture]
    public class AppTest
    {
        [Test]
        
        [Category("ShouldExecuteApplicationWithoutException")]
        public void ShouldExecuteApplicationWithoutException()
        {
            Assert.DoesNotThrow(() => App.Main(Array.Empty<string>()));
        }
    }
}
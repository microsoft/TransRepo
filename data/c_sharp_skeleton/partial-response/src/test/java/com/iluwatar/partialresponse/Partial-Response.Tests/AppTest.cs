using System;
using NUnit.Framework;

namespace Com.Iluwatar.Partialresponse
{
    [TestFixture]
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
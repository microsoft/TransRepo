using System;
using NUnit.Framework;

namespace Promise
{
    [TestFixture]
    public class AppTest
    {
        [Test]
        [Timeout(20000)]
        [Category("ShouldExecuteApplicationWithoutException")]
        public void ShouldExecuteApplicationWithoutException()
        {
            Assert.DoesNotThrow(() => App.Main(null));
        }
    }
}
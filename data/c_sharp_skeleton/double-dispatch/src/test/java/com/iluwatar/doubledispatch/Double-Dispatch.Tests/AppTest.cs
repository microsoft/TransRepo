using System;
using NUnit.Framework;

using com.iluwatar.doubledispatch;

namespace Com.Iluwatar.Doubledispatch
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
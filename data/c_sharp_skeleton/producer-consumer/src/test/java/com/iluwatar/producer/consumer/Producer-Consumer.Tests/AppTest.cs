using System;
using NUnit.Framework;

using ProducerConsumerPattern;

namespace Com.Iluwatar.Producer.Consumer
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
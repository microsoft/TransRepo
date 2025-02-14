using System;
using NUnit.Framework;

using ProducerConsumerPattern;

namespace Com.Iluwatar.Producer.Consumer
{
    [TestFixture]
    public class AppTest
    {
        [Test]
        public void ShouldExecuteApplicationWithoutException()
        {
            Assert.DoesNotThrow(() => App.Main(Array.Empty<string>()));
        }
    }
}
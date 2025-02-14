using System;
using System.Threading.Tasks;
using Moq;
using NUnit.Framework;

using ProducerConsumer;
using com.iluwatar.producer.consumer;

namespace Com.Iluwatar.ProducerConsumer
{
    [TestFixture]
    public class ProducerTest
    {
        [Test]
        public async Task TestProduce()
        {
            var cts = new System.Threading.CancellationTokenSource();
            cts.CancelAfter(TimeSpan.FromMilliseconds(6000));
            try
            {
                var queue = new Mock<ItemQueue>();
                var producer = new com.iluwatar.producer.consumer.Producer("producer", queue.Object);

                producer.Produce();
                queue.Verify(q => q.Put(It.IsAny<Item>()), Times.Once);

                queue.VerifyNoOtherCalls();
            }
            catch (TaskCanceledException)
            {
                Assert.Fail("Test took too long to execute");
            }
        }
    }
}
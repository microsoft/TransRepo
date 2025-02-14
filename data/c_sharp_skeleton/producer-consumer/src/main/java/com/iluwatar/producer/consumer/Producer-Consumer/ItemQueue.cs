using System.Collections.Concurrent;

using com.iluwatar.producer.consumer;

namespace ProducerConsumer
{
    /// <summary>
    /// Class as a channel for Producer-Consumer exchange.
    /// </summary>
    public class ItemQueue
    {
        private readonly BlockingCollection<Item> queue;

        public ItemQueue()
        {
            queue = new BlockingCollection<Item>();
        }

        public void Put(Item item)
        {
            queue.Add(item);
        }

        public Item Take()
        {
            return queue.Take();
        }
    }
}
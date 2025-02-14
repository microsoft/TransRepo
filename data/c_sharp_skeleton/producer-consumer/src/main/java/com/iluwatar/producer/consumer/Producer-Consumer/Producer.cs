using System;
using System.Security.Cryptography;

using ProducerConsumer;

namespace com.iluwatar.producer.consumer
{
    /// <summary>
    /// Class responsible for producing unit of work that can be expressed as <see cref="Item"/>
    /// and submitted to queue.
    /// </summary>
    public class Producer
    {
        private static readonly RandomNumberGenerator RANDOM = RandomNumberGenerator.Create();

        private readonly ItemQueue _queue;

        private readonly string _name;

        private int _itemId;

        public Producer(string name, ItemQueue queue)
        {
            _name = name;
            _queue = queue;
        }

        /// <summary>
        /// Put item in the queue.
        /// </summary>
        public void Produce()
        {
            //_insert logic for producing items and putting them in the queue
        }
    }
}

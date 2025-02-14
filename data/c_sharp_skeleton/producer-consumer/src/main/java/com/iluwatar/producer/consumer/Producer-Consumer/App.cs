using System;
using System.Threading;
using System.Threading.Tasks;

namespace ProducerConsumerPattern
{
    /// <summary>
    /// Producer Consumer Design pattern is a classic concurrency or threading pattern which reduces
    /// coupling between Producer and Consumer by separating Identification of work with Execution of
    /// Work.
    ///
    /// In producer consumer design pattern a shared queue is used to control the flow and this
    /// separation allows you to code producer and consumer separately. It also addresses the issue of
    /// different timing require to produce item or consuming item. by using producer consumer pattern
    /// both Producer and Consumer Thread can work with different speed.
    /// </summary>
    public class App
    {
        /// <summary>
        /// Program entry point.
        /// </summary>
        /// <param name="args">command line args</param>
        public static void Main(string[] args)
        {
            return;
        }
    }
}

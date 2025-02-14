using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;
using NLog;

namespace Promise
{
    public class App
    {
        private static readonly string DefaultUrl = "https://raw.githubusercontent.com/iluwatar/java-design-patterns/master/promise/README.md";
        private readonly CountdownEvent stopLatch;
        private static readonly Logger Logger = LogManager.GetCurrentClassLogger();

        private App()
        {
        }

        public static void Main(string[] args)
        {
        }

        private void PromiseUsage()
        {
        }

        private void CalculateLowestFrequencyChar()
        {
        }

        private void CalculateLineCount()
        {
        }

        private Task<Dictionary<char, long>> CharacterFrequency()
        {
            return null;
        }

        private Task<char> LowestFrequencyChar()
        {
            return null;
        }

        private Task<int> CountLines()
        {
            return null;
        }

        private async Task<string> Download(string urlString)
        {
            return null;
        }

        private async Task Stop()
        {
        }

        private void TaskCompleted()
        {
        }
    }
}

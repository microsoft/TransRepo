using System;
using System.Collections.Generic;
using Microsoft.Extensions.Logging;

namespace Com.Iluwatar.Partialresponse
{
    /// <summary>
    /// The Partial response pattern is a design pattern in which client specifies fields to fetch to
    /// serve. Here <see cref="App"/> is playing as client for <see cref="VideoResource"/> server. Client ask for
    /// specific fields information in video to server.
    ///
    /// <see cref="VideoResource"/> act as server to serve video information.
    /// </summary>
    public class App
    {
        private static readonly ILogger<App> _logger;

        /// <summary>
        /// Method as act client and request to server for video details.
        /// </summary>
        /// <param name="args">Program arguments</param>
        public static void Main(string[] args)
        {
            return;
        }
    }
}
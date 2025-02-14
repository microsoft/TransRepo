using System;
using System.Security.Cryptography;
using Microsoft.Extensions.Logging;

namespace Com.Iluwatar.Gameloop
{
    /// <summary>
    /// Abstract class for GameLoop implementation class.
    /// </summary>
    public abstract class GameLoop
    {
        protected readonly ILogger logger = LoggerFactory.Create(builder => builder.AddConsole()).CreateLogger<GameLoop>();

        protected internal volatile GameStatus status;
        public GameStatus Status => status;

        public readonly GameController controller;

        /// <summary>
        /// Initialize game status to be stopped.
        /// </summary>
        protected GameLoop()
        {
        }

        /// <summary>
        /// Run game loop.
        /// </summary>
        public void Run()
        {
        }

        /// <summary>
        /// Stop game loop.
        /// </summary>
        public void Stop()
        {
        }

        /// <summary>
        /// Check if game is running or not.
        /// </summary>
        /// <returns>true if the game is running.</returns>
        public bool IsGameRunning()
        {
            return true;
        }

        /// <summary>
        /// Handle any user input that has happened since the last call. In order to
        /// simulate the situation in real-life game, here we add a random time lag.
        /// The time lag ranges from 50 ms to 250 ms.
        /// </summary>
        protected void ProcessInput()
        {
        }

        /// <summary>
        /// Render game frames to screen. Here we print bullet position to simulate
        /// this process.
        /// </summary>
        protected void Render()
        {
        }

        /// <summary>
        /// Execute game loop logic.
        /// </summary>
        protected abstract void ProcessGameLoop();
    }
}
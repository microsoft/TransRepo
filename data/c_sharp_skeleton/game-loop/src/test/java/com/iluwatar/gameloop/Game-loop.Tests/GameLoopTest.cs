using System;
using NUnit.Framework;

using Gameloop;


namespace Com.Iluwatar.Gameloop
{
    /**
     * GameLoop unit test class.
     */
    class LocalGameLoop : GameLoop
    {
        protected override void ProcessGameLoop()
        {
            // Implementation here
        }

        public void SetStatus(GameStatus newStatus)
        {
            this.status = newStatus;
        }
    }

    [TestFixture]
    public class GameLoopTest
    {
        private LocalGameLoop gameLoop;

        /**
         * Create mock implementation of GameLoop.
         */
        [SetUp]
        public void Setup()
        {
            gameLoop = new LocalGameLoop();
        }

        [TearDown]
        public void Teardown()
        {
            gameLoop = null;
        }

         [Test]
        [Category("TestRun")]
        public void TestRun()
        {
            gameLoop.SetStatus(GameStatus.STOPPED);
            
            gameLoop.Run();
            Assert.AreEqual(GameStatus.RUNNING, gameLoop.Status);
        }

        [Test]
        [Category("TestStop")]
        public void TestStop()
        {
            gameLoop.SetStatus(GameStatus.RUNNING);
            
            gameLoop.Stop();
            Assert.AreEqual(GameStatus.STOPPED, gameLoop.Status);
        }

        [Test]
        [Category("TestIsGameRunning")]
        public void TestIsGameRunning()
        {
            Assert.False(gameLoop.IsGameRunning());
        }
    }
}
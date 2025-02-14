using System;
using System.Collections.Generic;
using NUnit.Framework;

using Gameloop;

namespace Com.Iluwatar.Gameloop
{
    /// <summary>
    /// FrameBasedGameLoop unit test class.
    /// </summary>
    public class FrameBasedGameLoopTest
    {
        private FrameBasedGameLoop gameLoop;

        [SetUp]
        public void Setup()
        {
            gameLoop = new FrameBasedGameLoop();
        }

        [TearDown]
        public void TearDown()
        {
            gameLoop = null;
        }

        [Test]
        

        [Category("TestUpdateFrameBasedGameLoop")]
        public void TestUpdate()
        {
            gameLoop.Update();
            Assert.AreEqual(0.5f, gameLoop.controller.GetBulletPosition(), 0);
        }
    }
}
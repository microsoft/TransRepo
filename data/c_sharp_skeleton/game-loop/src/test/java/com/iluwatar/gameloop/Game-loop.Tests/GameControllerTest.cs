using System.Collections.Generic;
using NUnit.Framework;

namespace Com.Iluwatar.Gameloop
{
    [TestFixture]
    public class GameControllerTest
    {
        private GameController controller;

        [SetUp]
        public void Setup()
        {
            controller = new GameController();
        }

        [TearDown]
        public void TearDown()
        {
            controller = null;
        }

        [Test]
        [Category("TestMoveBullet")]
        public void TestMoveBullet()
        {
            controller.MoveBullet(1.5f);
            Assert.AreEqual(1.5f, controller.Bullet.Position, 0);
        }

        [Test]
        [Category("TestGetBulletPosition")]
        public void TestGetBulletPosition()
        {
            Assert.AreEqual(controller.Bullet.Position, controller.GetBulletPosition(), 0);
        }
    }
}
using NUnit.Framework;
using System.Collections.Generic;

namespace Com.Iluwatar.Doubledispatch
{
    /**
     * FlamingAsteroidTest
     *
     */
    class FlamingAsteroidTest : CollisionTest<FlamingAsteroid>
    {
        protected override FlamingAsteroid GetTestedObject()
        {
            return new FlamingAsteroid(1, 2, 3, 4);
        }

        /**
         * Test the constructor parameters
         */
        [Test]
        
        [Category("TestConstructorFlamingAsteroid")]
        public void TestConstructorFlamingAsteroid()
        {
            var asteroid = new FlamingAsteroid(1, 2, 3, 4);
            Assert.AreEqual(1, asteroid.Left);
            Assert.AreEqual(2, asteroid.Top);
            Assert.AreEqual(3, asteroid.Right);
            Assert.AreEqual(4, asteroid.Bottom);
            Assert.IsTrue(asteroid.OnFire);
            Assert.IsFalse(asteroid.Damaged);
            Assert.AreEqual("FlamingAsteroid at [1,2,3,4] damaged=False onFire=True", asteroid.ToString());
        }

        /**
         * Test what happens we collide with an asteroid
         */
        [Test]
        
        [Category("TestCollideFlamingAsteroidFlamingAsteroid")]
        public void TestCollideFlamingAsteroid()
        {
            TestCollision(
                new FlamingAsteroid(1, 2, 3, 4),
                false, true,
                false, true
            );
        }

        /**
         * Test what happens we collide with a meteoroid
         */
        [Test]
        
        [Category("TestCollideMeteoroidFlamingAsteroid")]
        public void TestCollideMeteoroid()
        {
            TestCollision(
                new Meteoroid(1, 1, 3, 4),
                false, false,
                false, true
            );
        }

        /**
         * Test what happens we collide with ISS
         */
        [Test]
        
        [Category("TestCollideSpaceStationIssFlamingAsteroid")]
        public void TestCollideSpaceStationIss()
        {
            TestCollision(
                new SpaceStationIss(1, 1, 3, 4),
                true, true,
                false, true
            );
        }

        /**
         * Test what happens we collide with MIR
         */
        [Test]
        
        [Category("TestCollideSpaceStationMirFlamingAsteroid")]
        public void TestCollideSpaceStationMir()
        {
            TestCollision(
                new SpaceStationMir(1, 1, 3, 4),
                true, true,
                false, true
            );
        }
    }
}
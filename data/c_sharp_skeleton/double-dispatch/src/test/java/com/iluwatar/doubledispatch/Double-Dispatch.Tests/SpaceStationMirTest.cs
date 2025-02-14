using System;
using System.Collections.Generic;
using NUnit.Framework;


namespace Com.Iluwatar.Doubledispatch
{
    [TestFixture]
    class SpaceStationMirTest : CollisionTest<SpaceStationMir>
    {
        protected override SpaceStationMir GetTestedObject()
        {
            return new SpaceStationMir(1, 2, 3, 4);
        }

        [Test]
        

        [Category("TestConstructorSpaceStationMir")]
        public void TestConstructorSpaceStationMir()
        {
            var mir = new SpaceStationMir(1, 2, 3, 4);
            Assert.AreEqual(1, mir.Left);
            Assert.AreEqual(2, mir.Top);
            Assert.AreEqual(3, mir.Right);
            Assert.AreEqual(4, mir.Bottom);
            Assert.False(mir.OnFire);
            Assert.False(mir.Damaged);
            Assert.AreEqual("SpaceStationMir at [1,2,3,4] damaged=false onFire=false", mir.ToString());
        }

        [Test]
        

        [Category("TestCollideFlamingAsteroidSpaceStationMir")]
        public void TestCollideFlamingAsteroid()
        {
            TestCollision(
                new FlamingAsteroid(1, 1, 3, 4),
                false, true,
                false, false
            );
        }

        [Test]
        

        [Category("TestCollideMeteoroidSpaceStationMir")]
        public void TestCollideMeteoroid()
        {
            TestCollision(
                new Meteoroid(1, 1, 3, 4),
                false, false,
                false, false
            );
        }

        [Test]
        

        [Category("TestCollideSpaceStationIssSpaceStationMir")]
        public void TestCollideSpaceStationIss()
        {
            TestCollision(
                new SpaceStationIss(1, 1, 3, 4),
                true, false,
                false, false
            );
        }

        [Test]
        

        [Category("TestCollideSpaceStationMirSpaceStationMir")]
        public void TestCollideSpaceStationMir()
        {
            TestCollision(
                new SpaceStationMir(1, 1, 3, 4),
                true, false,
                false, false
            );
        }
    }
}
using System;
using System.Collections.Generic;
using NUnit.Framework;

namespace Com.Iluwatar.Doubledispatch
{
  [TestFixture]
  class MeteoroidTest : CollisionTest<Meteoroid>
  {
    protected override Meteoroid GetTestedObject()
    {
      return new Meteoroid(1, 2, 3, 4);
    }

    [Test]
    

    [Category("TestConstructorMeteoroid")]
    public void TestConstructorMeteoroid()
    {
      var meteoroid = new Meteoroid(1, 2, 3, 4);
      Assert.AreEqual(1, meteoroid.Left);
      Assert.AreEqual(2, meteoroid.Top);
      Assert.AreEqual(3, meteoroid.Right);
      Assert.AreEqual(4, meteoroid.Bottom);
      Assert.IsFalse(meteoroid.OnFire);
      Assert.IsFalse(meteoroid.Damaged);
      Assert.AreEqual("Meteoroid at [1,2,3,4] damaged=false onFire=false", meteoroid.ToString());
    }

    [Test]
    

    [Category("TestCollideFlamingAsteroidMeteoroid")]
    public void TestCollideFlamingAsteroid()
    {
      TestCollision(
          new FlamingAsteroid(1, 1, 3, 4),
          false, true,
          false, false
      );
    }

    [Test]
    

    [Category("TestCollideMeteoroidMeteoroid")]
    public void TestCollideMeteoroid()
    {
      TestCollision(
          new Meteoroid(1, 1, 3, 4),
          false, false,
          false, false
      );
    }

    [Test]
    

    [Category("TestCollideSpaceStationIssMeteoroid")]
    public void TestCollideSpaceStationIss()
    {
      TestCollision(
          new SpaceStationIss(1, 1, 3, 4),
          true, false,
          false, false
      );
    }

    [Test]
    

    [Category("TestCollideSpaceStationMirMeteoroid")]
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
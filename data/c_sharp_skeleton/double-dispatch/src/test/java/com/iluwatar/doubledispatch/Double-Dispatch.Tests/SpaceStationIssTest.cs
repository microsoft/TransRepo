/*
 * This project is licensed under the MIT license. Module model-view-viewmodel is using ZK framework licensed under LGPL (see lgpl-3.0.txt).
 *
 * The MIT License
 * Copyright © 2014-2022 Ilkka Seppälä
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

using System.Collections.Generic;
using NUnit.Framework;


namespace Com.Iluwatar.Doubledispatch
{
    /**
     * SpaceStationIssTest
     *
     */
    class SpaceStationIssTest : CollisionTest<SpaceStationIss>
    {
        protected override SpaceStationIss GetTestedObject()
        {
            return new SpaceStationIss(1, 2, 3, 4);
        }

        /**
         * Test the constructor parameters
         */
        [Test]
        
        [Category("TestConstructorSpaceStationIss")]
        public void TestConstructorSpaceStationIss()
        {
            var iss = new SpaceStationIss(1, 2, 3, 4);
            Assert.AreEqual(1, iss.Left);
            Assert.AreEqual(2, iss.Top);
            Assert.AreEqual(3, iss.Right);
            Assert.AreEqual(4, iss.Bottom);
            Assert.IsFalse(iss.OnFire);
            Assert.IsFalse(iss.Damaged);
            Assert.AreEqual("SpaceStationIss at [1,2,3,4] damaged=false onFire=false", iss.ToString());
        }

        /**
         * Test what happens we collide with an asteroid
         */
        [Test]
        
        [Category("TestCollideFlamingAsteroidSpaceStationIss")]
        public void TestCollideFlamingAsteroid()
        {
            TestCollision(
                new FlamingAsteroid(1, 1, 3, 4),
                false, true,
                false, false
            );
        }

        /**
         * Test what happens we collide with a meteoroid
         */
        [Test]
        
        [Category("TestCollideMeteoroidSpaceStationIss")]
        public void TestCollideMeteoroid()
        {
            TestCollision(
                new Meteoroid(1, 1, 3, 4),
                false, false,
                false, false
            );
        }

        /**
         * Test what happens we collide with ISS
         */
        [Test]
        
        [Category("TestCollideSpaceStationIssSpaceStationIss")]
        public void TestCollideSpaceStationIss()
        {
            TestCollision(
                new SpaceStationIss(1, 1, 3, 4),
                true, false,
                false, false
            );
        }

        /**
         * Test what happens we collide with MIR
         */
        [Test]
        
        [Category("TestCollideSpaceStationMirSpaceStationIss")]
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
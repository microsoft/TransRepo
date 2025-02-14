using System;
using System.Collections.Generic;
using NUnit.Framework;
using Moq;
using System.Linq;

using Observer.Utils;

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

namespace Observer.Generic
{
    [TestFixture]
    public abstract class ObserverTest<O> where O : IObserver
    {
        private InMemoryAppender appender;

        [SetUp]
        public void SetUp()
        {
            appender = new InMemoryAppender();
        }

        [TearDown]
        public void TearDown()
        {
            appender.Dispose();
        }

        private readonly Func<O> factory;

        protected ObserverTest(Func<O> factory)
        {
            this.factory = factory;
        }

        public static IEnumerable<object[]> dataProvider() {
            return new List<object[]>
            {
                new object[] { WeatherType.Sunny, "The orcs are facing Sunny weather now" },
                new object[] { WeatherType.Rainy, "The orcs are facing Rainy weather now" },
                new object[] { WeatherType.Windy, "The orcs are facing Windy weather now" },
                new object[] { WeatherType.Cold, "The orcs are facing Cold weather now" }
            };
        }

        [Test, TestCaseSource(nameof(dataProvider))]
        public void TestObserver(WeatherType weather, string response)
        {
            var observer = this.factory();
            Assert.AreEqual(0, appender.GetLogSize());

            observer.Update(null, weather);
            Assert.AreEqual(response, appender.GetLastMessage());
            Assert.AreEqual(1, appender.GetLogSize());
        }
    }
}
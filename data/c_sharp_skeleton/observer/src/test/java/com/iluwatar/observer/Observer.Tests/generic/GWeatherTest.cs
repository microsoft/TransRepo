using System;
using NUnit.Framework;
using Moq;
using System.Linq;
using System.Collections.Generic;

using Observer;
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
    public class GWeatherTest
    {
        private InMemoryAppender appender;

        [SetUp]
        public void SetUp()
        {
            appender = new InMemoryAppender(typeof(GenWeather));
        }

        [TearDown]
        public void TearDown()
        {
            appender.Dispose();
        }

        [Test]
        

        [Category("TestAddRemoveObserver")]
        public void TestAddRemoveObserver()
        {
            var observer = new Mock<Race>();

            var weather = new GenWeather();
            weather.AddObserver(observer.Object);
            observer.VerifyNoOtherCalls();

            weather.TimePasses();
            Assert.AreEqual("The weather changed to rainy.", appender.GetLastMessage());
            observer.Verify(o => o.Update(weather, WeatherType.Rainy));

            weather.RemoveObserver(observer.Object);
            weather.TimePasses();
            Assert.AreEqual("The weather changed to windy.", appender.GetLastMessage());

            observer.VerifyNoOtherCalls();
            Assert.AreEqual(2, appender.GetLogSize());
        }

        [Test]
        

        [Category("TestTimePasses")]
        public void TestTimePasses()
        {
            var observer = new Mock<Race>();
            var weather = new GenWeather();
            weather.AddObserver(observer.Object);

            // 使用 MockSequence 确保调用顺序
            var sequence = new MockSequence();

            var weatherTypes = (WeatherType[])Enum.GetValues(typeof(WeatherType));
            for (var i = 1; i < 20; i++)
            {
                weather.TimePasses();

                // 在 Mock 上调用 Verify，同时指定 MockSequence
                observer.InSequence(sequence).Setup(o => o.Update(weather, weatherTypes[i % weatherTypes.Length]));
            }

            // 重新验证调用
            foreach (var i in Enumerable.Range(1, 19))
            {
                observer.Verify(o => o.Update(weather, weatherTypes[i % weatherTypes.Length]), Times.Once);
            }

            // 验证没有其他调用
            observer.VerifyNoOtherCalls();
        }
    }
}
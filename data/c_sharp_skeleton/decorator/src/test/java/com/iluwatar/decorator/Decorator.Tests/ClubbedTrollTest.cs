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
using NUnit.Framework;
using Moq;

using PatternMatching;
using Decorator;

namespace DecoratorPattern.Tests
{
    [TestFixture]
    public class ClubbedTrollTest
    {
        [Test]
        
        [Category("TestClubbedTroll")]
        public void TestClubbedTroll()
        {
            // Create a normal troll first, but make sure we can spy on it later on.
            var simpleTrollMock = new Mock<SimpleTroll>();
            var simpleTroll = simpleTrollMock.Object;

            // Now we want to decorate the troll to make it stronger ...
            var clubbed = new ClubbedTroll(simpleTroll);
            Assert.AreEqual(20, clubbed.GetAttackPower());
            simpleTrollMock.Verify(t => t.GetAttackPower(), Times.Once);

            // Check if the clubbed troll actions are delegated to the decorated troll
            clubbed.Attack();
            simpleTrollMock.Verify(t => t.Attack(), Times.Once);

            clubbed.FleeBattle();
            simpleTrollMock.Verify(t => t.FleeBattle(), Times.Once);
            simpleTrollMock.VerifyNoOtherCalls();
        }
    }
}
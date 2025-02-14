using System;
using System.Collections.Generic;
using NUnit.Framework;
using System.Reflection;

using PatternMatching;
using Com.Iluwatar.Doublebuffer;

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

namespace DoubleBuffer
{
    /**
    * FrameBuffer unit test.
    */
    [TestFixture]
    public class FrameBufferTest
    {
        [Test]
        
        [Category("TestClearAll")]
        public void TestClearAll()
        {
            try
            {
                var field = typeof(FrameBuffer).GetField("pixels", BindingFlags.NonPublic | BindingFlags.Instance);
                if (field == null)
                {
                    Assert.Fail("Fail to find field.");
                    return;
                }

                var pixels = new Pixel[FrameBuffer.HEIGHT * FrameBuffer.WIDTH];
                Array.Fill(pixels, Pixel.WHITE);
                pixels[0] = Pixel.BLACK;
                var frameBuffer = new FrameBuffer();
                field.SetValue(frameBuffer, pixels);
                frameBuffer.ClearAll();
                Assert.AreEqual(Pixel.WHITE, frameBuffer.GetPixels()[0]);
            }
            catch (Exception)
            {
                Assert.Fail("Fail to modify field access.");
            }
        }

        [Test]
        

        [Category("TestClear")]
        public void TestClear()
        {
            try
            {
                var field = typeof(FrameBuffer).GetField("pixels", BindingFlags.NonPublic | BindingFlags.Instance);
                if (field == null)
                {
                    Assert.Fail("Fail to find field.");
                    return;
                }

                var pixels = new Pixel[FrameBuffer.HEIGHT * FrameBuffer.WIDTH];
                Array.Fill(pixels, Pixel.WHITE);
                pixels[0] = Pixel.BLACK;
                var frameBuffer = new FrameBuffer();
                field.SetValue(frameBuffer, pixels);
                frameBuffer.Clear(0, 0);
                Assert.AreEqual(Pixel.WHITE, frameBuffer.GetPixels()[0]); 
            }
            catch (Exception)
            {
                Assert.Fail("Fail to modify field access.");
            }
        }

        [Test]
        

        [Category("TestDraw")]
        public void TestDraw()
        {
            var frameBuffer = new FrameBuffer();
            frameBuffer.Draw(0, 0);
            Assert.AreEqual(Pixel.BLACK, frameBuffer.GetPixels()[0]);
        }

        [Test]
        

        [Category("TestGetPixels")]
        public void TestGetPixels()
        {
            try
            {
                var field = typeof(FrameBuffer).GetField("pixels", BindingFlags.NonPublic | BindingFlags.Instance);
                if (field == null)
                {
                    Assert.Fail("Fail to find field.");
                    return;
                }

                var pixels = new Pixel[FrameBuffer.HEIGHT * FrameBuffer.WIDTH];
                Array.Fill(pixels, Pixel.WHITE);
                pixels[0] = Pixel.BLACK;
                var frameBuffer = new FrameBuffer();
                field.SetValue(frameBuffer, pixels);
                Assert.AreEqual(pixels, frameBuffer.GetPixels());
            }
            catch (Exception)
            {
                Assert.Fail("Fail to modify field access.");
            }
        }
    }
}
using System;
using System.Collections.Generic;
using System.Reflection;
using NUnit.Framework;

using PatternMatching;
using Com.Iluwatar.DoubleBuffer;

namespace com.iluwatar.doublebuffer
{
    public class SceneTest
    {
        [Test]
        
        [Category("TestGetBuffer")]
        public void TestGetBuffer()
        {
            try
            {
                var scene = new Scene();
                var currentField = typeof(Scene).GetField("current", BindingFlags.NonPublic | BindingFlags.Instance);
                currentField.SetValue(scene, 0);
                var frameBuffers = new FrameBuffer[2];
                var frameBuffer = new FrameBuffer();
                frameBuffer.Draw(0, 0);
                frameBuffers[0] = frameBuffer;
                var frameBuffersField = typeof(Scene).GetField("frameBuffers", BindingFlags.NonPublic | BindingFlags.Instance);
                frameBuffersField.SetValue(scene, frameBuffers);
                Assert.AreEqual(frameBuffer, scene.GetBuffer());
            }
            catch (FieldAccessException)
            {
                Assert.Fail("Fail to access private field.");
            }
        }

        [Test]
        

        [Category("TestDraw")]
        public void TestDraw()
        {
            try
            {
                var scene = new Scene();
                var currentField = typeof(Scene).GetField("current", BindingFlags.NonPublic | BindingFlags.Instance);
                var nextField = typeof(Scene).GetField("next", BindingFlags.NonPublic | BindingFlags.Instance);
                currentField.SetValue(scene, 0);
                nextField.SetValue(scene, 1);
                scene.Draw(new List<System.Tuple<int, int>>());
                Assert.AreEqual(1, (int)currentField.GetValue(scene));
                Assert.AreEqual(0, (int)nextField.GetValue(scene));
            }
            catch (FieldAccessException)
            {
                Assert.Fail("Fail to access private field");
            }
        }
    }
}
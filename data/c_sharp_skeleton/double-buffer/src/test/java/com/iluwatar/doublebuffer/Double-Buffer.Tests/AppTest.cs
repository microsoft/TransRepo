using System;
using NUnit.Framework;

using DoubleBuffer;

namespace Com.Iluwatar.Doublebuffer
{
    /// <summary>
    /// App unit test.
    /// </summary>
    public class AppTest
    {
        /// <summary>
        /// Issue: Add at least one assertion to this test case.
        /// Solution: Inserted assertion to check whether the execution of the main method in <see cref="App.Main(string[])"/>
        /// throws an exception.
        /// </summary>
        [Test]
        
        [Category("ShouldExecuteApplicationWithoutException")]
        public void ShouldExecuteApplicationWithoutException()
        {
            Assert.DoesNotThrow(() => App.Main(new string[] { }));
        }
    }
}
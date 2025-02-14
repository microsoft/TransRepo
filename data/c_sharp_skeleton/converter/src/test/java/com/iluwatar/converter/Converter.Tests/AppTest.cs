using System;
using NUnit.Framework;

namespace Com.Iluwatar.Converter
{
    [TestFixture]
    public class AppTest
    {
        /**
         * Issue: Add at least one assertion to this test case.
         * Solution: Inserted assertion to check whether the execution of the main method in {@link App#main(String[])}
         * throws an exception.
         */
        [Test]
        
        [Category("ShouldExecuteApplicationWithoutException")]
        public void ShouldExecuteApplicationWithoutException()
        {
            Assert.DoesNotThrow(() => App.Main(new string[] { }));
        }
    }
}
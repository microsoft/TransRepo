using System;
using NUnit.Framework;

namespace com.iluwatar.unitofwork
{
    [TestFixture]
    public class AppTest 
    {
        [Test]
        
        [Category("ShouldExecuteWithoutException")]
        public void ShouldExecuteWithoutException() 
        {
            Assert.DoesNotThrow(() => App.Main(new string[]{}));
        }
    }
}
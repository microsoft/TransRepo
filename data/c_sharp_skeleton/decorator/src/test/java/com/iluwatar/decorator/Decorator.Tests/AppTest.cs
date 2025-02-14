using System;
using NUnit.Framework;

namespace Com.Iluwatar.Decorator
{
    public class AppTest
    {
        [Test]
        
        [Category("ShouldExecuteApplicationWithoutException")]
        public void ShouldExecuteApplicationWithoutException()
        {
            Assert.DoesNotThrow(() => App.Main(new string[] { }));
        }
    }

    // public class App
    // {
    //     public static void Main(string[] args)
    //     {
    //         // Application logic here
    //     }
    // }
}
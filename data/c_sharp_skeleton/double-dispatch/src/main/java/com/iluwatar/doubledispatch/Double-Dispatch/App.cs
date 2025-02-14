using System;
using System.Collections.Generic;
using NLog;

namespace Com.Iluwatar.Doubledispatch
{
    /// <summary>
    /// When a message with a parameter is sent to an object, the resultant behavior is defined by the
    /// implementation of that method in the receiver. Sometimes the behavior must also be determined by
    /// the type of the parameter.
    /// 
    /// One way to implement this would be to create multiple instanceof-checks for the methods
    /// parameter. However, this creates a maintenance issue. When new types are added we would also need
    /// to change the method's implementation and add a new instanceof-check. This violates the single
    /// responsibility principle - a class should have only one reason to change.
    /// 
    /// Instead of the instanceof-checks a better way is to make another virtual call on the
    /// parameter object. This way new functionality can be easily added without the need to modify
    /// existing implementation (open-closed principle).
    /// 
    /// In this example we have hierarchy of objects { get;that can collide to each; other. Each object 
    /// has its own coordinates which are checked against the other objects'
    /// coordinates. If there is an overlap, then the objects collide utilizing the Double Dispatch
    /// pattern.
    /// </summary>
    public class App
    {
        private static readonly Logger Logger = LogManager.GetCurrentClassLogger();

        /// <summary>
        /// Program entry point.
        /// </summary>
        /// <param name="args">command line args</param>
        public static void Main(string[] args)
        {
            return;
        }
    }
}
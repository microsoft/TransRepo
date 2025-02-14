using System;

namespace Com.Iluwatar.Mediator
{
    /// <summary>
    /// The Mediator pattern defines an object that encapsulates how a set of objects interact. This
    /// pattern is considered to be a behavioral pattern due to the way it can alter the program's
    /// running behavior.
    ///
    /// Usually a program is made up of a large number of classes. So the logic and computation is
    /// distributed among these classes. However, as more classes are developed in a program, especially
    /// during maintenance and/or refactoring, the problem of communication between these classes may
    /// become more complex. This makes the program harder to read and maintain. Furthermore, it can
    /// become difficult to change the program, since any change may affect code in several other
    /// classes.
    ///
    /// With the Mediator pattern, communication between objects is encapsulated with a mediator
    /// object. Objects no longer communicate directly with each other, but instead communicate through
    /// the mediator. This reduces the dependencies between communicating objects, thereby lowering the
    /// coupling.
    ///
    /// In this example the mediator encapsulates how a set of objects (PartyMember)
    /// interact. Instead of referring to each other directly they use the mediator (Party)
    /// interface.
    /// </summary>
    public class App
    {
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
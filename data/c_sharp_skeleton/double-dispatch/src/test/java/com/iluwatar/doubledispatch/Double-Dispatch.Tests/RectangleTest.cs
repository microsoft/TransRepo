using System;
using System.Collections.Generic;
using NUnit.Framework;

namespace Com.Iluwatar.Doubledispatch
{
    /**
     * Unit test for Rectangle
     */
    public class RectangleTest
    {
        /**
         * Test if the values passed through the constructor matches the values fetched from the getters
         */
        [Test]
        
        [Category("TestConstructorRectangle")]
        public void TestConstructorRectangle()
        {
            var rectangle = new Rectangle(1, 2, 3, 4);
            Assert.AreEqual(1, rectangle.Left);
            Assert.AreEqual(2, rectangle.Top);
            Assert.AreEqual(3, rectangle.Right);
            Assert.AreEqual(4, rectangle.Bottom);
        }

        /**
         * Test if the values passed through the constructor matches the values in the {@link
         * #toString()} 
         */
        [Test]
        
        [Category("TestToString")]
        public void TestToString()
        {
            var rectangle = new Rectangle(1, 2, 3, 4);
            Assert.AreEqual("[1,2,3,4]", rectangle.ToString());
        }

        /**
         * Test if the {@link Rectangle} class can detect if it intersects with another rectangle.
         */
        [Test]
        
        [Category("TestIntersection")]
        public void TestIntersection()
        {
            Assert.IsTrue(new Rectangle(0, 0, 1, 1).IntersectsWith(new Rectangle(0, 0, 1, 1)));
            Assert.IsTrue(new Rectangle(0, 0, 1, 1).IntersectsWith(new Rectangle(-1, -5, 7, 8)));
            Assert.IsFalse(new Rectangle(0, 0, 1, 1).IntersectsWith(new Rectangle(2, 2, 3, 3)));
            Assert.IsFalse(new Rectangle(0, 0, 1, 1).IntersectsWith(new Rectangle(-2, -2, -1, -1)));
        }
    }
}
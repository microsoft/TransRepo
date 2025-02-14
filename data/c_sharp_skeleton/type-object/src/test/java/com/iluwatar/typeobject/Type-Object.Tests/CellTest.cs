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
using System;
using System.Collections.Generic;
using NUnit.Framework;

namespace Com.Iluwatar.Typeobject
{
    [TestFixture]
    public class CellTest
    {
        [Test]
        
        [Category("InteractTest")]
        public void InteractTest()
        {
            var c1 = new Candy("green jelly", "jelly", Candy.CandyType.CrushableCandy, 5);
            var c2 = new Candy("green apple", "apple", Candy.CandyType.RewardFruit, 10);
            var matrix = new Cell[4, 4];
            matrix[0, 0] = new Cell(c1, 0, 0);
            matrix[0, 1] = new Cell(c1, 1, 0);
            matrix[0, 2] = new Cell(c2, 2, 0);
            matrix[0, 3] = new Cell(c1, 3, 0);
            var cp = new CellPool(5);
            var points1 = matrix[0, 0].Interact(matrix[0, 1], cp, matrix);
            var points2 = matrix[0, 2].Interact(matrix[0, 3], cp, matrix);
            Assert.IsTrue(points1 > 0 && points2 == 0);
        }

        [Test]
        

        [Category("CrushTest")]
        public void CrushTest()
        {
            var c1 = new Candy("green jelly", "jelly", Candy.CandyType.CrushableCandy, 5);
            var c2 = new Candy("purple candy", "candy", Candy.CandyType.CrushableCandy, 5);
            var matrix = new Cell[4, 4];
            matrix[0, 0] = new Cell(c1, 0, 0);
            matrix[1, 0] = new Cell(c2, 0, 1);
            matrix[1, 0].Crush(new CellPool(5), matrix);
            Assert.AreEqual("green jelly", matrix[1, 0].Candy.Name);
        }
    }
}
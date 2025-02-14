using System;
using System.Collections.Generic;
using NUnit.Framework;

namespace Com.Iluwatar.Typeobject
{
    public class CandyGameTest
    {
        [Test]
        
        [Category("AdjacentCellsTest")]
        public void AdjacentCellsTest()
        {
            var cg = new CandyGame(3, new CellPool(9));
            var arr1 = cg.AdjacentCells(0, 0);
            var arr2 = cg.AdjacentCells(1, 2);
            var arr3 = cg.AdjacentCells(1, 1);
            Assert.True(arr1.Count == 2 && arr2.Count == 3 && arr3.Count == 4);
        }

        [Test]
        

        [Category("ContinueRoundTest")]
        public void ContinueRoundTest()
        {
            var matrix = new Cell[2, 2];
            var c1 = new Candy("green jelly", "jelly", Candy.CandyType.CrushableCandy, 5);
            var c2 = new Candy("purple jelly", "jelly", Candy.CandyType.CrushableCandy, 5);
            var c3 = new Candy("green apple", "apple", Candy.CandyType.RewardFruit, 10);
            matrix[0, 0] = new Cell(c1, 0, 0);
            matrix[0, 1] = new Cell(c2, 1, 0);
            matrix[1, 0] = new Cell(c3, 0, 1);
            matrix[1, 1] = new Cell(c2, 1, 1);
            var p = new CellPool(4);
            var cg = new CandyGame(2, p);
            cg.Cells = matrix;
            var fruitInLastRow = cg.ContinueRound();
            matrix[1, 0].Crush(p, matrix);
            matrix[0, 0] = new Cell(c3, 0, 0);
            var matchingCandy = cg.ContinueRound();
            matrix[0, 1].Crush(p, matrix);
            matrix[0, 1] = new Cell(c3, 1, 0);
            var noneLeft = cg.ContinueRound();
            Assert.True(fruitInLastRow && matchingCandy && !noneLeft);
        }
    }
}
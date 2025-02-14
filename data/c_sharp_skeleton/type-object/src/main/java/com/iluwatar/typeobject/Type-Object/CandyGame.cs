using System;
using System.Collections.Generic;

namespace Com.Iluwatar.Typeobject
{
    public class CandyGame
    {
        private Cell[,] cells;
        private CellPool pool;
        private int totalPoints;

        public Cell[,] Cells
        {
            get { return cells; }
            set { cells = value; }
        }

        public CandyGame(int num, CellPool pool)
        {
        }

        public List<Cell> AdjacentCells(int y, int x)
        {
            return null;
        }

        public bool ContinueRound()
        {
            return false;
        }

        public void HandleChange(int points)
        {
        }

        public void Round(int timeSoFar, int totalTime)
        {
        }
    }
}
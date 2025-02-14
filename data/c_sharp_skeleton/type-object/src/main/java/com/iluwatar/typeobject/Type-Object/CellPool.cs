using System;
using System.Collections.Generic;
using System.Security.Cryptography;
using Newtonsoft.Json;

namespace Com.Iluwatar.Typeobject
{
    public class CellPool
    {
        private static readonly RandomNumberGenerator RANDOM = RandomNumberGenerator.Create();
        public static readonly string FRUIT = "fruit";
        public static readonly string CANDY = "candy";
        private List<Cell> pool;
        private int pointer;
        private Candy[] randomCode;

        // 添加公共属性来访问randomCode
        public Candy[] RandomCode 
        { 
            get { return randomCode; } 
            private set { randomCode = value; }
        }

        public CellPool(int num)
        {
        }

        public Cell GetNewCell()
        {
            return null;
        }

        public void AddNewCell(Cell c)
        {
            return;
        }

        public Candy[] AssignRandomCandytypes()
        {
            var candies = new Candy[5];
            return candies;
        }
    }
}
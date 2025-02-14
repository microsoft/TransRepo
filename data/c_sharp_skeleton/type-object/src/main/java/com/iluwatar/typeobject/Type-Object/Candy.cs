using System;
using System.Collections.Generic;
using System.Text;

namespace Com.Iluwatar.Typeobject
{
    public class Candy
    {
        public enum CandyType
        {
            CrushableCandy,
            RewardFruit
        }

        public string Name { get; }
        public Candy Parent { get; }
        public string ParentName { get; }

        private int points;
        public int Points
        {
            get { return points; }
            set { points = value; }
        }
        public readonly CandyType Type;

        public Candy(string name, string parentName, CandyType type, int points)
        {
            Name = name;
            ParentName = parentName;
            Type = type;
            Points = points;
        }
    }
}
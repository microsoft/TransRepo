using System;

namespace Com.Iluwatar.Mediator
{
    public class Action
    {
        public static readonly Action HUNT = new Action("hunted a rabbit", "arrives for dinner");
        public static readonly Action TALE = new Action("tells a tale", "comes to listen");
        public static readonly Action GOLD = new Action("found gold", "takes his share of the gold");
        public static readonly Action ENEMY = new Action("spotted enemies", "runs for cover");
        public static readonly Action NONE = new Action("", "");

        private readonly string _title;
        public string Description { get; }

        private Action(string title, string description)
        {
            _title = title;
            Description = description;
        }

        public override string ToString()
        {
            return _title;
        }
    }
}
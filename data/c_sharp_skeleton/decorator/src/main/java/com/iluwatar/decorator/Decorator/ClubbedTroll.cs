using System;

using PatternMatching;

namespace Decorator
{

    public class ClubbedTroll : Troll
    {
        private readonly Troll _decorated;

        public ClubbedTroll(Troll decorated)
        {
            _decorated = decorated;
        }

        public void Attack()
        {
            // Logger can be added if needed, for example, Console.WriteLine for debugging
            // Console.WriteLine("Troll swings at you with a club!");
            return;
        }

        public int GetAttackPower()
        {
            // Ensuring it calls the decorated troll's attack power plus additional from the club
            return 0;
        }

        public void FleeBattle()
        {
            // Logic for the troll fleeing the battle
            return;
        }
    }
}
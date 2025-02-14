using System;

namespace PatternMatching
{
    /// <summary>
    /// Interface for trolls.
    /// </summary>
    public interface ITroll
    {
        void Attack();

        int GetAttackPower();

        void FleeBattle();
    }
}
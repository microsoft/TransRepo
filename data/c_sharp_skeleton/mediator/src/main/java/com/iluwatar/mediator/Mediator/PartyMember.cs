using System;

namespace Com.Iluwatar.Mediator
{
    /// <summary>
    /// Interface for party members interacting with <see cref="Party"/>.
    /// </summary>
    public interface IPartyMember
    {
        void JoinedParty(IParty party);
        void PartyAction(Action action);
        void Act(Action action);
    }
}
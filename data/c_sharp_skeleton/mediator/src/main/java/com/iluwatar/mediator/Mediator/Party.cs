using System;

namespace Com.Iluwatar.Mediator
{
    public interface IParty
    {
        void AddMember(IPartyMember member);
        void Act(IPartyMember actor, Action action);
    }
}
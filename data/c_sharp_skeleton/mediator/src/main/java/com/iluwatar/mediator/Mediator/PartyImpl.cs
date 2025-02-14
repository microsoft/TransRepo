using System;
using System.Collections.Generic;

namespace Com.Iluwatar.Mediator
{
    /**
     * Party implementation.
     */
    public class PartyImpl : IParty
    {
        private readonly List<IPartyMember> members;

        public PartyImpl()
        {
            members = new List<IPartyMember>();
        }

        public void Act(IPartyMember actor, Action action)
        {
            return;
        }

        public void AddMember(IPartyMember member)
        {
            return;
        }
    }
}
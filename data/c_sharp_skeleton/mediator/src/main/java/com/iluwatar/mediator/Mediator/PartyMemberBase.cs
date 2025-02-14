using System;

namespace Com.Iluwatar.Mediator
{
    /**
     * Abstract base class for party members.
     */
    public abstract class PartyMemberBase : IPartyMember
    {
        protected IParty Party { get; set; }

        public virtual void JoinedParty(IParty party)
        {
        }

        public virtual void PartyAction(Action action)
        {
        }

        public virtual void Act(Action action)
        {
        }

        public abstract override string ToString();
    }
}
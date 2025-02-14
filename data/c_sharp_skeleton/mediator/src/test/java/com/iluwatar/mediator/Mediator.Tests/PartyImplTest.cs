using NUnit.Framework;
using Moq;

namespace Com.Iluwatar.Mediator
{
    [TestFixture]
    public class PartyImplTest
    {
        [Test]
        
        [Category("TestPartyAction")]
        public void TestPartyAction()
        {
            var partyMember1 = new Mock<IPartyMember>();
            var partyMember2 = new Mock<IPartyMember>();

            var party = new PartyImpl();
            party.AddMember(partyMember1.Object);
            party.AddMember(partyMember2.Object);

            partyMember1.Verify(m => m.JoinedParty(party));
            partyMember2.Verify(m => m.JoinedParty(party));

            party.Act(partyMember1.Object, Action.GOLD);
            partyMember1.VerifyNoOtherCalls();
            partyMember2.Verify(m => m.PartyAction(Action.GOLD));

            partyMember1.VerifyNoOtherCalls();
            partyMember2.VerifyNoOtherCalls();
        }
    }
}
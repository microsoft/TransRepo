using System;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;

namespace Com.Iluwatar.Mediator.Tests
{
    [TestFixture]
    public class PartyMemberTest
    {
        private TestLogger _logger;

        [SetUp]
        public void SetUp()
        {
            _logger = new TestLogger();
        }

        private static TestLogger CreateLogger()
        {
            return new TestLogger();
        }

        private static IEnumerable<TestCaseData> CreatePartyMembers()
        {
            var logger = CreateLogger();
            yield return new TestCaseData(new Func<IPartyMember>(() => new TestPartyMember("Hobbit", logger)), logger);
            yield return new TestCaseData(new Func<IPartyMember>(() => new TestPartyMember("Hunter", logger)), logger);
            yield return new TestCaseData(new Func<IPartyMember>(() => new TestPartyMember("Rogue", logger)), logger);
            yield return new TestCaseData(new Func<IPartyMember>(() => new TestPartyMember("Wizard", logger)), logger);
        }

        [Test]
        [TestCaseSource(nameof(CreatePartyMembers))]
        public void TestPartyAction(Func<IPartyMember> memberSupplier, TestLogger logger)
        {
            var member = memberSupplier();

            foreach (var action in Enum.GetValues(typeof(Action)).Cast<Action>())
            {
                member.PartyAction(action);
                Assert.That(logger.GetLastMessage(), Is.EqualTo($"{member} {action}"));
            }

            Assert.That(logger.LogSize, Is.EqualTo(Enum.GetValues(typeof(Action)).Length));
        }

        [Test]
        [TestCaseSource(nameof(CreatePartyMembers))]
        public void TestAct(Func<IPartyMember> memberSupplier, TestLogger logger)
        {
            var member = memberSupplier();

            member.Act(Action.GOLD);
            Assert.That(logger.LogSize, Is.EqualTo(0));

            var party = new TestParty();
            member.JoinedParty(party);
            Assert.That(logger.GetLastMessage(), Is.EqualTo($"{member} joins the party"));

            foreach (var action in Enum.GetValues(typeof(Action)).Cast<Action>())
            {
                member.Act(action);
                Assert.That(logger.GetLastMessage(), Is.EqualTo($"{member} {action}"));
                Assert.That(party.ReceivedActions.Contains((member, action)), Is.True);
            }

            Assert.That(logger.LogSize, Is.EqualTo(Enum.GetValues(typeof(Action)).Length + 1));
        }

        [Test]
        [TestCaseSource(nameof(CreatePartyMembers))]
        public void TestToString(Func<IPartyMember> memberSupplier, TestLogger logger)
        {
            var member = memberSupplier();
            Assert.That(member.ToString(), Is.EqualTo(member.GetType().Name));
        }
    }

    public class TestLogger
    {
        private readonly List<string> _log = new List<string>();

        public void Log(string message)
        {
            _log.Add(message);
        }

        public int LogSize => _log.Count;

        public string GetLastMessage() => _log.LastOrDefault();
    }

    public class TestParty : IParty
    {
        public List<(IPartyMember Member, Action Action)> ReceivedActions { get; } = new();

        public void Act(IPartyMember actor, Action action)
        {
            ReceivedActions.Add((actor, action));
        }

        public void AddMember(IPartyMember member)
        {
            // 测试实现可以为空
        }
    }

    public class TestPartyMember : PartyMemberBase
    {
        private readonly string _name;
        private readonly TestLogger _logger;

        public TestPartyMember(string name, TestLogger logger)
        {
            _name = name;
            _logger = logger;
        }

        public override void JoinedParty(IParty party)
        {
            base.JoinedParty(party);
            Party = party;
            _logger.Log($"{this} joins the party");
        }

        public override void PartyAction(Action action)
        {
            _logger.Log($"{this} {action}");
        }

        public override void Act(Action action)
        {
            if (Party != null)
            {
                _logger.Log($"{this} {action}");
                Party.Act(this, action);
            }
        }

        public override string ToString()
        {
            return _name;
        }
    }
}
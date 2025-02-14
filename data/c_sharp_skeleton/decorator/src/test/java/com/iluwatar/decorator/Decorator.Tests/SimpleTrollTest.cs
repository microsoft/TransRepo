using System;
using System.Collections.Generic;
using NUnit.Framework;
using NSubstitute;
using log4net;
using log4net.Appender;
using log4net.Config;
using log4net.Core;

using PatternMatching;

namespace Com.Iluwatar.Decorator
{
    [TestFixture]
    public class SimpleTrollTest
    {
        private InMemoryAppender appender;

        [SetUp]
        public void SetUp()
        {
            appender = new InMemoryAppender();
            BasicConfigurator.Configure(appender);
        }

        [TearDown]
        public void TearDown()
        {
            appender.Clear();
        }

        [Test]
        

        [Category("TestTrollActions")]
        public void TestTrollActions()
        {
            var troll = new SimpleTroll();
            Assert.AreEqual(10, troll.GetAttackPower());

            troll.Attack();
            Assert.AreEqual("The troll tries to grab you!", appender.GetLastMessage());

            troll.FleeBattle();
            Assert.AreEqual("The troll shrieks in horror and runs away!", appender.GetLastMessage());

            Assert.AreEqual(2, appender.GetLogSize());
        }

        private class InMemoryAppender : AppenderSkeleton
        {
            private readonly List<LoggingEvent> log = new List<LoggingEvent>();

            protected override void Append(LoggingEvent loggingEvent)
            {
                log.Add(loggingEvent);
            }

            public string GetLastMessage()
            {
                return log[log.Count - 1].RenderedMessage;
            }

            public int GetLogSize()
            {
                return log.Count;
            }

            public void Clear()
            {
                log.Clear();
            }
        }
    }
}
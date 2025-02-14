using System;
using System.Collections.Generic;
using NUnit.Framework;

namespace Com.Iluwatar.Bytecode
{
    [TestFixture]
    public class VirtualMachineTest
    {
        private Wizard wizard1;
        private Wizard wizard2;
        private VirtualMachine vm;

        [SetUp]
        public void Setup()
        {
            wizard1 = new Wizard(0, 0, 0, 0, 0);
            wizard2 = new Wizard(0, 0, 0, 0, 0);
            vm = new VirtualMachine(wizard1, wizard2);
        }

        [Test]
        

        [Category("TestLiteral")]
        public void TestLiteral()
        {
            var bytecode = new[]
            {
                (int)Instruction.Literal,
                10
            };
            vm.Execute(bytecode);
            
            Assert.AreEqual(1, vm.GetStack().Count);  // 检查栈上有一个元素
            Assert.AreEqual(10, vm.GetStack().Pop());
        }

        [Test]
        

        [Category("TestSetHealth")]
        public void TestSetHealth()
        {
            var bytecode = new[]
            {
                (int)Instruction.Literal,
                0,              // wizard number
                (int)Instruction.Literal,
                50,            // health amount
                (int)Instruction.SetHealth
            };
            vm.Execute(bytecode);

            Assert.That(wizard1.Health, Is.EqualTo(50));
        }

        [Test]
        

        [Category("TestSetAgility")]
        public void TestSetAgility()
        {
            var bytecode = new[]
            {
                (int)Instruction.Literal,
                0,              // wizard number
                (int)Instruction.Literal,
                50,            // agility amount
                (int)Instruction.SetAgility
            };
            vm.Execute(bytecode);

            Assert.That(wizard1.Agility, Is.EqualTo(50));
        }

        [Test]
        

        [Category("TestSetWisdom")]
        public void TestSetWisdom()
        {
            var bytecode = new[]
            {
                (int)Instruction.Literal,
                0,              // wizard number
                (int)Instruction.Literal,
                50,            // wisdom amount
                (int)Instruction.SetWisdom
            };
            vm.Execute(bytecode);

            Assert.That(wizard1.Wisdom, Is.EqualTo(50));
        }

        [Test]
        

        [Category("TestGetHealth")]
        public void TestGetHealth()
        {
            wizard1.Health = 50;
            var bytecode = new[]
            {
                (int)Instruction.Literal,
                0,              // wizard number
                (int)Instruction.GetHealth
            };
            vm.Execute(bytecode);
            Assert.AreEqual(50, vm.GetStack().Pop());
        }

        [Test]
        

        [Category("TestPlaySound")]
        public void TestPlaySound()
        {
            var bytecode = new[]
            {
                (int)Instruction.Literal,
                0,              // wizard number
                (int)Instruction.PlaySound
            };
            vm.Execute(bytecode);

            Assert.That(wizard1.NumberOfPlayedSounds, Is.EqualTo(1));
        }

        [Test]
        

        [Category("TestSpawnParticles")]
        public void TestSpawnParticles()
        {
            var bytecode = new[]
            {
                (int)Instruction.Literal,
                0,              // wizard number
                (int)Instruction.SpawnParticles
            };
            vm.Execute(bytecode);

            Assert.That(wizard1.NumberOfSpawnedParticles, Is.EqualTo(1));
        }

        [Test]
        

        [Category("TestInvalidInstruction")]
        public void TestInvalidInstruction()
        {
            var bytecode = new[] { 999 };
            Assert.Throws<ArgumentException>(() => vm.Execute(bytecode));
        }

    }
}
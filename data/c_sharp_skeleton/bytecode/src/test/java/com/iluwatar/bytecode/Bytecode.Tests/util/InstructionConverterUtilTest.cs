using System;
using System.Collections.Generic;
using NUnit.Framework;

namespace Com.Iluwatar.Bytecode
{
    [TestFixture]
    public class InstructionConverterUtilTest
    {
        [Test]
        
        [Category("TestEmptyInstruction")]
        public void TestEmptyInstruction()
        {
            var instruction = string.Empty;

            var bytecode = InstructionConverterUtil.ConvertToByteCode(instruction);

            Assert.AreEqual(0, bytecode.Length);
        }

        [Test]
        

        [Category("TestInstructions")]
        public void TestInstructions()
        {
            var instructions = "LITERAL 35 SET_HEALTH SET_WISDOM SET_AGILITY PLAY_SOUND" +
                               " SPAWN_PARTICLES GET_HEALTH ADD DIVIDE";

            var bytecode = InstructionConverterUtil.ConvertToByteCode(instructions);

            Assert.AreEqual(10, bytecode.Length);
            Assert.AreEqual((int)Instruction.Literal, bytecode[0]);
            Assert.AreEqual(35, bytecode[1]);
            Assert.AreEqual((int)Instruction.SetHealth, bytecode[2]);
            Assert.AreEqual((int)Instruction.SetWisdom, bytecode[3]);
            Assert.AreEqual((int)Instruction.SetAgility, bytecode[4]);
            Assert.AreEqual((int)Instruction.PlaySound, bytecode[5]);
            Assert.AreEqual((int)Instruction.SpawnParticles, bytecode[6]);
            Assert.AreEqual((int)Instruction.GetHealth, bytecode[7]);
            Assert.AreEqual((int)Instruction.Add, bytecode[8]);
            Assert.AreEqual((int)Instruction.Divide, bytecode[9]);
        }
    }
}
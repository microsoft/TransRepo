using System;

namespace Com.Iluwatar.Bytecode
{
    /// <summary>
    /// Representation of instructions understandable by virtual machine.
    /// </summary>
    public enum Instruction
    {
        /// <summary>
        /// "LITERAL 0", push 0 to stack
        /// </summary>
        Literal = 1,

        /// <summary>
        /// "SET_HEALTH", pop health and wizard number, call set health
        /// </summary>
        SetHealth = 2,

        /// <summary>
        /// "SET_WISDOM", pop wisdom and wizard number, call set wisdom
        /// </summary>
        SetWisdom = 3,

        /// <summary>
        /// "SET_AGILITY", pop agility and wizard number, call set agility
        /// </summary>
        SetAgility = 4,

        /// <summary>
        /// "PLAY_SOUND", pop value as wizard number, call play sound
        /// </summary>
        PlaySound = 5,

        /// <summary>
        /// "SPAWN_PARTICLES", pop value as wizard number, call spawn particles
        /// </summary>
        SpawnParticles = 6,

        /// <summary>
        /// "GET_HEALTH", pop value as wizard number, push wizard's health
        /// </summary>
        GetHealth = 7,

        /// <summary>
        /// "GET_AGILITY", pop value as wizard number, push wizard's agility
        /// </summary>
        GetAgility = 8,

        /// <summary>
        /// "GET_WISDOM", pop value as wizard number, push wizard's wisdom
        /// </summary>
        GetWisdom = 9,

        /// <summary>
        /// "ADD", pop 2 values, push their sum
        /// </summary>
        Add = 10,

        /// <summary>
        /// "DIVIDE", pop 2 values, push their division
        /// </summary>
        Divide = 11
    }

    public static class InstructionExtensions
    {
        /// <summary>
        /// Converts integer value to Instruction.
        /// </summary>
        /// <param name="value">Integer value of instruction</param>
        /// <returns>Representation of the instruction</returns>
        public static Instruction? GetInstruction(int value)
        {
            return null;
        }
    }
}
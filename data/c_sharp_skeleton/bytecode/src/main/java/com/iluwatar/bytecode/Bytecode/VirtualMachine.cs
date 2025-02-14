using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Com.Iluwatar.Bytecode
{
    /**
     * Implementation of virtual machine.
     */
    public class VirtualMachine
    {
        private readonly Stack<int> _stack = new Stack<int>();

        private readonly Wizard[] _wizards = new Wizard[2];

        public Stack<int> GetStack()
        {
            return _stack;
        }

        /**
         * No-args constructor.
         */
        public VirtualMachine()
        {
        
        }

        /**
         * Constructor taking the wizards as arguments.
         */
        public VirtualMachine(Wizard wizard1, Wizard wizard2)
        {
        
        }

        /**
         * Executes provided bytecode.
         *
         * @param bytecode to execute
         */
        public void Execute(int[] bytecode)
        {
            return;
        }

        public void SetHealth(int wizard, int amount)
        {
            return;
        }

        public void SetWisdom(int wizard, int amount)
        {
            return;
        }

        public void SetAgility(int wizard, int amount)
        {
            return;
        }

        public int GetHealth(int wizard)
        {
            return 0;
        }

        public int GetWisdom(int wizard)
        {
            return 0;
        }

        public int GetAgility(int wizard)
        {
            return 0;
        }

        private int RandomInt(int min, int max)
        {
            return 0;
        }
    }
}
using System;

namespace Gameloop
{
    /**
     * A game loop runs continuously during gameplay. Each turn of the loop, it processes
     * user input without blocking, updates the game state, and renders the game. It tracks
     * the passage of time to control the rate of gameplay.
     */
    public static class App
    {
        /**
         * Each type of game loop will run for 2 seconds.
         */
        private static readonly int GAME_LOOP_DURATION_TIME = 2000;

        /**
         * Program entry point.
         * @param args runtime arguments
         */
        public static void Main(string[] args)
        {
            return;
        }
    }
}
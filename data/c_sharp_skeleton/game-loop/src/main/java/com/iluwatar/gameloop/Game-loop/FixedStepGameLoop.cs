using System;

namespace Com.Iluwatar.Gameloop
{
    /// <summary>
    /// For fixed-step game loop, a certain amount of real time has elapsed since the
    /// last turn of the game loop. This is how much game time need to be simulated for
    /// the game’s “now” to catch up with the player’s.
    /// </summary>
    public class FixedStepGameLoop : GameLoop
    {
        /// <summary>
        /// 20 ms per frame = 50 FPS.
        /// </summary>
        private static readonly long MsPerFrame = 20;

        protected override void ProcessGameLoop()
        {
            return;
        }

        public void Update()
        {
            return;
        }
    }
}
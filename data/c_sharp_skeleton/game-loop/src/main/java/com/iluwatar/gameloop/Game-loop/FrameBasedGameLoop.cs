using System;

namespace Com.Iluwatar.Gameloop
{
    /**
     * Frame-based game loop is the easiest implementation. The loop always keeps spinning
     * for the following three processes: processInput, update and render. The problem with
     * it is you have no control over how fast the game runs. On a fast machine, that loop
     * will spin so fast users won’t be able to see what’s going on. On a slow machine, the
     * game will crawl. If you have a part of the game that's content-heavy or does more AI
     * or physics, the game will actually play slower there.
     */
    public class FrameBasedGameLoop : GameLoop
    {
        protected override void ProcessGameLoop()
        {
            return;
        }

        /**
         * Each time when update() is invoked, a new frame is created, and the bullet will be
         * moved 0.5f away from the current position.
         */
        public void Update()
        {
            return;
        }
    }
}
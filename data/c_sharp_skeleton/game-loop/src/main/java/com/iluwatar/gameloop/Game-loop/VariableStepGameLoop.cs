using System;

namespace Com.Iluwatar.Gameloop
{
    /// <summary>
    /// The variable-step game loop chooses a time step to advance based on how much
    /// real time passed since the last frame. The longer the frame takes, the bigger
    /// steps the game takes. It always keeps up with real time because it will take
    /// bigger and bigger steps to get there.
    /// </summary>
    public class VariableStepGameLoop : GameLoop
    {
        protected override void ProcessGameLoop()
        {
            return;
        }

        public void Update(long elapsedTime)
        {
            return;
        }
    }
}
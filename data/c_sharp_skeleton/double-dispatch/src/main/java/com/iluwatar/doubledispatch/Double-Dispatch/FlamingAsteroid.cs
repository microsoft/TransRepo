using System;

namespace Com.Iluwatar.Doubledispatch
{
    /// <summary>
    /// Flaming asteroid game object.
    /// </summary>
    public class FlamingAsteroid : Meteoroid
    {
        public FlamingAsteroid(int left, int top, int right, int bottom):base(left, top, right, bottom)
        {
            // Constructor logic, if any
        }

        public override void Collision(GameObject gameObject)
        {
            return;
        }
    }
}
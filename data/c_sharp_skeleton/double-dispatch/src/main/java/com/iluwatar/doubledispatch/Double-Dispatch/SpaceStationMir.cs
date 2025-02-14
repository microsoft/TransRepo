using System;
using static System.Console;

namespace Com.Iluwatar.Doubledispatch
{
    /// <summary>
    /// Space station Mir game object.
    /// </summary>
    public class SpaceStationMir : GameObject
    {
        public SpaceStationMir(int left, int top, int right, int bottom):base(left, top, right, bottom)
        {
        }

        public override void Collision(GameObject gameObject)
        {
            return;
        }

        public override void CollisionResolve(FlamingAsteroid asteroid)
        {
            return;
        }

        public override void CollisionResolve(Meteoroid meteoroid)
        {
            return;
        }

        public override void CollisionResolve(SpaceStationMir mir)
        {
            return;
        }

        public override void CollisionResolve(SpaceStationIss iss)
        {
            return;
        }

        private void LogHits(GameObject gameObject)
        {
            return;
        }
    }
}
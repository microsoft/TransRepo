using System;

namespace Com.Iluwatar.Doubledispatch
{
    public class Meteoroid : GameObject
    {
        public Meteoroid(int left, int top, int right, int bottom):base(left, top, right, bottom)
        {
            // Constructor implementation
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
    }
}
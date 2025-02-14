using System;

namespace Com.Iluwatar.Doubledispatch
{
    /// <summary>
    /// Space station ISS game object.
    /// </summary>
    public class SpaceStationIss : SpaceStationMir
    {
        public SpaceStationIss(int left, int top, int right, int bottom):base(left, top, right, bottom)
        {
        
        }

        public override void Collision(GameObject gameObject)
        {
            return;
        }
    }
}
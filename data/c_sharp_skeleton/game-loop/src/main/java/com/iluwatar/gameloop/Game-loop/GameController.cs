using System;

namespace Com.Iluwatar.Gameloop
{
    /// <summary>
    /// Update and render objects in the game. Here we add a Bullet object to the
    /// game system to show how the game loop works.
    /// </summary>
    public class GameController
    {
        private readonly Bullet bullet;

        public Bullet Bullet { get; private set; }

        /// <summary>
        /// Initialize Bullet instance.
        /// </summary>
        public GameController()
        {
        }

        /// <summary>
        /// Move bullet position by the provided offset.
        /// </summary>
        /// <param name="offset">Moving offset</param>
        public void MoveBullet(float offset)
        {
            return;
        }

        /// <summary>
        /// Get current position of the bullet.
        /// </summary>
        /// <returns>Position of bullet</returns>
        public float GetBulletPosition()
        {
            return 0.0f;
        }
    }
}
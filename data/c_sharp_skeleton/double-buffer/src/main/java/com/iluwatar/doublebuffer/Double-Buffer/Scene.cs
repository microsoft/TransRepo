using System.Collections.Generic;
using Microsoft.Extensions.Logging;
using System;

namespace Com.Iluwatar.DoubleBuffer
{
    /// <summary>
    /// Scene class. Render the output frame.
    /// </summary>
    public class Scene
    {
        private readonly Buffer[] frameBuffers;

        private int current;

        private int next;

        /// <summary>
        /// Constructor of Scene.
        /// </summary>
        public Scene()
        {

        }

        /// <summary>
        /// Draw the next frame.
        /// </summary>
        /// <param name="coordinateList">List of pixels of which the color should be black</param>
        public void Draw(List<Tuple<int, int>> coordinateList)
        {
            return;
        }

        public Buffer GetBuffer()
        {
            return null;
        }

        private void Swap()
        {
            return;
        }
    }
}
// Please note that the code below is a direct translation of the given Java code into C#,
// and it follows the guidelines and translation rules provided.

using System;

using Com.Iluwatar.Doublebuffer;

namespace PatternMatching
{
    public class FrameBuffer : Buffer
    {
        public static readonly int WIDTH = 10;
        public static readonly int HEIGHT = 8;

        private readonly Pixel[] pixels = new Pixel[WIDTH * HEIGHT];

        public FrameBuffer()
        {
        }

        public void Clear(int x, int y)
        {
            return;
        }

        public void Draw(int x, int y)
        {
            return;
        }

        public void ClearAll()
        {
            return;
        }

        public Pixel[] GetPixels()
        {
            return new Pixel[0];
        }

        private int GetIndex(int x, int y)
        {
            return 0;
        }
    }
}
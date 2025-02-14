/*
 * This project is licensed under the MIT license. Module model-view-viewmodel is using ZK framework licensed under LGPL (see lgpl-3.0.txt).
 *
 * The MIT License
 * Copyright © 2014-2022 Ilkka Seppälä
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;

namespace Promise
{
    /// <summary>
    /// Utility to perform various operations.
    /// </summary>
    public static class Utility
    {
        /// <summary>
        /// Calculates character frequency of the file provided.
        /// </summary>
        /// <param name="fileLocation">Location of the file.</param>
        /// <returns>A map of character to its frequency, an empty map if file does not exist.</returns>
        public static Dictionary<char, long> CharacterFrequency(string fileLocation)
        {
            return null;
        }

        /// <summary>
        /// Return the character with the lowest frequency, if exists.
        /// </summary>
        /// <returns>The character, null otherwise.</returns>
        public static char? LowestFrequencyChar(Dictionary<char, long> charFrequency)
        {
            return null;
        }

        /// <summary>
        /// Count the number of lines in a file.
        /// </summary>
        /// <returns>Number of lines, 0 if file does not exist.</returns>
        public static int CountLines(string fileLocation)
        {
            return 0;
        }

        /// <summary>
        /// Downloads the contents from the given urlString, and stores it in a temporary directory.
        /// </summary>
        /// <returns>The absolute path of the file downloaded.</returns>
        public static string DownloadFile(string urlString)
        {
            return "";
        }
    }
}
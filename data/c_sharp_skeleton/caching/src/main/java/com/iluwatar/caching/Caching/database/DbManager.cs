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

namespace Com.Iluwatar.Caching
{
    /// <summary>
    /// DBManager handles the communication with the underlying data store i.e.
    /// Database. It contains the implemented methods for querying, inserting,
    /// and updating data. MongoDB was used as the database for the application.
    /// </summary>
    public interface DbManager
    {
        /// <summary>
        /// Connect to DB.
        /// </summary>
        void Connect();

        /// <summary>
        /// Disconnect from DB.
        /// </summary>
        void Disconnect();

        /// <summary>
        /// Read from DB.
        /// </summary>
        /// <param name="userId">String</param>
        /// <returns>UserAccount</returns>
        UserAccount ReadFromDb(string userId);

        /// <summary>
        /// Write to DB.
        /// </summary>
        /// <param name="userAccount">UserAccount</param>
        /// <returns>UserAccount</returns>
        UserAccount WriteToDb(UserAccount userAccount);

        /// <summary>
        /// Update record.
        /// </summary>
        /// <param name="userAccount">UserAccount</param>
        /// <returns>UserAccount</returns>
        UserAccount UpdateDb(UserAccount userAccount);

        /// <summary>
        /// Update record or Insert if not exists.
        /// </summary>
        /// <param name="userAccount">UserAccount</param>
        /// <returns>UserAccount</returns>
        UserAccount UpsertDb(UserAccount userAccount);
    }
}
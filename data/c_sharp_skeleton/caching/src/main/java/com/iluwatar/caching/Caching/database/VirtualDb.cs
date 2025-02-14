using System;
using System.Collections.Generic;

namespace Com.Iluwatar.Caching
{
    /// <summary>
    /// Implementation of DatabaseManager.
    /// Implements base methods to work with HashMap as database.
    /// </summary>
    public class VirtualDb : DbManager
    {
        /// <summary>
        /// Virtual DataBase.
        /// </summary>
        private IDictionary<string, UserAccount> db;

        /// <summary>
        /// Creates new HashMap.
        /// </summary>
        public void Connect()
        {
            // No operation
            return;
        }

        public void Disconnect()
        {
            // No operation
            return;
        }

        /// <summary>
        /// Read from Db.
        /// </summary>
        /// <param name="userId">User ID as string</param>
        /// <returns>UserAccount</returns>
        public UserAccount ReadFromDb(string userId)
        {
            return null;
        }

        /// <summary>
        /// Write to DB.
        /// </summary>
        /// <param name="userAccount">UserAccount</param>
        /// <returns>UserAccount</returns>
        public UserAccount WriteToDb(UserAccount userAccount)
        {
            return null;
        }

        /// <summary>
        /// Update record in DB.
        /// </summary>
        /// <param name="userAccount">UserAccount</param>
        /// <returns>UserAccount</returns>
        public UserAccount UpdateDb(UserAccount userAccount)
        {
            return null;
        }

        /// <summary>
        /// Update.
        /// </summary>
        /// <param name="userAccount">UserAccount</param>
        /// <returns>UserAccount</returns>
        public UserAccount UpsertDb(UserAccount userAccount)
        {
            return null;
        }
    }
}
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


// The MIT License
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//

namespace Com.Iluwatar.Caching
{
    using Microsoft.Extensions.Logging;
    
    /// <summary>
    /// The caching strategies are implemented in this class.
    /// </summary>
    public class CacheStore
    {
        // Cache capacity
        private const int CAPACITY = 3;
        
        // Lru cache see LruCache
        private LruCache _cache;

        // DbManager
        private readonly DbManager _dbManager;

        /// <summary>
        /// Cache Store.
        /// </summary>
        /// <param name="dataBaseManager">DbManager</param>
        public CacheStore(DbManager dataBaseManager)
        {

        }

        /// <summary>
        /// Init cache capacity.
        /// </summary>
        /// <param name="capacity">int</param>
        public void InitCapacity(int capacity)
        {
            return;
        }

        /// <summary>
        /// Get user account using read-through cache.
        /// </summary>
        /// <param name="userId">string</param>
        /// <returns>UserAccount</returns>
        public UserAccount ReadThrough(string userId)
        {
            return null;
        }

        /// <summary>
        /// Get user account using write-through cache.
        /// </summary>
        /// <param name="userAccount">UserAccount</param>
        public void WriteThrough(UserAccount userAccount)
        {
            return;
        }

        /// <summary>
        /// Get user account using write-around cache.
        /// </summary>
        /// <param name="userAccount">UserAccount</param>
        public void WriteAround(UserAccount userAccount)
        {
            return;
        }

        /// <summary>
        /// Get user account using read-through cache with write-back policy.
        /// </summary>
        /// <param name="userId">string</param>
        /// <returns>UserAccount</returns>
        public UserAccount ReadThroughWithWriteBackPolicy(string userId)
        {
            return null;
        }

        /// <summary>
        /// Set user account.
        /// </summary>
        /// <param name="userAccount">UserAccount</param>
        public void WriteBehind(UserAccount userAccount)
        {
            return;
        }

        /// <summary>
        /// Clears cache.
        /// </summary>
        public void ClearCache()
        {
            return;
        }

        /// <summary>
        /// Writes remaining content in the cache into the DB.
        /// </summary>
        public void FlushCache()
        {
            return;
        }

        /// <summary>
        /// Print user accounts.
        /// </summary>
        /// <returns>string</returns>
        public string Print()
        {
            return "";
        }

        /// <summary>
        /// Delegate to backing cache store.
        /// </summary>
        /// <param name="userId">string</param>
        /// <returns>UserAccount</returns>
        public UserAccount Get(string userId)
        {
            return null;
        }

        /// <summary>
        /// Delegate to backing cache store.
        /// </summary>
        /// <param name="userId">string</param>
        /// <param name="userAccount">UserAccount</param>
        public void Set(string userId, UserAccount userAccount)
        {
            return;
        }

        /// <summary>
        /// Delegate to backing cache store.
        /// </summary>
        /// <param name="userId">string</param>
        public void Invalidate(string userId)
        {
            return;
        }
    }
}
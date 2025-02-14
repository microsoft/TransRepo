using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;


namespace Com.Iluwatar.Caching
{
    /// <summary>
    /// AppManager helps to bridge the gap in communication between the main class
    /// and the application's back-end. DB connection is initialized through this
    /// class. The chosen caching strategy/policy is also initialized here.
    /// Before the cache can be used, the size of the cache has to be set.
    /// Depending on the chosen caching policy, AppManager will call the
    /// appropriate function in the CacheStore class.
    /// </summary>
    public class AppManager
    {
        /// <summary>
        /// Caching Policy.
        /// </summary>
        private CachingPolicy _cachingPolicy;

        /// <summary>
        /// Database Manager.
        /// </summary>
        private readonly DbManager _dbManager;

        /// <summary>
        /// Cache Store.
        /// </summary>
        private readonly CacheStore _cacheStore;

        /// <summary>
        /// Constructor.
        /// </summary>
        /// <param name="newDbManager">Database manager</param>
        public AppManager(DbManager newDbManager)
        {
            _dbManager = newDbManager;
        }

        /// <summary>
        /// Developer/Tester is able to choose whether the application should use
        /// MongoDB as its underlying data storage or a simple .NET data structure
        /// to (temporarily) store the data/objects during runtime.
        /// </summary>
        public void InitDb()
        {
            // Implementation here
        }

        /// <summary>
        /// Initialize caching policy.
        /// </summary>
        /// <param name="policy">Caching policy</param>
        public void InitCachingPolicy(CachingPolicy policy)
        {
            _cachingPolicy = policy;
        }

        /// <summary>
        /// Find user account.
        /// </summary>
        /// <param name="userId">User ID</param>
        /// <returns>User account</returns>
        public UserAccount Find(string userId)
        {
            // Implementation here
            return null;
        }

        /// <summary>
        /// Save user account.
        /// </summary>
        /// <param name="userAccount">User account</param>
        public void Save(UserAccount userAccount)
        {
            // Implementation here
        }

        /// <summary>
        /// Returns cache content as String.
        /// </summary>
        /// <returns>Cache content</returns>
        public string PrintCacheContent()
        {
            // Implementation here
            return "";
        }

        /// <summary>
        /// Cache-Aside save user account helper.
        /// </summary>
        /// <param name="userAccount">User account</param>
        private void SaveAside(UserAccount userAccount)
        {
            // Implementation here
        }

        /// <summary>
        /// Cache-Aside find user account helper.
        /// </summary>
        /// <param name="userId">User ID</param>
        /// <returns>User account</returns>
        private UserAccount FindAside(string userId)
        {
            // Implementation here
            return null;
        }
    }
}
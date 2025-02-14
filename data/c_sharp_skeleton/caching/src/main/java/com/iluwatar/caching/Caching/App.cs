using System;
using System.Collections.Generic;
using Microsoft.Extensions.Logging;

namespace Com.Iluwatar.Caching
{
    /// <summary>
    /// The Caching pattern describes how to avoid expensive re-acquisition of
    /// resources by not releasing the resources immediately after their use.
    /// The resources retain their identity, are kept in some fast-access storage,
    /// and are re-used to avoid having to acquire them again. There are four main
    /// caching strategies/techniques in this pattern; each with their own pros and
    /// cons. They are <code>write-through</code> which writes data to the cache and
    /// DB in a single transaction, <code>write-around</code> which writes data
    /// immediately into the DB instead of the cache, <code>write-behind</code>
    /// which writes data into the cache initially whilst the data is only
    /// written into the DB when the cache is full, and <code>cache-aside</code>
    /// which pushes the responsibility of keeping the data synchronized in both
    /// data sources to the application itself. The <code>read-through</code>
    /// strategy is also included in the mentioned four strategies --
    /// returns data from the cache to the caller <b>if</b> it exists <b>else</b>
    /// queries from DB and stores it into the cache for future use. These strategies
    /// determine when the data in the cache should be written back to the backing
    /// store (i.e. Database) and help keep both data sources
    /// synchronized/up-to-date. This pattern can improve performance and also helps
    /// to maintainconsistency between data held in the cache and the data in
    /// the underlying data store.
    ///
    /// In this example, the user account (UserAccount) entity is used
    /// as the underlying application data. The cache itself is implemented as an
    /// internal (Java) data structure. It adopts a Least-Recently-Used (LRU)
    /// strategy for evicting data from itself when its full. The four
    /// strategies are individually tested. The testing of the cache is restricted
    /// towards saving and querying of user accounts from the
    /// underlying data store(DbManager). The main class (App)
    /// is not aware of the underlying mechanics of the application
    /// (i.e. save and query) and whether the data is coming from the cache or the
    /// DB (i.e. separation of concern). The AppManager (AppManager) handles
    /// the transaction of data to-and-from the underlying data store (depending on
    /// the preferred caching policy/strategy).
    /// 
    /// App --> AppManager --> CacheStore/LRUCache/CachingPolicy -->
    /// DBManager
    /// 
    /// There are 2 ways to launch the application.
    ///  - to use 'in Memory' database.
    ///  - to use the MongoDb as a database
    ///
    /// To run the application with 'in Memory' database, just launch it without parameters
    /// Example: 'dotnet run'
    ///
    /// To run the application with MongoDb you need to be installed the MongoDb
    /// in your system, or to launch it in the docker container.
    /// You may launch docker container from the root of current module with command:
    /// 'docker-compose up'
    /// Then you can start the application with parameter --mongo
    /// Example: 'dotnet run --mongo'
    /// </summary>
    public class App
    {
        private static readonly string USE_MONGO_DB = "--mongo";

        private readonly AppManager appManager;

        public App(bool isMongo)
        {
            // Constructor logic
        }

        public static void Main(string[] args)
        {
            bool isDbMongo = IsDbMongo(args);
            App app = new App(isDbMongo);
            app.UseReadAndWriteThroughStrategy();
            app.UseReadThroughAndWriteAroundStrategy();
            app.UseReadThroughAndWriteBehindStrategy();
            app.UseCacheAsideStrategy();
        }

        private static bool IsDbMongo(string[] args)
        {
            return false;
        }

        public void UseReadAndWriteThroughStrategy()
        {
            appManager.Find("001");
        }

        public void UseReadThroughAndWriteAroundStrategy()
        {
            appManager.Find("002");
        }

        public void UseReadThroughAndWriteBehindStrategy()
        {
            appManager.Find("003");
            appManager.Find("004");
        }

        public void UseCacheAsideStrategy()
        {
            appManager.Find("003");
            appManager.Find("004");
        }
    }
}
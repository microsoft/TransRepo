using System;
using MongoDB.Bson;
using MongoDB.Driver;


namespace Com.Iluwatar.Caching
{
    /**
     * Implementation of DatabaseManager.
     * implements base methods to work with MongoDb.
     */
    public class MongoDb : DbManager
    {
        private static readonly string DATABASE_NAME = "admin";
        private static readonly string MONGO_USER = "root";
        private static readonly string MONGO_PASSWORD = "rootpassword";
        private MongoClient client;
        private IMongoDatabase db;

        public void SetDb(IMongoDatabase db)
        {
        }

        /**
         * Connect to Db. Check the connection
         */
        public void Connect()
        {
            db = client.GetDatabase(DATABASE_NAME);
        }

        public void Disconnect()
        {
        }

        /**
         * Read data from DB.
         *
         * @param userId {@link String}
         * @return {@link UserAccount}
         */
        public UserAccount ReadFromDb(string userId)
        {
            return null;
        }

        /**
         * Write data to DB.
         *
         * @param userAccount {@link UserAccount}
         * @return {@link UserAccount}
         */
        public UserAccount WriteToDb(UserAccount userAccount)
        {
            db.GetCollection<BsonDocument>("").InsertOne(null);
            return null;
        }

        /**
         * Update DB.
         *
         * @param userAccount {@link UserAccount}
         * @return {@link UserAccount}
         */
        public UserAccount UpdateDb(UserAccount userAccount)
        {
            db.GetCollection<BsonDocument>("").UpdateOne(null, null);
            return null;
        }

        /**
         * Update data if exists.
         *
         * @param userAccount {@link UserAccount}
         * @return {@link UserAccount}
         */
        public UserAccount UpsertDb(UserAccount userAccount)
        {
            db.GetCollection<BsonDocument>("").UpdateOne(null, null);
            return null;
        }
    }
}
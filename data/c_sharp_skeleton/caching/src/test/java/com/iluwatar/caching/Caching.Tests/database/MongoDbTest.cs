using System;
using static System.Linq.Enumerable;
using System.Collections.Generic;
using MongoDB.Bson;
using MongoDB.Driver;
using Moq;


namespace Com.Iluwatar.Caching
{
    public class MongoDbTest
    {
        private const string ID = "123";
        private const string NAME = "Some user";
        private const string ADDITIONAL_INFO = "Some app Info";

        private Mock<IMongoDatabase> _mockDb;
        private MongoDb _mongoDb;
        private UserAccount _userAccount;

        [SetUp]
        public void SetUp()
        {
            _mockDb = new Mock<IMongoDatabase>();
            _mongoDb = new MongoDb();
            _mongoDb.SetDb(_mockDb.Object);
            _userAccount = new UserAccount(ID, NAME, ADDITIONAL_INFO);
        }

        [Test]
        

        [Category("Connect_DoesNotThrow")]
        public void Connect_DoesNotThrow()
        {
            Assert.DoesNotThrow(() => _mongoDb.Connect());
        }

        [Test]
        

        [Category("ReadFromDb_ReturnsCorrectUserAccount")]
        public void ReadFromDb_ReturnsCorrectUserAccount()
        {
            var document = new BsonDocument
            {
                { "userId", ID },
                { "userName", NAME },
                { "additionalInfo", ADDITIONAL_INFO }
            };

            var mockCollection = new Mock<IMongoCollection<BsonDocument>>();
            _mockDb.Setup(db => db.GetCollection<BsonDocument>("UserAccount", null))
                .Returns(mockCollection.Object);

            var mockFindIterable = new Mock<IAsyncCursor<BsonDocument>>();
            mockFindIterable.SetupSequence(cursor => cursor.MoveNext(It.IsAny<System.Threading.CancellationToken>()))
                            .Returns(true).Returns(false);
            mockFindIterable.Setup(cursor => cursor.Current).Returns(new List<BsonDocument> { document });

            mockCollection.Setup(collection => collection.FindSync(
                It.IsAny<FilterDefinition<BsonDocument>>(),
                It.IsAny<FindOptions<BsonDocument, BsonDocument>>(),
                It.IsAny<System.Threading.CancellationToken>()))
                .Returns(mockFindIterable.Object);

            var result = _mongoDb.ReadFromDb(ID);

            Assert.AreEqual(_userAccount, result);
        }

        [Test]
        

        [Category("WriteToDb_DoesNotThrow")]
        public void WriteToDb_DoesNotThrow()
        {
            var mockCollection = new Mock<IMongoCollection<BsonDocument>>();
            _mockDb.Setup(db => db.GetCollection<BsonDocument>("UserAccount", null))
                .Returns(mockCollection.Object);

            Assert.DoesNotThrow(() => _mongoDb.WriteToDb(_userAccount));
        }

        [Test]
        

        [Category("UpdateDb_DoesNotThrow")]
        public void UpdateDb_DoesNotThrow()
        {
            var mockCollection = new Mock<IMongoCollection<BsonDocument>>();
            _mockDb.Setup(db => db.GetCollection<BsonDocument>("UserAccount", null))
                .Returns(mockCollection.Object);

            Assert.DoesNotThrow(() => _mongoDb.UpdateDb(_userAccount));
        }

        [Test]
        

        [Category("UpsertDb_DoesNotThrow")]
        public void UpsertDb_DoesNotThrow()
        {
            var mockCollection = new Mock<IMongoCollection<BsonDocument>>();
            _mockDb.Setup(db => db.GetCollection<BsonDocument>("UserAccount", null))
                .Returns(mockCollection.Object);

        Assert.DoesNotThrow(() => _mongoDb.UpsertDb(_userAccount));
        }
    }
}
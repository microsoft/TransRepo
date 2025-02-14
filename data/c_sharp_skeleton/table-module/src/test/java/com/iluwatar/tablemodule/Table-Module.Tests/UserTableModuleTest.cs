using System;
using System.Data;
using System.Data.SqlClient;
using System.Data.SQLite;
using NUnit.Framework;

namespace Com.Iluwatar.Tablemodule
{
    [TestFixture]
    public class UserTableModuleTests
    {
        private const string DbUrl = "Data Source=:memory:";

        private static IDbConnection CreateConnection()
        {
            var connection = new SQLiteConnection(DbUrl);
            connection.Open();
            return connection;
        }

        [SetUp]
        public void SetUp()
        {
            using(var connection = CreateConnection())
            using(var command = connection.CreateCommand())
            {
                command.CommandText = UserTableModule.DeleteSchemaSql;
                command.ExecuteNonQuery();
                command.CommandText = UserTableModule.CreateSchemaSql;
                command.ExecuteNonQuery();
            }
        }

        [TearDown]
        public void TearDown()
        {
            using(var connection = CreateConnection())
            using(var command = connection.CreateCommand())
            {
                command.CommandText = UserTableModule.DeleteSchemaSql;
                command.ExecuteNonQuery();
            }
        }

        [Test]
        

        [Category("LoginShouldFail")]
        public void LoginShouldFail()
        {
            var dataSource = CreateConnection();
            var userTableModule = new UserTableModule(dataSource);
            var user = new User(1, "123456", "123456");
            Assert.AreEqual(0, userTableModule.Login(user.Username, user.Password));
        }

        [Test]
        

        [Category("LoginShouldSucceed")]
        public void LoginShouldSucceed()
        {
            var dataSource = CreateConnection();
            var userTableModule = new UserTableModule(dataSource);
            var user = new User(1, "123456", "123456");
            userTableModule.RegisterUser(user);
            Assert.AreEqual(1, userTableModule.Login(user.Username, user.Password));
        }

        [Test]
        

        [Category("RegisterShouldFail")]
        public void RegisterShouldFail()
        {
            var dataSource = CreateConnection();
            var userTableModule = new UserTableModule(dataSource);
            var user = new User(1, "123456", "123456");
            userTableModule.RegisterUser(user);
            Assert.Throws<SQLiteException>(() => userTableModule.RegisterUser(user));
        }

        [Test]
        

        [Category("RegisterShouldSucceed")]
        public void RegisterShouldSucceed()
        {
            var dataSource = CreateConnection();
            var userTableModule = new UserTableModule(dataSource);
            var user = new User(1, "123456", "123456");
            Assert.AreEqual(1, userTableModule.RegisterUser(user));
        }
    }
}
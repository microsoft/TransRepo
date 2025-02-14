using System;
using System.Collections.Generic;
using NUnit.Framework;

namespace Com.Iluwatar.Converter
{
    [TestFixture]
    public class ConverterTest
    {
        private readonly UserConverter userConverter = new UserConverter();

        [Test]
        

        [Category("TestConversionsStartingFromDomain")]
        public void TestConversionsStartingFromDomain()
        {
            var u1 = new User("Tom", "Hanks", true, "tom@hanks.com");
            var u2 = userConverter.ConvertFromDto(userConverter.ConvertFromEntity(u1));
            Assert.AreEqual(u1, u2);
        }

        [Test]
        

        [Category("TestConversionsStartingFromDto")]
        public void TestConversionsStartingFromDto()
        {
            var u1 = new UserDto("Tom", "Hanks", true, "tom@hanks.com");
            var u2 = userConverter.ConvertFromEntity(userConverter.ConvertFromDto(u1));
            Assert.AreEqual(u1, u2);
        }

        [Test]
        

        [Category("TestCustomConverter")]
        public void TestCustomConverter()
        {
            var converter = new Converter<UserDto, User>(
                userDto => new User(
                    userDto.FirstName,
                    userDto.LastName,
                    userDto.Active, 
                    new Random().Next().ToString()
                ),
                user => new UserDto(
                    user.FirstName,
                    user.LastName,
                    user.Active,
                    user.FirstName.ToLower() + user.LastName.ToLower() + "@whatever.com")
            );
            var u1 = new User("John", "Doe", false, "12324");
            var userDto = converter.ConvertFromEntity(u1);
            Assert.AreEqual("johndoe@whatever.com", userDto.Email);
        }

        [Test]
        

        [Category("TestCollectionConversion")]
        public void TestCollectionConversion()
        {
            var users = new List<User>
            {
                new User("Camile", "Tough", false, "124sad"),
                new User("Marti", "Luther", true, "42309fd"),
                new User("Kate", "Smith", true, "if0243")
            };
            var fromDtos = userConverter.CreateFromDtos(userConverter.CreateFromEntities(users));
            Assert.AreEqual(users, fromDtos);
        }
    }
}
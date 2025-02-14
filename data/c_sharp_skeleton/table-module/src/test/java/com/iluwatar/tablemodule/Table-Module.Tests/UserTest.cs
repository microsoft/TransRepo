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
using NUnit.Framework;

namespace Com.Iluwatar.Tablemodule
{
    [TestFixture]
    public class UserTest
    {
        [Test]
        [Category("TestEquals1")]
        public void TestEquals1()
        {
            var user = new User(1, "janedoe", "iloveyou");
            var otherUser = new User(123, "abcd", "qwerty");
            Assert.AreNotEqual(user, otherUser);
            Assert.IsFalse(user.Equals(otherUser));
            Assert.AreNotEqual(user.GetHashCode(), otherUser.GetHashCode());
        }

        [Test]
        [Category("TestEquals2")]
        public void TestEquals2()
        {
            var user1 = new User(1, "janedoe", "iloveyou");
            var user2 = new User(1, "janedoe", "iloveyou");
            Assert.AreEqual(user1, user2);
            Assert.IsTrue(user1.Equals(user2));
            Assert.IsTrue(user2.Equals(user1));
            Assert.AreEqual(user1.GetHashCode(), user2.GetHashCode());
        }

        [Test]
        [Category("TestEquals3")]
        public void TestEquals3()
        {
            var user1 = new User(123, "janedoe", "iloveyou");
            var user2 = new User(1, "janedoe", "iloveyou");
            Assert.AreNotEqual(user1, user2);
            Assert.IsFalse(user1.Equals(user2));
            Assert.IsFalse(user2.Equals(user1));
            Assert.AreNotEqual(user1.GetHashCode(), user2.GetHashCode());
            Assert.AreEqual(user1.Username, user2.Username);
            Assert.AreEqual(user1.Password, user2.Password);
        }

        [Test]
        [Category("TestEquals4")]
        public void TestEquals4()
        {
            var user1 = new User(1, null, "iloveyou");
            var user2 = new User(1, "janedoe", "iloveyou");
            Assert.AreNotEqual(user1, user2);
            Assert.IsFalse(user1.Equals(user2));
            Assert.IsFalse(user2.Equals(user1));
            Assert.AreNotEqual(user1.GetHashCode(), user2.GetHashCode());
            Assert.AreEqual(user1.Id, user2.Id);
            Assert.AreEqual(user1.Password, user2.Password);
        }

        [Test]
        [Category("TestEquals5")]
        public void TestEquals5()
        {
            var user1 = new User(1, "iloveyou", "iloveyou");
            var user2 = new User(1, "janedoe", "iloveyou");
            Assert.AreNotEqual(user1, user2);
            Assert.IsFalse(user1.Equals(user2));
            Assert.IsFalse(user2.Equals(user1));
            Assert.AreNotEqual(user1.GetHashCode(), user2.GetHashCode());
            Assert.AreEqual(user1.Id, user2.Id);
            Assert.AreEqual(user1.Password, user2.Password);
        }

        [Test]
        [Category("TestEquals6")]
        public void TestEquals6()
        {
            var user1 = new User(1, "janedoe", "janedoe");
            var user2 = new User(1, "janedoe", "iloveyou");
            Assert.AreNotEqual(user1, user2);
            Assert.IsFalse(user1.Equals(user2));
            Assert.IsFalse(user2.Equals(user1));
            Assert.AreNotEqual(user1.GetHashCode(), user2.GetHashCode());
            Assert.AreEqual(user1.Id, user2.Id);
            Assert.AreEqual(user1.Username, user2.Username);
        }

        [Test]
        [Category("TestEquals7")]
        public void TestEquals7()
        {
            var user1 = new User(1, "janedoe", null);
            var user2 = new User(1, "janedoe", "iloveyou");
            Assert.AreNotEqual(user1, user2);
            Assert.IsFalse(user1.Equals(user2));
            Assert.IsFalse(user2.Equals(user1));
            Assert.AreNotEqual(user1.GetHashCode(), user2.GetHashCode());
            Assert.AreEqual(user1.Id, user2.Id);
            Assert.AreEqual(user1.Username, user2.Username);
        }

        [Test]
        [Category("TestEquals8")]
        public void TestEquals8()
        {
            var user1 = new User(1, null, "iloveyou");
            var user2 = new User(1, null, "iloveyou");
            Assert.AreEqual(user1, user2);
            Assert.IsTrue(user1.Equals(user2));
            Assert.IsTrue(user2.Equals(user1));
            Assert.AreEqual(user1.GetHashCode(), user2.GetHashCode());
            Assert.AreEqual(user1.Id, user2.Id);
            Assert.AreEqual(user1.Password, user2.Password);
            Assert.IsNull(user1.Username);
            Assert.IsNull(user2.Username);
        }

        [Test]
        [Category("TestEquals9")]
        public void TestEquals9()
        {
            var user1 = new User(1, "janedoe", null);
            var user2 = new User(1, "janedoe", null);
            Assert.AreEqual(user1, user2);
            Assert.IsTrue(user1.Equals(user2));
            Assert.IsTrue(user2.Equals(user1));
            Assert.AreEqual(user1.GetHashCode(), user2.GetHashCode());
            Assert.AreEqual(user1.Id, user2.Id);
            Assert.AreEqual(user1.Username, user2.Username);
            Assert.IsNull(user1.Password);
            Assert.IsNull(user2.Password);
        }

        [Test]
        [Category("TestHashCode1")]
        public void TestHashCode1()
        {
            Assert.AreEqual(-1758941372, new User(1, "janedoe",
                "iloveyou").GetHashCode());
        }

        [Test]
        [Category("TestHashCode2")]
        public void TestHashCode2()
        {
            Assert.AreEqual(-1332207447, new User(1, null,
                "iloveyou").GetHashCode());
        }

        [Test]
        [Category("TestHashCode3")]
        public void TestHashCode3()
        {
            Assert.AreEqual(-426522485, new User(1, "janedoe",
                null).GetHashCode());
        }

        [Test]
        [Category("TestSetId")]
        public void TestSetId()
        {
            var user = new User(1, "janedoe", "iloveyou");
            string originalUsername = "janedoe";
            string originalPassword = "iloveyou";
            user.Id = 2;
            Assert.AreEqual(2, user.Id);
            Assert.AreEqual(originalUsername, user.Username);
            Assert.AreEqual(originalPassword, user.Password);
        }

        [Test]
        [Category("TestSetPassword")]
        public void TestSetPassword()
        {
            var user = new User(1, "janedoe", "tmp");
            int originalId = 1;
            string originalUsername = "janedoe";
            user.Password = "iloveyou";
            Assert.AreEqual("iloveyou", user.Password);
            Assert.AreEqual(originalId, user.Id);
            Assert.AreEqual(originalUsername, user.Username);
        }

        [Test]
        [Category("TestSetUsername")]
        public void TestSetUsername()
        {
            var user = new User(1, "tmp", "iloveyou");
            int originalId = 1;
            string originalPassword = "iloveyou";
            user.Username = "janedoe";
            Assert.AreEqual("janedoe", user.Username);
            Assert.AreEqual(originalId, user.Id);
            Assert.AreEqual(originalPassword, user.Password);
        }

        [Test]
        [Category("TestToString")]
        public void TestToString()
        {
            var user = new User(1, "janedoe", "iloveyou");
            string result = user.ToString();
            Assert.AreEqual(string.Format("User(id={0}, username={1}, password={2})",
                user.Id, user.Username, user.Password), result);
            Assert.That(result, Does.Match(@"User\(id=\d+, username=.+, password=.+\)"));
            Assert.That(result.Contains(user.Id.ToString()));
            Assert.That(result.Contains(user.Username));
            Assert.That(result.Contains(user.Password));
        }
    }
}
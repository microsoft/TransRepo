using System;
using System.Collections.Generic;
using NUnit.Framework;

namespace Com.Iluwatar.Partialresponse
{
    [TestFixture]
    public class FieldJsonMapperTest
    {
        private static FieldJsonMapper mapper;

        [OneTimeSetUp]
        public static void SetUp()
        {
            mapper = new FieldJsonMapper();
        }

        [Test]
        

        [Category("ShouldReturnJsonForSpecifiedFieldsInVideo")]
        public void ShouldReturnJsonForSpecifiedFieldsInVideo()
        {
            var fields = new[] { "id", "title", "length" };
            var video = new Video(
                2, "Godzilla Resurgence", 120,
                "Action & drama movie|", "Hideaki Anno", "Japanese"
            );

            var jsonFieldResponse = mapper.ToJson(video, fields);

            var expectedDetails = "{\"id\": 2,\"title\": \"Godzilla Resurgence\",\"length\": 120}";
            Assert.AreEqual(expectedDetails, jsonFieldResponse);
        }
    }

    public class FieldJsonMapper
    {
        public string ToJson(Video video, string[] fields)
        {
            var dictionary = new Dictionary<string, object>();
            foreach (var field in fields)
            {
                switch (field.ToLower())
                {
                    case "id":
                        dictionary[field] = video.Id;
                        break;
                    case "title":
                        dictionary[field] = video.Title;
                        break;
                    case "length":
                        dictionary[field] = video.Length;
                        break;
                }
            }
            return Newtonsoft.Json.JsonConvert.SerializeObject(dictionary);
        }
    }
}
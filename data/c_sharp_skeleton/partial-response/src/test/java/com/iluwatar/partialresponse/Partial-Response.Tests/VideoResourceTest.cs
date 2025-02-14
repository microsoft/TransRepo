using NUnit.Framework;
using Moq;
using System.Collections.Generic;

namespace Com.Iluwatar.Partialresponse
{
    [TestFixture]
    public class VideoResourceTest
    {
        private Mock<IFieldJsonMapper> _fieldJsonMapper;
        private VideoResource _resource;

        [SetUp]
        public void SetUp()
        {
            _fieldJsonMapper = new Mock<IFieldJsonMapper>();
            
            var videos = new Dictionary<int, Video>
            {
                { 
                    1, 
                    new Video(
                        id: 1, 
                        title: "Avatar", 
                        length: 178, 
                        description: "epic science fiction film",
                        director: "James Cameron", 
                        language: "English"
                    ) 
                },
                { 
                    2, 
                    new Video(
                        id: 2, 
                        title: "Godzilla Resurgence", 
                        length: 120, 
                        description: "Action & drama movie|",
                        director: "Hideaki Anno", 
                        language: "Japanese"
                    ) 
                },
                { 
                    3, 
                    new Video(
                        id: 3, 
                        title: "Interstellar", 
                        length: 169, 
                        description: "Adventure & Sci-Fi",
                        director: "Christopher Nolan", 
                        language: "English"
                    ) 
                }
            };
            
            _resource = new VideoResource(_fieldJsonMapper.Object, videos);
        }

        [Test]
        [Category("ShouldGiveVideoDetailsById")]
        public void ShouldGiveVideoDetailsById()
        {
            var actualDetails = _resource.GetDetails(1);

            var expectedDetails = "{\"id\": 1,\"title\": \"Avatar\",\"length\": 178,\"description\": "
                + "\"epic science fiction film\",\"director\": \"James Cameron\",\"language\": \"English\"}";
            Assert.That(actualDetails, Is.EqualTo(expectedDetails));
        }

        [Test]
        [Category("ShouldGiveSpecifiedFieldsInformationOfVideo")]
        public void ShouldGiveSpecifiedFieldsInformationOfVideo()
        {
            var fields = new[] { "id", "title", "length" };

            var expectedDetails = "{\"id\": 1,\"title\": \"Avatar\",\"length\": 178}";
            _fieldJsonMapper
                .Setup(x => x.ToJson(It.IsAny<Video>(), fields))
                .Returns(expectedDetails);

            var actualFieldsDetails = _resource.GetDetails(2, fields);

            Assert.That(actualFieldsDetails, Is.EqualTo(expectedDetails));
        }

        [Test]
        [Category("ShouldAllSpecifiedFieldsInformationOfVideo")]
        public void ShouldAllSpecifiedFieldsInformationOfVideo()
        {
            var fields = new[] { "id", "title", "length", "description", "director", "language" };

            var expectedDetails = "{\"id\": 1,\"title\": \"Avatar\",\"length\": 178,\"description\": "
                + "\"epic science fiction film\",\"director\": \"James Cameron\",\"language\": \"English\"}";
            _fieldJsonMapper
                .Setup(x => x.ToJson(It.IsAny<Video>(), fields))
                .Returns(expectedDetails);

            var actualFieldsDetails = _resource.GetDetails(1, fields);

            Assert.That(actualFieldsDetails, Is.EqualTo(expectedDetails));
        }
    }
}
using System;
using System.Collections.Generic;

namespace Com.Iluwatar.Partialresponse
{
    /// <summary>
    /// The resource record class which serves video information. This class acts as the server in the demo
    /// which has all video details.
    /// </summary>
    public class VideoResource
    {
        private readonly IFieldJsonMapper _fieldJsonMapper;  // 改为使用接口
        private readonly IDictionary<int, Video> _videos;

        /// <summary>
        /// Initializes a new instance of the <see cref="VideoResource"/> class.
        /// </summary>
        /// <param name="fieldJsonMapper">Map object to JSON.</param>
        /// <param name="videos">Initialize resource with existing videos. Acts as database.</param>
        public VideoResource(IFieldJsonMapper fieldJsonMapper, IDictionary<int, Video> videos)  // 改为使用接口
        {
        }

        /// <summary>
        /// Get details.
        /// </summary>
        /// <param name="id">Video ID.</param>
        /// <param name="fields">Fields to get information about.</param>
        /// <returns>Full response if no fields specified else partial response for given field.</returns>
        public string GetDetails(int id, params string[] fields)
        {
            return string.Empty;
        }
    }
}
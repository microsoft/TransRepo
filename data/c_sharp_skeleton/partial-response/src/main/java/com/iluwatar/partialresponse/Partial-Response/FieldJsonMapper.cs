using System;
using System.Linq;
using System.Reflection;
using System.Text;

namespace Com.Iluwatar.Partialresponse
{
    /// <summary>
    /// Map a video to JSON.
    /// </summary>
    public class FieldJsonMapper : IFieldJsonMapper
    {
        /// <summary>
        /// Gets JSON of required fields from video.
        /// </summary>
        /// <param name="video">Object containing video information</param>
        /// <param name="fields">Fields information to get</param>
        /// <returns>JSON of required fields from video</returns>
        public string ToJson(Video video, string[] fields)
        {
            return "";
        }

        private string GetString(Video video, FieldInfo declaredField)
        {
            return "";
        }
    }
}
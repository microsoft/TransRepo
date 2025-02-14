namespace Com.Iluwatar.Partialresponse
{
    public interface IFieldJsonMapper
    {
        string ToJson(Video video, string[] fields);
    }
}
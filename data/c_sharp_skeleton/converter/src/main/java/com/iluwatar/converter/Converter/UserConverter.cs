using System;

namespace Com.Iluwatar.Converter
{
    /**
     * Example implementation of the simple User converter.
     */
    public class UserConverter : Converter<UserDto, User>
    {
        public UserConverter() 
            : base(ConvertToEntity, ConvertToDto)
        {
        }

        private static UserDto ConvertToDto(User user)
        {
            return null;
        }

        private static User ConvertToEntity(UserDto dto)
        {
            return null;
        }
    }
}
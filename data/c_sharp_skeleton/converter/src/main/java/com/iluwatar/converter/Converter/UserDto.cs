using System;

namespace Com.Iluwatar.Converter
{
    /// <summary>
    /// UserDto record.
    /// </summary>
    public record UserDto(string FirstName, string LastName, bool Active, string Email);
}
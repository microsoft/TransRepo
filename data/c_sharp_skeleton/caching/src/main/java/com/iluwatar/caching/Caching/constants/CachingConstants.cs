using System;
namespace Com.Iluwatar.Caching
{
    /// <summary>
    /// Constant class for defining constants.
    /// </summary>
    public sealed class CachingConstants
    {
        /// <summary>
        /// User Account.
        /// </summary>
        public const string USER_ACCOUNT = "user_accounts";
        
        /// <summary>
        /// User ID.
        /// </summary>
        public const string USER_ID = "userID";
        
        /// <summary>
        /// User Name.
        /// </summary>
        public const string USER_NAME = "userName";
        
        /// <summary>
        /// Additional Info.
        /// </summary>
        public const string ADD_INFO = "additionalInfo";

        // Private constructor to prevent instantiation
        private CachingConstants()
        {
        }
    }
}
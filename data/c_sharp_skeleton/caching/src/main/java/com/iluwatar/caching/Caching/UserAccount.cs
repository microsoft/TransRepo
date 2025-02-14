using System;

namespace Com.Iluwatar.Caching
{
    /**
     * Entity class (stored in cache and DB) used in the application.
     */
    public class UserAccount
    {
        /**
         * User Id.
         */
        public string UserId { get; set; }
        /**
         * User Name.
         */
        public string UserName { get; set; }
        /**
         * Additional Info.
         */
        public string AdditionalInfo { get; set; }

        public UserAccount(string userId, string userName, string additionalInfo)
        {
        }

        public override string ToString()
        {
            return "";
        }

        public override bool Equals(object obj)
        {
            return false;
        }

        public override int GetHashCode()
        {
            return 0;
        }
    }
}
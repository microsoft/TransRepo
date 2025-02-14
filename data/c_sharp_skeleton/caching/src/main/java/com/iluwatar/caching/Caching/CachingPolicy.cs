using System;

namespace Com.Iluwatar.Caching
{
    /// <summary>
    /// Enum class containing the four caching strategies implemented in the pattern.
    /// </summary>
    public enum CachingPolicy
    {
        /// <summary>
        /// Through.
        /// </summary>
        Through,

        /// <summary>
        /// Around.
        /// </summary>
        Around,

        /// <summary>
        /// Behind.
        /// </summary>
        Behind,

        /// <summary>
        /// Aside.
        /// </summary>
        Aside
    }

    public static class CachingPolicyExtensions
    {
        /// <summary>
        /// Retrieves the policy value for a CachingPolicy.
        /// </summary>
        public static string GetPolicy(this CachingPolicy cachingPolicy)
        {
            return cachingPolicy switch
            {
                CachingPolicy.Through => "through",
                CachingPolicy.Around => "around",
                CachingPolicy.Behind => "behind",
                CachingPolicy.Aside => "aside",
                _ => throw new ArgumentOutOfRangeException(nameof(cachingPolicy), cachingPolicy, null)
            };
        }
    }
}
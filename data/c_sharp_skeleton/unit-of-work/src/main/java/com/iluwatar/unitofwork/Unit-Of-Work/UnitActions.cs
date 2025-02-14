using System;

namespace com.iluwatar.unitofwork
{
    public enum UnitActions
    {
        Insert,
        Delete,
        Modify
    }

    public static class UnitActionsExtensions
    {
        public static string GetActionValue(this UnitActions action)
        {
            return "";
        }
    }
}

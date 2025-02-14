using System;

namespace com.iluwatar.unitofwork
{
    /**
     * {@link Weapon} is an entity.
     */
    public class Weapon
    {
        public int Id { get; }
        public string Name { get; }

        public Weapon(int id, string name)
        {
            Id = id;
            Name = name;
        }
    }
}
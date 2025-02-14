using System;
using System.Collections.Generic;

namespace com.iluwatar.unitofwork
{
    public class ArmsDealer : IUnitOfWork<Weapon>
    {
        private readonly IDictionary<string, List<Weapon>> _context;
        private readonly WeaponDatabase _weaponDatabase;

        public ArmsDealer(IDictionary<string, List<Weapon>> context, WeaponDatabase weaponDatabase)
        {
        }

        public void RegisterNew(Weapon weapon)
        {
            return;
        }
        
        public void RegisterModified(Weapon weapon)
        {
            return;
        }

        public void RegisterDeleted(Weapon weapon)
        {
            return;
        }

        private void Register(Weapon weapon, string operation)
        {
            return;
        }

        public void Commit()
        {
            return;
        }

        private void CommitInsert()
        {
            return;
        }

        private void CommitModify()
        {
            return;
        }

        private void CommitDelete()
        {
            return;
        }
    }
}
using System;
using System.Collections.Generic;
using NUnit.Framework;

namespace Com.Iluwatar.Doubledispatch
{
    public abstract class CollisionTest<O> where O : GameObject
    {
        /// <summary>
        /// Get the tested object
        /// </summary>
        /// <returns>The tested object, should never return 'null'</returns>
        protected abstract O GetTestedObject();

        /// <summary>
        /// Collide the tested item with the other given item and verify if the damage and fire state is as expected
        /// </summary>
        /// <param name="other">The other object we have to collide with</param>
        /// <param name="otherDamaged">Indicates if the other object should be damaged after the collision</param>
        /// <param name="otherOnFire">Indicates if the other object should be burning after the collision</param>
        /// <param name="thisDamaged">Indicates if the test object should be damaged after the collision</param>
        /// <param name="thisOnFire">Indicates if the other object should be burning after the collision</param>
        public void TestCollision(
            GameObject other, 
            bool otherDamaged, 
            bool otherOnFire,
            bool thisDamaged, 
            bool thisOnFire)
        {
            if (other == null) throw new ArgumentNullException(nameof(other));
            if (GetTestedObject() == null) throw new ArgumentNullException(nameof(GetTestedObject));
            
            var tested = GetTestedObject();
            tested.Collision(other);

            TestOnFire(other, tested, otherOnFire);
            TestDamaged(other, tested, otherDamaged);

            TestOnFire(tested, other, thisOnFire);
            TestDamaged(tested, other, thisDamaged);
        }

        /// <summary>
        /// Test if the fire state of the target matches the expected state after colliding with the given object
        /// </summary>
        /// <param name="target">The target object</param>
        /// <param name="other">The other object</param>
        /// <param name="expectTargetOnFire">The expected state of fire on the target object</param>
        private void TestOnFire(GameObject target, GameObject other, bool expectTargetOnFire)
        {
            var targetName = target.GetType().Name;
            var otherName = other.GetType().Name;

            var errorMessage = expectTargetOnFire
                ? $"Expected [{targetName}] to be on fire after colliding with [{otherName}] but it was not!"
                : $"Expected [{targetName}] not to be on fire after colliding with [{otherName}] but it was!";

            Assert.AreEqual(expectTargetOnFire, target.OnFire, errorMessage);
        }

        /// <summary>
        /// Test if the damage state of the target matches the expected state after colliding with the given object
        /// </summary>
        /// <param name="target">The target object</param>
        /// <param name="other">The other object</param>
        /// <param name="expectedDamage">The expected state of damage on the target object</param>
        private void TestDamaged(GameObject target, GameObject other, bool expectedDamage)
        {
            var targetName = target.GetType().Name;
            var otherName = other.GetType().Name;

            var errorMessage = expectedDamage
                ? $"Expected [{targetName}] to be damaged after colliding with [{otherName}] but it was not!"
                : $"Expected [{targetName}] not to be damaged after colliding with [{otherName}] but it was!";

            Assert.AreEqual(expectedDamage, target.Damaged, errorMessage);
        }
    }
}
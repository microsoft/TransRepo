using System.Collections.Generic;
using NUnit.Framework;

namespace Com.Iluwatar.Typeobject
{
    public class CellPoolTest
    {
        [Test]
        
        [Category("AssignRandomCandyTypesTest")]
        public void AssignRandomCandyTypesTest()
        {
            var cp = new CellPool(10);
            var ht = new Dictionary<string, bool>();
            var parentTypes = 0;
            for (var i = 0; i < cp.RandomCode.Length; i++)
            {
                if (!ht.ContainsKey(cp.RandomCode[i].Name))
                {
                    ht[cp.RandomCode[i].Name] = true;
                }
                if (cp.RandomCode[i].Name == "fruit" || cp.RandomCode[i].Name == "candy")
                {
                    parentTypes++;
                }
            }
            Assert.IsTrue(ht.Count == 5 && parentTypes == 0);
        }
    }
}
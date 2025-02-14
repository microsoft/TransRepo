/*
 * This project is licensed under the MIT license. Module model-view-viewmodel is using ZK framework licensed under LGPL (see lgpl-3.0.txt).
 *
 * The MIT License
 * Copyright © 2014-2022 Ilkka Seppälä
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
using System.Collections.Generic;
using NUnit.Framework;
using Moq;

using com.iluwatar.unitofwork;

/**
 * tests ArmsDealer
 */

public class ArmsDealerTest
{
    private readonly Weapon weapon1 = new Weapon(1, "battle ram");
    private readonly Weapon weapon2 = new Weapon(1, "wooden lance");

    private readonly Dictionary<string, List<Weapon>> context = new Dictionary<string, List<Weapon>>();
    private readonly Mock<WeaponDatabase> weaponDatabase = new Mock<WeaponDatabase>();
    private readonly ArmsDealer armsDealer;

    public ArmsDealerTest()
    {
        armsDealer = new ArmsDealer(context, weaponDatabase.Object);
    }

    [Test]
    

    [Category("ShouldSaveNewStudentWithoutWritingToDb")]
    public void ShouldSaveNewStudentWithoutWritingToDb()
    {
        armsDealer.RegisterNew(weapon1);
        armsDealer.RegisterNew(weapon2);

        Assert.AreEqual(2, context[UnitActionsExtensions.GetActionValue(UnitActions.Insert)].Count);
        weaponDatabase.VerifyNoOtherCalls();
    }

    [Test]
    

    [Category("ShouldSaveDeletedStudentWithoutWritingToDb")]
    public void ShouldSaveDeletedStudentWithoutWritingToDb()
    {
        armsDealer.RegisterDeleted(weapon1);
        armsDealer.RegisterDeleted(weapon2);

        Assert.AreEqual(2, context[UnitActionsExtensions.GetActionValue(UnitActions.Delete)].Count);
        weaponDatabase.VerifyNoOtherCalls();
    }

    [Test]
    

    [Category("ShouldSaveModifiedStudentWithoutWritingToDb")]
    public void ShouldSaveModifiedStudentWithoutWritingToDb()
    {
        armsDealer.RegisterModified(weapon1);
        armsDealer.RegisterModified(weapon2);

        Assert.AreEqual(2, context[UnitActionsExtensions.GetActionValue(UnitActions.Modify)].Count);
        weaponDatabase.VerifyNoOtherCalls();
    }

    [Test]
    

    [Category("ShouldSaveAllLocalChangesToDb")]
    public void ShouldSaveAllLocalChangesToDb()
    {
        context[UnitActionsExtensions.GetActionValue(UnitActions.Insert)] = new List<Weapon> { weapon1 };
        context[UnitActionsExtensions.GetActionValue(UnitActions.Modify)] = new List<Weapon> { weapon1 };
        context[UnitActionsExtensions.GetActionValue(UnitActions.Delete)] = new List<Weapon> { weapon1 };

        armsDealer.Commit();

        weaponDatabase.Verify(db => db.Insert(weapon1), Times.Once);
        weaponDatabase.Verify(db => db.Modify(weapon1), Times.Once);
        weaponDatabase.Verify(db => db.Delete(weapon1), Times.Once);
    }

    [Test]
    

    [Category("ShouldNotWriteToDbIfContextIsNull")]
    public void ShouldNotWriteToDbIfContextIsNull()
    {
        var weaponRepository = new ArmsDealer(null, weaponDatabase.Object);
        weaponRepository.Commit();
        weaponDatabase.VerifyNoOtherCalls();
    }

    [Test]
    

    [Category("ShouldNotWriteToDbIfNothingToCommit")]
    public void ShouldNotWriteToDbIfNothingToCommit()
    {
        var weaponRepository = new ArmsDealer(new Dictionary<string, List<Weapon>>(), weaponDatabase.Object);

        weaponRepository.Commit();

        weaponDatabase.VerifyNoOtherCalls();
    }

    [Test]
    

    [Category("ShouldNotInsertToDbIfNoRegisteredStudentsToBeCommitted")]
    public void ShouldNotInsertToDbIfNoRegisteredStudentsToBeCommitted()
    {
        context[UnitActionsExtensions.GetActionValue(UnitActions.Modify)] = new List<Weapon> { weapon1 };
        context[UnitActionsExtensions.GetActionValue(UnitActions.Delete)] = new List<Weapon> { weapon1 };

        armsDealer.Commit();

        weaponDatabase.Verify(db => db.Insert(weapon1), Times.Never);
    }

    [Test]
    

    [Category("ShouldNotModifyToDbIfNotRegisteredStudentsToBeCommitted")]
    public void ShouldNotModifyToDbIfNotRegisteredStudentsToBeCommitted()
    {
        context[UnitActionsExtensions.GetActionValue(UnitActions.Insert)] = new List<Weapon> { weapon1 };
        context[UnitActionsExtensions.GetActionValue(UnitActions.Delete)] = new List<Weapon> { weapon1 };

        armsDealer.Commit();

        weaponDatabase.Verify(db => db.Modify(weapon1), Times.Never);
    }

    [Test]
    

    [Category("ShouldNotDeleteFromDbIfNotRegisteredStudentsToBeCommitted")]
    public void ShouldNotDeleteFromDbIfNotRegisteredStudentsToBeCommitted()
    {
        context[UnitActionsExtensions.GetActionValue(UnitActions.Insert)] = new List<Weapon> { weapon1 };
        context[UnitActionsExtensions.GetActionValue(UnitActions.Modify)] = new List<Weapon> { weapon1 };

        armsDealer.Commit();

        weaponDatabase.Verify(db => db.Delete(weapon1), Times.Never);
    }
}
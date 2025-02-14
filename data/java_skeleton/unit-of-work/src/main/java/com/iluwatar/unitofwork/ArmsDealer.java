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
package com.iluwatar.unitofwork;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/**
 * {@link ArmsDealer} Weapon repository that supports unit of work for weapons.
 */
@Slf4j
@RequiredArgsConstructor
public class ArmsDealer implements UnitOfWork<Weapon> {

  private final Map<String, List<Weapon>> context;
  private final WeaponDatabase weaponDatabase;

  @Override
  public void registerNew(Weapon weapon) {
      return;
  }

  @Override
  public void registerModified(Weapon weapon) {
      return;
  }

  @Override
  public void registerDeleted(Weapon weapon) {
      return;
  }

  private void register(Weapon weapon, String operation) {
      return;
  }

  /**
   * All UnitOfWork operations are batched and executed together on commit only.
   */
  @Override
  public void commit() {
      return;
  }

  private void commitInsert() {
      return;
  }

  private void commitModify() {
      return;
  }

  private void commitDelete() {
      return;
  }
}

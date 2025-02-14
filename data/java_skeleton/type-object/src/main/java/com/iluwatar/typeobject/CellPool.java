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
package com.iluwatar.typeobject;

import com.google.gson.JsonParseException;
import com.iluwatar.typeobject.Candy.Type;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.List;
import lombok.extern.slf4j.Slf4j;

/**
 * The CellPool class allows the reuse of crushed cells instead of creation of new cells each time.
 * The reused cell is given a new candy to hold using the randomCode field which holds all the
 * candies available.
 */
@Slf4j
public class CellPool {
  private static final SecureRandom RANDOM = new SecureRandom();
  public static final String FRUIT = "fruit";
  public static final String CANDY = "candy";
  List<Cell> pool;
  int pointer;
  Candy[] randomCode;

  CellPool(int num) {
  
  }

  Cell getNewCell() {
      return null;
  }

  void addNewCell(Cell c) {
      return;
  }

  Candy[] assignRandomCandytypes() throws JsonParseException {
      return new Candy[0];
  }
}

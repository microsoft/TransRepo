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

import com.iluwatar.typeobject.Candy.Type;
import java.util.ArrayList;
import java.util.List;
import lombok.extern.slf4j.Slf4j;

/**
 * The CandyGame class contains the rules for the continuation of the game and has the game matrix
 * (field 'cells') and totalPoints gained during the game.
 */

@Slf4j
@SuppressWarnings("java:S3776") //"Cognitive Complexity of methods should not be too high"
public class CandyGame {

  Cell[][] cells;
  CellPool pool;
  int totalPoints;

  CandyGame(int num, CellPool pool) {
  
  }

  static String numOfSpaces(int num) {
      return "";
  }

  void printGameStatus() {
      return;
  }

  List<Cell> adjacentCells(int y, int x) {
      return null;
  }

  boolean continueRound() {
      return false;
  }

  void handleChange(int points) {
      return;
  }

  void round(int timeSoFar, int totalTime) {
      return;
  }

}
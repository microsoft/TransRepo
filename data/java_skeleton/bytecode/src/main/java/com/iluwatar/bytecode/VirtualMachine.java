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
package com.iluwatar.bytecode;

import java.util.Stack;
import java.util.concurrent.ThreadLocalRandom;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;

/**
 * Implementation of virtual machine.
 */
@Getter
@Slf4j
public class VirtualMachine {

  private final Stack<Integer> stack = new Stack<>();

  private final Wizard[] wizards = new Wizard[2];

  /**
   * No-args constructor.
   */
  public VirtualMachine() {
  
  }

  /**
   * Constructor taking the wizards as arguments.
   */
  public VirtualMachine(Wizard wizard1, Wizard wizard2) {
  
  }

  /**
   * Executes provided bytecode.
   *
   * @param bytecode to execute
   */
  public void execute(int[] bytecode) {
      return;
  }

  public void setHealth(int wizard, int amount) {
      return;
  }

  public void setWisdom(int wizard, int amount) {
      return;
  }

  public void setAgility(int wizard, int amount) {
      return;
  }

  public int getHealth(int wizard) {
      return 0;
  }

  public int getWisdom(int wizard) {
      return 0;
  }

  public int getAgility(int wizard) {
      return 0;
  }

  private int randomInt(int min, int max) {
      return 0;
  }
}

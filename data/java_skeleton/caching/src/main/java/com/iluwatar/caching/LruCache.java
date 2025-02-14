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
package com.iluwatar.caching;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.extern.slf4j.Slf4j;


/**
 * Data structure/implementation of the application's cache. The data structure
 * consists of a hash table attached with a doubly linked-list. The linked-list
 * helps in capturing and maintaining the LRU data in the cache. When a data is
 * queried (from the cache), added (to the cache), or updated, the data is
 * moved to the front of the list to depict itself as the most-recently-used
 * data. The LRU data is always at the end of the list.
 */
@Slf4j
public class LruCache {
  /**
   * Static class Node.
   */
  static class Node {
    /**
     * user id.
     */
    private final String userId;
    /**
     * User Account.
     */
    private UserAccount userAccount;
    /**
     * previous.
     */
    private Node previous;
    /**
     * next.
     */
    private Node next;

    /**
     * Node definition.
     *
     * @param id      String
     * @param account {@link UserAccount}
     */
    Node(final String id, final UserAccount account) {
    
    }
  }

  /**
   * Capacity of Cache.
   */
  private int capacity;
  /**
   * Cache {@link HashMap}.
   */
  private Map<String, Node> cache = new HashMap<>();
  /**
   * Head.
   */
  private Node head;
  /**
   * End.
   */
  private Node end;

  /**
   * Constructor.
   *
   * @param cap Integer.
   */
  public LruCache(final int cap) {
  
  }

  /**
   * Get user account.
   *
   * @param userId String
   * @return {@link UserAccount}
   */
  public UserAccount get(final String userId) {
      return null;
  }

  /**
   * Remove node from linked list.
   *
   * @param node {@link Node}
   */
  public void remove(final Node node) {
      return;
  }

  /**
   * Move node to the front of the list.
   *
   * @param node {@link Node}
   */
  public void setHead(final Node node) {
      return;
  }

  /**
   * Set user account.
   *
   * @param userAccount {@link UserAccount}
   * @param userId      {@link String}
   */
  public void set(final String userId, final UserAccount userAccount) {
      return;
  }

  /**
   * Check if Cache contains the userId.
   *
   * @param userId {@link String}
   * @return boolean
   */
  public boolean contains(final String userId) {
      return false;
  }

  /**
   * Invalidate cache for user.
   *
   * @param userId {@link String}
   */
  public void invalidate(final String userId) {
      return;
  }

  /**
   * Check if the cache is full.
   * @return boolean
   */
  public boolean isFull() {
      return false;
  }

  /**
   * Get LRU data.
   *
   * @return {@link UserAccount}
   */
  public UserAccount getLruData() {
      return null;
  }

  /**
   * Clear cache.
   */
  public void clear() {
      return;
  }

  /**
   * Returns cache data in list form.
   *
   * @return {@link List}
   */
  public List<UserAccount> getCacheDataInListForm() {
      return null;
  }

  /**
   * Set cache capacity.
   *
   * @param newCapacity int
   */
  public void setCapacity(final int newCapacity) {
      return;
  }
}

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

import com.iluwatar.caching.database.DbManager;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;

/**
 * The caching strategies are implemented in this class.
 */
@Slf4j
public class CacheStore {
  /**
   * Cache capacity.
   */
  private static final int CAPACITY = 3;

  /**
   * Lru cache see {@link LruCache}.
   */
  private LruCache cache;
  /**
   * DbManager.
   */
  private final DbManager dbManager;

  /**
   * Cache Store.
   * @param dataBaseManager {@link DbManager}
   */
  public CacheStore(final DbManager dataBaseManager) {
  
  }

  /**
   * Init cache capacity.
   * @param capacity int
   */
  public void initCapacity(final int capacity) {
      return;
  }

  /**
   * Get user account using read-through cache.
   * @param userId {@link String}
   * @return {@link UserAccount}
   */
  public UserAccount readThrough(final String userId) {
      return null;
  }

  /**
   * Get user account using write-through cache.
   * @param userAccount {@link UserAccount}
   */
  public void writeThrough(final UserAccount userAccount) {
      return;
  }

  /**
   * Get user account using write-around cache.
   * @param userAccount {@link UserAccount}
   */
  public void writeAround(final UserAccount userAccount) {
      return;
  }

  /**
   * Get user account using read-through cache with write-back policy.
   * @param userId {@link String}
   * @return {@link UserAccount}
   */
  public UserAccount readThroughWithWriteBackPolicy(final String userId) {
      return null;
  }

  /**
   * Set user account.
   * @param userAccount {@link UserAccount}
   */
  public void writeBehind(final UserAccount userAccount) {
      return;
  }

  /**
   * Clears cache.
   */
  public void clearCache() {
      return;
  }

  /**
   * Writes remaining content in the cache into the DB.
   */
  public void flushCache() {
      return;
  }

  /**
   * Print user accounts.
   * @return {@link String}
   */
  public String print() {
      return "";
  }

  /**
   * Delegate to backing cache store.
   * @param userId {@link String}
   * @return {@link UserAccount}
   */
  public UserAccount get(final String userId) {
      return null;
  }

  /**
   * Delegate to backing cache store.
   * @param userId {@link String}
   * @param userAccount {@link UserAccount}
   */
  public void set(final String userId, final UserAccount userAccount) {
      return;
  }

  /**
   * Delegate to backing cache store.
   * @param userId {@link String}
   */
  public void invalidate(final String userId) {
      return;
  }
}

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
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;

/**
 * AppManager helps to bridge the gap in communication between the main class
 * and the application's back-end. DB connection is initialized through this
 * class. The chosen  caching strategy/policy is also initialized here.
 * Before the cache can be used, the size of the  cache has to be set.
 * Depending on the chosen caching policy, AppManager will call the
 * appropriate function in the CacheStore class.
 */
@Slf4j
public class AppManager {
  /**
   * Caching Policy.
   */
  private CachingPolicy cachingPolicy;
  /**
   * Database Manager.
   */
  private final DbManager dbManager;
  /**
   * Cache Store.
   */
  private final CacheStore cacheStore;

  /**
   * Constructor.
   *
   * @param newDbManager database manager
   */
  public AppManager(final DbManager newDbManager) {
  
  }

  /**
   * Developer/Tester is able to choose whether the application should use
   * MongoDB as its underlying data storage or a simple Java data structure
   * to (temporarily) store the data/objects during runtime.
   */
  public void initDb() {
      return;
  }

  /**
   * Initialize caching policy.
   *
   * @param policy is a {@link CachingPolicy}
   */
  public void initCachingPolicy(final CachingPolicy policy) {
      return;
  }

  /**
   * Find user account.
   *
   * @param userId String
   * @return {@link UserAccount}
   */
  public UserAccount find(final String userId) {
      return null;
  }

  /**
   * Save user account.
   *
   * @param userAccount {@link UserAccount}
   */
  public void save(final UserAccount userAccount) {
      return;
  }

  /**
   * Returns String.
   *
   * @return String
   */
  public String printCacheContent() {
      return "";
  }

  /**
   * Cache-Aside save user account helper.
   *
   * @param userAccount {@link UserAccount}
   */
  private void saveAside(final UserAccount userAccount) {
      return;
  }

  /**
   * Cache-Aside find user account helper.
   *
   * @param userId String
   * @return {@link UserAccount}
   */
  private UserAccount findAside(final String userId) {
      return null;
  }
}

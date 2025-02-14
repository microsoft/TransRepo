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

using System;
using System.Data;

namespace Com.Iluwatar.Tablemodule
{
    /**
     * This class organizes domain logic with the user table in the
     * database. A single instance of this class contains the various
     * procedures that will act on the data.
     */
    public class UserTableModule
    {
        /**
         * Public element for creating schema.
         */
        public static readonly string CreateSchemaSql =
                "CREATE TABLE IF NOT EXISTS USERS (ID NUMBER, USERNAME VARCHAR(30) " +
                "UNIQUE, PASSWORD VARCHAR(30))";
        /**
         * Public element for deleting schema.
         */
        public static readonly string DeleteSchemaSql = "DROP TABLE USERS IF EXISTS";
        private readonly IDbConnection _dataSource;

        /**
         * Public constructor.
         *
         * @param userDataSource the data source in the database
         */
        public UserTableModule(IDbConnection userDataSource)
        {
        }

        /**
         * Login using username and password.
         *
         * @param username the username of a user
         * @param password the password of a user
         * @return the execution result of the method
         * @throws SQLException if any error
         */
        public int Login(string username, string password)
        {
            return 0;
        }

        /**
         * Register a new user.
         *
         * @param user a user instance
         * @return the execution result of the method
         * @throws SQLException if any error
         */
        public int RegisterUser(User user)
        {
            return 0;
        }
    }
}
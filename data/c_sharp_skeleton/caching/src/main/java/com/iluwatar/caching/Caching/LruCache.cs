using System;
using System.Collections.Generic;

namespace Com.Iluwatar.Caching
{
    /**
     * Data structure/implementation of the application's cache. The data structure
     * consists of a hash table attached with a doubly linked-list. The linked-list
     * helps in capturing and maintaining the LRU data in the cache. When a data is
     * queried (from the cache), added (to the cache), or updated, the data is
     * moved to the front of the list to depict itself as the most-recently-used
     * data. The LRU data is always at the end of the list.
     */
    public class LruCache
    {
        /**
         * Static class Node.
         */
        public class Node
        {
            public readonly string UserId;
            public UserAccount UserAccount;
            public Node Previous;
            public Node Next;

            /**
             * Node definition.
             *
             * @param id String
             * @param account UserAccount
             */
            public Node(string id, UserAccount account)
            {
                UserId = id;
                UserAccount = account;
            }
        }

        private int _capacity;
        private Dictionary<string, Node> _cache = new Dictionary<string, Node>();
        private Node _head;
        private Node _end;

        /**
         * Constructor.
         *
         * @param cap Integer.
         */
        public LruCache(int cap)
        {
            _capacity = cap;
        }

        /**
         * Get user account.
         *
         * @param userId String
         * @return UserAccount
         */
        public UserAccount Get(string userId)
        {
            if (_cache.ContainsKey(userId))
            {
                Node node = _cache[userId];
                Remove(node);
                SetHead(node);
                return node.UserAccount;
            }
            return null;
        }

        /**
         * Remove node from linked list.
         *
         * @param node Node
         */
        public void Remove(Node node)
        {
            if (node.Previous != null)
            {
                node.Previous.Next = node.Next;
            }
            else
            {
                _head = node.Next;
            }

            if (node.Next != null)
            {
                node.Next.Previous = node.Previous;
            }
            else
            {
                _end = node.Previous;
            }
        }

        /**
         * Move node to the front of the list.
         *
         * @param node Node
         */
        public void SetHead(Node node)
        {
            node.Next = _head;
            node.Previous = null;

            if (_head != null)
            {
                _head.Previous = node;
            }

            _head = node;

            if (_end == null)
            {
                _end = _head;
            }
        }

        /**
         * Set user account.
         *
         * @param userAccount UserAccount
         * @param userId String
         */
        public void Set(string userId, UserAccount userAccount)
        {
            if (_cache.ContainsKey(userId))
            {
                Node old = _cache[userId];
                old.UserAccount = userAccount;
                Remove(old);
                SetHead(old);
            }
            else
            {
                Node newNode = new Node(userId, userAccount);
                if (_cache.Count >= _capacity)
                {
                    _cache.Remove(_end.UserId);
                    Remove(_end);
                    SetHead(newNode);
                }
                else
                {
                    SetHead(newNode);
                }
                _cache[userId] = newNode;
            }
        }

        /**
         * Check if Cache contains the userId.
         *
         * @param userId String
         * @return boolean
         */
        public bool Contains(string userId)
        {
            return _cache.ContainsKey(userId);
        }

        /**
         * Invalidate cache for user.
         *
         * @param userId String
         */
        public void Invalidate(string userId)
        {
            if (_cache.ContainsKey(userId))
            {
                Node toRemove = _cache[userId];
                Remove(toRemove);
                _cache.Remove(userId);
            }
        }

        /**
         * Check if the cache is full.
         * @return boolean
         */
        public bool IsFull()
        {
            return _cache.Count >= _capacity;
        }

        /**
         * Get LRU data.
         *
         * @return UserAccount
         */
        public UserAccount GetLruData()
        {
            return _end != null ? _end.UserAccount : null;
        }

        /**
         * Clear cache.
         */
        public void Clear()
        {
            _head = null;
            _end = null;
            _cache.Clear();
        }

        /**
         * Returns cache data in list form.
         *
         * @return List<UserAccount>
         */
        public List<UserAccount> GetCacheDataInListForm()
        {
            List<UserAccount> list = new List<UserAccount>();
            Node current = _head;
            while (current != null)
            {
                list.Add(current.UserAccount);
                current = current.Next;
            }
            return list;
        }

        /**
         * Set cache capacity.
         *
         * @param newCapacity int
         */
        public void SetCapacity(int newCapacity)
        {
            _capacity = newCapacity;
        }
    }
}

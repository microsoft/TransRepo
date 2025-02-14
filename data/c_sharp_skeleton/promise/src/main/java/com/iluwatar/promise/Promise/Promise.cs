using System;
using System.Threading;
using System.Threading.Tasks;

namespace Promise
{
    public class Promise<T>: PromiseSupport<T>
    {
        private Action fulfillmentAction;
        private Action<Exception> exceptionHandler;
        public bool IsDone => Task.IsCompleted;
        public bool IsCancelled => Task.IsCanceled;

        public T Get()
        {
            return default(T);
        }

        public T Get(TimeSpan timeout)
        {
            return default(T);
        }

        public Promise()
        {
        }

        public void Fulfill(T value)
        {
            return;
        }

        public void FulfillExceptionally(Exception exception)
        {
            return;
        }

        private void HandleException(Exception exception)
        {
            return;
        }

        private void PostFulfillment()
        {
            return;
        }

        public Promise<T> FulfillInAsync(Task<T> task, TaskFactory factory)
        {
            return null;
        }

        public Promise<Unit> ThenAccept(Action<T> action)
        {
            return null;
        }

        public Promise<T> OnError(Action<Exception> exceptionHandler)
        {
            return null;
        }

        public Promise<V> ThenApply<V>(Func<T, V> func)
        {
            return null;
        }

        private class ConsumeAction : Runnable
        {
            private readonly Promise<T> src;
            private readonly Promise<Unit> dest;
            private readonly Action<T> action;

            private ConsumeAction(Promise<T> src, Promise<Unit> dest, Action<T> action)
            {
            }

            public void Run()
            {
                return;
            }
        }

        private class TransformAction<V> : Runnable
        {
            private readonly Promise<T> src;
            private readonly Promise<V> dest;
            private readonly Func<T, V> func;

            private TransformAction(Promise<T> src, Promise<V> dest, Func<T, V> func)
            {
            }

            public void Run()
            {
                return;
            }
        }
    }

    public struct Unit
    {
        public static readonly Unit Value = new Unit();
    }

    public interface Runnable
    {
        void Run();
    }
}
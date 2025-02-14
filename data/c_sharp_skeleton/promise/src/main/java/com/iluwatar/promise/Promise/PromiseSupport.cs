using System;
using System.Threading;
using System.Threading.Tasks;

namespace Promise
{
    public class PromiseSupport<T> : TaskCompletionSource<T>
    {
        private static readonly NLog.Logger LOGGER = NLog.LogManager.GetCurrentClassLogger();

        private const int RUNNING = 1;
        private const int FAILED = 2;
        private const int COMPLETED = 3;

        private readonly object _lock = new object();

        private volatile int state = RUNNING;
        private T value;
        private Exception exception;

        public PromiseSupport() : base(TaskCreationOptions.RunContinuationsAsynchronously)
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

        public bool TrySetCancel()
        {
            return false;
        }

        public bool TrySetResult(T result)
        {
            return false;
        }

        public bool TrySetException(Exception exception)
        {
            return false;
        }

        public bool TrySetCanceled(CancellationToken cancellationToken)
        {
            return false;
        }
    }
}
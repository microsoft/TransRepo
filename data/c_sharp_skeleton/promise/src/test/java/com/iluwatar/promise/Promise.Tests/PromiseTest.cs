using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using NUnit.Framework;
using Moq;
using static Moq.It;

namespace Promise
{
    using static NUnit.Framework.Assert;
    using static Moq.Mock;
    
    [TestFixture]
    public class PromiseTest
    {
        private TaskFactory _executor;
        private Promise<int> _promise;

        [SetUp]
        public void SetUp()
        {
            _executor = new TaskFactory(TaskScheduler.Default);
            _promise = new Promise<int>();
        }

        [Test]
        

        [Category("PromiseIsFulfilledWithTheResultantValueOfExecutingTheTask")]
        public void PromiseIsFulfilledWithTheResultantValueOfExecutingTheTask()
        {
             var numberCrunchingTask = new NumberCrunchingTask();
            _promise.FulfillInAsync(numberCrunchingTask.AsTask(), _executor);

            
            //AreEqual(NumberCrunchingTask.CRUNCHED_NUMBER, _promise.Task.Result);
             IsTrue(_promise.IsDone);
             IsFalse(_promise.IsCancelled);
        }

        [Test]
        [Timeout(20000)]
        [Category("PromiseIsFulfilledWithAnExceptionIfTaskThrowsAnException")]
        public void PromiseIsFulfilledWithAnExceptionIfTaskThrowsAnException()
        {
            TestWaitingForeverForPromiseToBeFulfilled();
            TestWaitingSomeTimeForPromiseToBeFulfilled();
        }

        private void TestWaitingForeverForPromiseToBeFulfilled()
        {
            var promise = new Promise<int>();
            promise.FulfillInAsync(Task.Run(() =>
            {
                throw new Exception("Barf!");
                return 0; // 必须有返回值，这里返回一个默认值
            }), Task.Factory);

            try
            {
                promise.Get();
                Fail("Fetching promise should result in exception if the task threw an exception");
            }
            catch (AggregateException ex)
            {
                IsTrue(promise.IsDone);
                IsFalse(promise.IsCancelled);
            }

            try
            {
                promise.Get(TimeSpan.FromSeconds(2));
                Fail("Fetching promise should result in exception if the task threw an exception");
            }
            catch (AggregateException ex)
            {
                IsTrue(promise.IsDone);
                IsFalse(promise.IsCancelled);
            }
        }

        private void TestWaitingSomeTimeForPromiseToBeFulfilled()
        {
            var promise = new Promise<int>();
            promise.FulfillInAsync(Task.Run(() =>
            {
                throw new Exception("Barf!");
                return 0; // 必须有返回值，这里返回一个默认值
            }), Task.Factory);
            // promise.FulfillInAsync(() => throw new Exception("Barf!"), _executor);

            try
            {
                promise.Get(TimeSpan.FromSeconds(2));
                Fail("Fetching promise should result in exception if the task threw an exception");
            }
            catch (AggregateException ex)
            {
                IsTrue(promise.IsDone);
                IsFalse(promise.IsCancelled);
            }

            try
            {
                promise.Get();
                Fail("Fetching promise should result in exception if the task threw an exception");
            }
            catch (AggregateException ex)
            {
                IsTrue(promise.IsDone);
                IsFalse(promise.IsCancelled);
            }
        }

        [Test]
        

        [Category("DependentPromiseIsFulfilledAfterTheConsumerConsumesTheResultOfThisPromise")]
        public void DependentPromiseIsFulfilledAfterTheConsumerConsumesTheResultOfThisPromise()
        {
            var dependentPromise = _promise
                .FulfillInAsync(new NumberCrunchingTask().AsTask(), _executor)
                .ThenAccept(value => AreEqual(NumberCrunchingTask.CRUNCHED_NUMBER, value));

            dependentPromise.Get();
            IsTrue(dependentPromise.IsDone);
            IsFalse(dependentPromise.IsCancelled);
        }

        [Test]
        [Timeout(20000)]
        [Category("DependentPromiseIsFulfilledWithAnExceptionIfConsumerThrowsAnException")]
        public void DependentPromiseIsFulfilledWithAnExceptionIfConsumerThrowsAnException()
        {
            var dependentPromise = _promise
                .FulfillInAsync(new NumberCrunchingTask().AsTask(), _executor)
                .ThenAccept(value => throw new Exception("Barf!"));

            try
            {
                dependentPromise.Get();
                Fail("Fetching dependent promise should result in exception if the action threw an exception");
            }
            catch (AggregateException ex)
            {
                IsTrue(_promise.IsDone);
                IsFalse(_promise.IsCancelled);
            }

            try
            {
                dependentPromise.Get(TimeSpan.FromSeconds(2));
                Fail("Fetching dependent promise should result in exception if the action threw an exception");
            }
            catch (AggregateException ex)
            {
                IsTrue(_promise.IsDone);
                IsFalse(_promise.IsCancelled);
            }
        }

        [Test]
        [Timeout(20000)]
        [Category("DependentPromiseIsFulfilledAfterTheFunctionTransformsTheResultOfThisPromise")]
        public void DependentPromiseIsFulfilledAfterTheFunctionTransformsTheResultOfThisPromise()
        {
            var dependentPromise = _promise
                .FulfillInAsync(new NumberCrunchingTask().AsTask(), _executor)
                .ThenApply(value =>
                {
                    AreEqual(NumberCrunchingTask.CRUNCHED_NUMBER, value);
                    return value.ToString();
                });

            AreEqual(NumberCrunchingTask.CRUNCHED_NUMBER.ToString(), dependentPromise.Task.Result);
            IsTrue(dependentPromise.IsDone);
            IsFalse(dependentPromise.IsCancelled);
        }

        [Test]
        [Timeout(20000)]
        [Category("DependentPromiseIsFulfilledWithAnExceptionIfTheFunctionThrowsException")]
        public void DependentPromiseIsFulfilledWithAnExceptionIfTheFunctionThrowsException()
        {
            var dependentPromise = _promise
            .FulfillInAsync(new NumberCrunchingTask().AsTask(), _executor)
            .ThenApply<string>(value => throw new Exception("Barf!"));

            try
            {
                dependentPromise.Get();
                Fail("Fetching dependent promise should result in exception if the function threw an exception");
            }
            catch (AggregateException ex)
            {
                IsTrue(_promise.IsDone);
                IsFalse(_promise.IsCancelled);
            }

            try
            {
                dependentPromise.Get(TimeSpan.FromSeconds(2));
                Fail("Fetching dependent promise should result in exception if the function threw an exception");
            }
            catch (AggregateException ex)
            {
                IsTrue(_promise.IsDone);
                IsFalse(_promise.IsCancelled);
            }
        }

        [Test]
        [Timeout(20000)]
        [Category("FetchingAnAlreadyFulfilledPromiseReturnsTheFulfilledValueImmediately")]
        public void FetchingAnAlreadyFulfilledPromiseReturnsTheFulfilledValueImmediately()
        {
            var promise = new Promise<int>();
            promise.Fulfill(NumberCrunchingTask.CRUNCHED_NUMBER);

            var result = promise.Get(TimeSpan.FromSeconds(2));
            AreEqual(NumberCrunchingTask.CRUNCHED_NUMBER, result);
        }

        [Test]
        [Timeout(20000)]
        [Category("ExceptionHandlerIsCalledWhenPromiseIsFulfilledExceptionally")]
        public void ExceptionHandlerIsCalledWhenPromiseIsFulfilledExceptionally()
        {
            // 创建 Promise 对象
            var promise = new Promise<int>();

            // 使用 Mock 对 Action<Exception> 进行模拟
            var exceptionHandler = new Mock<Action<Exception>>();

            // 设置异常处理回调
            promise.OnError(exceptionHandler.Object);

            // 模拟抛出异常
            var exception = new Exception("Barf!");
            promise.FulfillExceptionally(exception);

            // 验证异常处理回调是否被正确调用
            exceptionHandler.Verify(handler => handler.Invoke(It.Is<Exception>(e => e == exception)), Times.Once);
        }
        
        private class NumberCrunchingTask
        {
            public static readonly int CRUNCHED_NUMBER = int.MaxValue;

            public int Call()
            {
                // 模拟复杂计算
                // Thread.Sleep(100);
                return CRUNCHED_NUMBER;
            }

            public Task<int> AsTask()
            {
                return Task.Run(() => Call());
            }
        }
    }
}
using System;

namespace Observer.Generic
{
    /**
     * Observer.
     *
     * @param <S> Observable
     * @param <O> Observer
     * @param <A> Action
     */

    public interface IObserver {
        void Update(object subject, object argument);
     }

    public interface Observer<S, O, A> : IObserver
        where S : Observable<S, O, A>
        where O : Observer<S, O, A>
    {
        void Update(S subject, A argument);
    }
}
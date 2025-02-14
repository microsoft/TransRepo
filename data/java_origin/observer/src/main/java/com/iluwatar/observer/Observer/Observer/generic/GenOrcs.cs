using System;
using System.Collections.Generic;
using static System.String;

namespace Observer.Generic
{
    public class GenOrcs : Race, IObserver
    {
        void IObserver.Update(object subject, object argument)
        {
            if (subject is GenWeather weather && argument is WeatherType weatherType)
            {
                Update(weather, weatherType);
            }
        }

        public void Update(GenWeather weather, WeatherType weatherType)
        {
            return;
        }
    }
}
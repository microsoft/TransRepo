using System;
using static System.Console;
using System.Collections.Generic;

namespace Observer.Generic
{
    public class GenHobbits : Race, IObserver
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
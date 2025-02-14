using System;
using System.Collections.Generic;

namespace Observer.Generic
{
    public class GenWeather : Observable<GenWeather, Race, WeatherType>
    {
        private WeatherType currentWeather;

        public GenWeather()
        {
          
        }

        /// <summary>
        /// Makes time pass for weather.
        /// </summary>
        public void TimePasses()
        {
            // Implementation for making time pass
        }
    }
}
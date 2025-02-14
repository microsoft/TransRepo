using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Observer.Generic
{
    public interface Race : Observer<GenWeather, Race, WeatherType>
    {
    }
}
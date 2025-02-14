using System;
using System.Collections.Generic;
using System.Linq;

namespace Com.Iluwatar.Converter
{
    public class Converter<T, U>
    {
        private readonly Func<T, U> fromDto;
        private readonly Func<U, T> fromEntity;

        public Converter(Func<T, U> fromDto, Func<U, T> fromEntity)
        {
            return;
        }

        public U ConvertFromDto(T dto)
        {
            return default(U);
        }

        public T ConvertFromEntity(U entity)
        {
            return default(T);
        }

        public IList<U> CreateFromDtos(ICollection<T> dtos)
        {
            return null;
        }

        public IList<T> CreateFromEntities(ICollection<U> entities)
        {
            return null;
        }
    }
}
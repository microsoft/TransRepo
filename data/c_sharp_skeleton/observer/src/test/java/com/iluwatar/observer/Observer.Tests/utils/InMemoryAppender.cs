using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;

namespace Observer.Utils
{
    /// <summary>
    /// In-memory Log Appender Utility for capturing log messages.
    /// </summary>
    public class InMemoryAppender : IDisposable
    {
        private readonly List<LogEntry> _logEntries = new();
        private readonly ILoggerFactory _loggerFactory;
        private readonly ILogger _logger;

        /// <summary>
        /// Constructs an InMemoryAppender for a specific logger category based on Type.
        /// </summary>
        /// <param name="type">The Type for the logger category.</param>
        public InMemoryAppender(Type type)
        {
            _loggerFactory = LoggerFactory.Create(builder =>
            {
                builder.AddProvider(new InMemoryLoggerProvider(this));
            });

            _logger = _loggerFactory.CreateLogger(type.FullName ?? "Unknown");
        }

        /// <summary>
        /// Constructs an InMemoryAppender for the root logger.
        /// </summary>
        public InMemoryAppender() : this(typeof(object))
        {
        }

        /// <summary>
        /// Adds a log entry to the in-memory list.
        /// </summary>
        /// <param name="logLevel">The log level.</param>
        /// <param name="message">The log message.</param>
        internal void AddLog(LogLevel logLevel, string message)
        {
            _logEntries.Add(new LogEntry(logLevel, message));
        }

        /// <summary>
        /// Gets the total number of log entries.
        /// </summary>
        /// <returns>The log size.</returns>
        public int GetLogSize()
        {
            return _logEntries.Count;
        }

        /// <summary>
        /// Gets the last logged message.
        /// </summary>
        /// <returns>The last log message.</returns>
        public string GetLastMessage()
        {
            if (_logEntries.Count == 0)
            {
                throw new InvalidOperationException("No logs available.");
            }
            return _logEntries[^1].Message; // Using ^1 to get the last entry
        }

        /// <summary>
        /// Disposes the logger factory.
        /// </summary>
        public void Dispose()
        {
            _loggerFactory?.Dispose();
        }

        /// <summary>
        /// Logs a message using the in-memory logger.
        /// </summary>
        /// <param name="logLevel">The log level.</param>
        /// <param name="message">The log message.</param>
        public void Log(LogLevel logLevel, string message)
        {
            _logger.Log(logLevel, message);
        }

        /// <summary>
        /// Represents a log entry.
        /// </summary>
        private record LogEntry(LogLevel LogLevel, string Message);

        /// <summary>
        /// Custom logger provider for in-memory logging.
        /// </summary>
        private class InMemoryLoggerProvider : ILoggerProvider
        {
            private readonly InMemoryAppender _inMemoryAppender;

            public InMemoryLoggerProvider(InMemoryAppender inMemoryAppender)
            {
                _inMemoryAppender = inMemoryAppender;
            }

            public ILogger CreateLogger(string categoryName)
            {
                return new InMemoryLogger(categoryName, _inMemoryAppender);
            }

            public void Dispose()
            {
                // No resources to dispose in this provider.
            }
        }

        /// <summary>
        /// Custom logger for in-memory logging.
        /// </summary>
        private class InMemoryLogger : ILogger
        {
            private readonly string _categoryName;
            private readonly InMemoryAppender _inMemoryAppender;

            public InMemoryLogger(string categoryName, InMemoryAppender inMemoryAppender)
            {
                _categoryName = categoryName;
                _inMemoryAppender = inMemoryAppender;
            }

            public IDisposable BeginScope<TState>(TState state)
            {
                return null; // No scope support in this implementation.
            }

            public bool IsEnabled(LogLevel logLevel)
            {
                return true; // Enable all log levels.
            }

            public void Log<TState>(LogLevel logLevel, EventId eventId, TState state, Exception exception, Func<TState, Exception, string> formatter)
            {
                if (formatter == null)
                {
                    throw new ArgumentNullException(nameof(formatter));
                }

                var message = formatter(state, exception);
                _inMemoryAppender.AddLog(logLevel, message);
            }
        }
    }
}

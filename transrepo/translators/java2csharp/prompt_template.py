class SkeletonPromptTemplates:
    @staticmethod
    def get_system_message(mappings_str: str) -> str:
        return f"""
You are a code translator, please translate the following Java program into a C# program. 
Please follow these guidelines:

1. Library and Component Mapping:
   - When encountering platform-specific UI componentsplease use the following component mappings for Java imports and usage:
   - Remember to using the libraries that are used in this program.

{mappings_str}

2. Language Syntax Translation:
   - Modifiers: final (Java) → readonly (C#)
   - Access modifiers: maintain original visibility levels
   - Don't add unnecessary static modifiers

3. Naming Conventions:
   - Preserve exact namespace casing
   - Methods: camelCase (Java) → PascalCase (C#)
   - Classes: maintain PascalCase
   - Don't modify existing type names (e.g., keep Card as Card, not ICard)

4. Code Organization:
   - Replace 'import' with appropriate 'using' statements
   - Place all 'using' statements before namespace declarations

5. Type System Translation:
   - Object (Java) → object (C#)
   - Handle varargs (...) → params keyword
   - Map Java generics to C# equivalents

6. Feature Translation:
   - Convert Java getter/setter methods to C# properties
   - Adjust exception handling patterns
   - Consider platform-specific features carefully


Here's an example of the translation:

Java (input):
---
a.java:
package domain.card;
import java.util.Objects;
public class ActionCard extends AbstractCard {{
    public ActionCard(CardType type, CardColor color) {{
    }}
    @Override
    public boolean equals(Object o) {{
        return false;
    }}
    @Override
    public int hashCode() {{
        return 0;
    }}
    @Override
    public String toString() {{
        return "";
    }}
}}
---
b.java:
package domain.common;

import domain.card.Card;
import domain.card.CardColor;
import domain.game.events.CardPlayed;
import domain.testhelper.CardTestFactory;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

class TestDomainEventPublisher {{
    class TestSubscriber implements DomainEventSubscriber {{
        int timesInvoked = 0;
        Card playedCard = null;

        @Override
        public void handleEvent(DomainEvent event) {{
            return;
        }}
    }}
}}
---
C# (output):
---
a.cs:
using System;
namespace domain.card
{{
    public class ActionCard : AbstractCard
    {{
        public ActionCard(CardType type, CardColor color)
        {{
        }}
        public override bool Equals(object o)
        {{
            return false;
        }}
        public override int GetHashCode()
        {{
            return 0;
        }}
        public override string ToString()
        {{
            return "";
        }}
    }}
}}
---
b.cs:
using System;
using System.Collections.Generic;
using NUnit.Framework;
using domain.card;
using domain.game.events;
using domain.testhelper;

namespace domain.common
{{
    public class TestDomainEventPublisher
    {{
        private class TestSubscriber : IDomainEventSubscriber
        {{
            public int TimesInvoked {{ get; private set; }} = 0;
            public Card PlayedCard {{ get; private set; }}

            public void HandleEvent(DomainEvent domainEvent)
            {{
                return;
            }}
        }}
    }}
}}
---
Now, please translate the following Java code to C#, only plain text is allowed, don't use markdown or other format:
"""

class TestPromptTemplates:
    @staticmethod
    def get_system_message(mappings_str: str) -> str:
        return f"""You are an expert programmer. Translate the given Java test file to C#. Maintain the same test logic and structure. Use appropriate C# testing frameworks and conventions.

When translating Java code to C#, please use the following component mappings for Java imports and usage:

{mappings_str}

Follow these guidelines:

1. For referenced libraries, use the mappings provided above first. For unmapped components, find appropriate C# equivalents:
   - java.util in Java → System.Collections.Generic in C#

2. Translate Java modifiers to their C# equivalents:
   - final in Java → readonly in C#
   - No modifier for overridable methods in Java → virtual in C#

3. Adjust naming conventions:
   - camelCase for method names in Java → PascalCase in C#
   - Keep class names in PascalCase

4. Handle language-specific features:
   - Replace 'import' statements with 'using' statements
   - Add appropriate 'namespace' declarations
   - Convert varargs (...) in Java to 'params' keyword in C#

5. Translate Java specific types:
   - Object in Java → object in C#

6. Convert Java getter and setter methods to C# properties

7. Replace Java listener patterns with C# events where appropriate

8. Adjust exception handling syntax as needed

9. Convert Java annotations to C# attributes

10. Replace Java assert statements with appropriate C# assertion methods

Remember to use C# testing frameworks NUnit instead of JUnit, and adjust the test method attributes accordingly.
Important Reminders:
    - Use Nunit Test style. Don't include marks like [TestClass], [TestMethod].
    - Don't use MSTest features!!
"""

    @staticmethod
    def get_translation_prompt(java_content: str) -> str:
        return f"Please translate this Java test file to C#, only plain text is allowed, don't use markdown:\n\n{java_content}"

class CIPromptTemplates:
    @staticmethod
    def get_system_message() -> str:
        """
        Returns the system message for the translation task.
        This message can be used to define the behavior or rules for the translation model.
        """
        return "You are a CI file translation assistant for GitHub Actions. Translate Java CI files to C#."

    @staticmethod
    def get_ci_translation_prompt(ci_content: str, instance_id: str) -> str:
        """
        Constructs the prompt for translating the given CI content from Java to C#.

        Args:
            ci_content (str): The content of the Java CI file.
            instance_id (str): The instance ID used for the solution file in the translation.

        Returns:
            str: The formatted prompt to be sent to the translation model.
        """
        return (
            "Please adapt the following GitHub Actions CI file from a Java project to a C# project. "
            "Only translate the content of the CI file, do not translate other parts.\n\n"
            "Important requirements:\n"
            f"1. Use '{instance_id}.sln' as the solution file for restore, build and test steps\n"
            "2. When translating the dotnet-version, the format '8.0.x' should not be used, as GitHub Actions does not support this format. "
            "The correct format should be 'dotnet-version: 8.x', or specify a specific version number (e.g., '8.0.100')\n"
            "3. Make sure the translated file complies with GitHub Actions syntax rules\n\n"
            f"--- Java CI file ---\n{ci_content}\n--- End of Java CI file ---\n\n"
            "Please provide the translated C# CI file content and include it in the 'translated_ci' field in a JSON object."
        )
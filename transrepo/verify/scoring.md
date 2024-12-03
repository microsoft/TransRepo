# Code Translation Scoring System

This scoring system is designed to evaluate the quality of code translation results, specifically focusing on compilation success and test performance. The system adopts a 100-point scale with two main components:

## Scoring Components

### 1. Build Score (30 points)
The build score evaluates the compilation success of the translated code.

| Condition | Points |
|-----------|--------|
| Successful build without warnings | 30 |
| Successful build with warnings | max(30 - (5 * number of warnings), 0) |
| Build failure | 0 |

### 2. Test Score (70 points)
The test score is calculated based on test execution results and potential runtime issues.

#### Base Test Score
- Calculated as: `(passed_tests / total_tests) * 70`

#### Error Penalties
Deductions are made for various types of test failures:

| Error Type | Penalty Points |
|------------|----------------|
| Assertion Failure | -5 per occurrence |
| Exception Thrown | -10 per occurrence |
| Timeout | -8 per occurrence |
| Memory Error | -15 per occurrence |

## Score Calculation Example

```python
Final Score = Build Score + Test Score

# Example:
# Build: Successful with 1 warning = 20 points
# Tests: 8/10 passed with 1 assertion failure
# Test Score = (8/10 * 70) - (1 * 5) = 51 points
# Final Score = 20 + 51 = 71 points
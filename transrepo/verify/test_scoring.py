import re

class TestScoring:
    def __init__(self):
        # Scoring weights
        self.BUILD_SCORE = 30
        self.TEST_SCORE = 70
        
        # Build penalties
        self.WARNING_PENALTY = 10
        
        # Test error weights
        self.ERROR_WEIGHTS = {
            'assert': 5,    # Assert failure
            'exception': 10, # Exception thrown
            'timeout': 8,   # Timeout
            'memory': 15    # Memory overflow
        }
    
    def parse_build_output(self, build_output):
        """Parse build output to get warnings and errors count"""
        warnings = len(re.findall(r'warning', build_output, re.IGNORECASE))
        errors = len(re.findall(r'error', build_output, re.IGNORECASE))
        return warnings, errors
    
    def parse_test_output(self, test_output):
        """Parse test output to get detailed test results"""
        # Extract test counts
        total_tests = len(re.findall(r'Test Run', test_output))
        passed_tests = len(re.findall(r'Passed!', test_output))
        
        # Extract different types of errors
        assert_failures = len(re.findall(r'Assert\..*failed', test_output, re.IGNORECASE))
        exceptions = len(re.findall(r'Exception:', test_output))
        timeouts = len(re.findall(r'timeout', test_output, re.IGNORECASE))
        memory_errors = len(re.findall(r'OutOfMemoryException', test_output))
        
        return {
            'total': total_tests or 0,  # Ensure non-None values
            'passed': passed_tests or 0,
            'assert_failures': assert_failures,
            'exceptions': exceptions,
            'timeouts': timeouts,
            'memory_errors': memory_errors
        }
    
    def calculate_build_score(self, build_status, build_output=""):
        """Calculate build score"""
        if build_status != 'success':
            return 0
        
        warnings, _ = self.parse_build_output(build_output)
        score = self.BUILD_SCORE
        
        # Apply warning penalties
        if warnings > 0:
            penalty = min(self.WARNING_PENALTY * warnings, self.BUILD_SCORE)
            score -= penalty
            
        return max(0, score)
    
    def calculate_test_score(self, test_results):
        """Calculate test execution score"""
        if not test_results['total']:
            return 0
        
        # Calculate base score from pass rate
        pass_rate = test_results['passed'] / test_results['total']
        base_score = self.TEST_SCORE * pass_rate
        
        # Calculate error penalties
        penalty = (
            test_results['assert_failures'] * self.ERROR_WEIGHTS['assert'] +
            test_results['exceptions'] * self.ERROR_WEIGHTS['exception'] +
            test_results['timeouts'] * self.ERROR_WEIGHTS['timeout'] +
            test_results['memory_errors'] * self.ERROR_WEIGHTS['memory']
        )
        
        return max(0, base_score - penalty)
    
    def calculate_final_score(self, test_results):
        """Calculate comprehensive test result with detailed breakdown"""
        build_status = test_results.get('build', 'failed')
        build_score = self.calculate_build_score(
            build_status,
            test_results.get('build_error', '')
        )
        
        test_score = 0
        test_details = None
        
        if build_status == 'success' and 'test_output' in test_results:
            test_details = self.parse_test_output(test_results['test_output'])
            test_score = self.calculate_test_score(test_details)
        
        return {
            'build_score': build_score,
            'test_score': test_score,
            'total_score': build_score + test_score,
            'test_details': test_details
        }
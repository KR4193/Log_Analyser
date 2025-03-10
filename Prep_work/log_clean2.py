import re

dirty_log_file = "C:/Users/kr4193/Desktop/Log_error_reporter/Prep_work/SMOKE-ZSB-DP12-002.log"
log_file_path = "C:/Users/kr4193/Desktop/Log_error_reporter/Prep_work/clean_smoke.log"

with open(dirty_log_file, 'r') as file:
    lines = file.readlines()

def process_line(line):
    # Match and capture everything after 'D:' or 'I:'
    match = re.search(r'[DI]:\s*(.*)', line)
    if match:
        return match.group(1).strip()  # Return the captured group, stripped of leading/trailing whitespace
    return line.strip()  # If no match, return the line as is

current_suite = None
current_module = None
current_test = None
ans = None
suites = []
inbetween = []
failures = []
to_retrieve = []
log = []
previous_line = None  # Initialize previous_line variable
suite_test_cases = {}  # Dictionary to store suite name as key and failed/error test cases as values

with open(log_file_path, 'w') as output_file:
    for line in lines:
        line = process_line(line)

        # Check for suite start
        suite_match = re.search(r'Entering suite: (\w+)', line)
        if suite_match:
            current_suite = suite_match.group(1)
            suites.append(current_suite)
            suite_test_cases[current_suite] = []  # Initialize list for test cases
            continue

        # Check for module start
        module_match = re.search(r' Execute module', line)
        if module_match:
            current_module = module_match.group(1)
            continue

        # Check for test start
        test_start_match = re.search(r'Running test: (\w+)', line)
        if test_start_match:
            current_test = test_start_match.group(1)
            continue

        # Check for test outcome
        test_outcome_match = re.search(r'test outcome\s*:\s*(\w+)', line, re.IGNORECASE)
        if test_outcome_match:
            result = test_outcome_match.group(1).lower()
            if result in ['failed', 'error']:
                if current_suite and current_test:
                    suite_test_cases[current_suite].append(current_test)
                    for line in inbetween:
                        output_file.write(line + '\n')
                    log.append(inbetween)
                    inbetween.clear()
            current_test = None  # Reset current test
            continue

        # Check for failure
        failure_match = re.search(r'(failed)', line, re.IGNORECASE)
        if failure_match:
            if current_suite and current_module:
                failures.append((suite_match, module_match, line.strip()))

        # Check for the end of the suite and the result
        if current_suite:
            suite_end_match = re.search(r'^Suite', line)
            if suite_end_match:
                result, suite = line.split(" ")[-1], line.split(" ")[-2]
                suite_end_match = None
                if result == 'failed' or result == 'error':
                    to_retrieve.append(suite[:-1])
                    # for line in inbetween:
                    #     output_file.write(line + '\n')
                    # log.append(inbetween)
                    suites.remove(suite[:-1])
                else:
                    suites.remove(suite[:-1])
            if len(suites) == 0:
                inbetween.clear()

        # Check if the current line is the same as the previous line
        if line != previous_line:
            inbetween.append(line)
        previous_line = line  # Update previous_line

# Filter out suites with no failed/error test cases
suite_test_cases = {suite: test_cases for suite, test_cases in suite_test_cases.items() if test_cases}

print(to_retrieve)
print(suite_test_cases)

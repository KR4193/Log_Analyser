import os
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-02-01"
)
log_file_path = "C:/Users/kr4193/Desktop/Log_error_reporter/Prep_work/clean_Geiger_for_LLMs.log"
pytest_path = "C:/Users/kr4193/Downloads/evtstuff/atf/tests/print/clean_cutter.py"
# Read the log content from the file

file = open(pytest_path, "r")
content = file.read()
def read_log_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
log_content = read_log_file(log_file_path)
# print(log_content)
question = "Classify the logs."
response = client.chat.completions.create(
    model="gpt-4o", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant ."},
        {"role": "system", "content": "The fromat of tests is as follows Test suites -> Test modules -> Test cases , Test cases are the lowest level of granularity "},
        {"role": "system", "content": "Test Suites are started at the line Entering suites: <suitename> and ended at Suite <suitename> <result>"},
        {"role": "system", "content": "Test models are started at Execute module: <module_name>"},
        {"role": "system", "content": "Test cases are started at the line Running test: <test_name> and ended at line <test_name>: <result>"}, 
        {"role": "system", "content": "Always Ignore all passed test cases and Suites"},
        {"role": "system", "content": "Always Identify and Classify the Failed tests into one of the 3 categories - Product issues, ATF Script Issues & Setup issues"},
        {"role": "system", "content": "Always display for failed test suites only in the follwing format {Suite, Module,\
          Synopsis of the test Failed, test name, Failure category, Reason for categorisation } "},
        {"role": "user", "content": f"Here is the script that was used to run the test {content}"},
        {"role": "user", "content": f"Here is a log entry for analysis:\n{log_content}\n\nQuestion: {question}\n"},
    ]
)


with open("output_context.txt", "w") as output_file:
    output_file.write(response.choices[0].message.content)
from flask import Flask,render_template
import json

app = Flask(__name__)

# json_data= ''' 
# [{
#   "test_suite": "FipsSGDTests",
#   "test_case": "device_fips_enabled_sgd_type",
#   "test_description": "Test SGD device.fips.enabled type is enum",
#   "classification": "Product issue",
#   "reasoning": "The assertion failure indicates that the expected range for 'device.fips.enabled' is {'no'} but encountered values are {'yes', 'no'}. This discrepancy suggests a potential issue with the product's behavior or configuration."
# },
# {
#   "test_suite": "WlanSGDTest",
#   "test_case": "ip_dhcp_cid_all_set_get",
#   "test_description": "Test the setting and retrieval of DHCP CID all parameter",
#   "classification": "Product issue",
#   "reasoning": "The log indicates that the test ended due to an assertion exception. This likely points to a discrepancy in product behavior or an unexpected output from the product when performing set and get actions on the DHCP cid_all parameter."
# }]'''

# Read the file content
with open('output_context.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()

# Replace HTML entities with actual characters
json_like_content = file_content.replace('&quot;', '"').replace('&#x27;', "'")

# Split the content into separate JSON objects if needed
json_objects = json_like_content.split('}\n{')

# Fix the individual JSON objects by adding braces
fixed_json_objects = []
for index, obj in enumerate(json_objects):
    if index == 0:
        fixed_json_objects.append(obj + '}')
    elif index == len(json_objects) - 1:
        fixed_json_objects.append('{' + obj)
    else:
        fixed_json_objects.append('{' + obj + '}')

# Parse the JSON objects into Python dictionaries
data_list = [json.loads(obj) for obj in fixed_json_objects]

data_dict = json.loads(json_data)


@app.route("/")
def generate_html():
    return render_template("index.html", data=data_dict)

if __name__ == '__main__':
    app.run(debug=True)
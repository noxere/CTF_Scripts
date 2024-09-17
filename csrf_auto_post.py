import requests
import re
import time

# URLs
get_url = '<GET_URL>'  # Replace with the URL used for the GET request
post_url = '<POST_URL>'  # Replace with the URL used for the POST request

# Cookies and headers
cookies = {
    'session': '<SESSION_TOKEN>',  # Replace with the actual session token
    'sessionid': '<SESSION_ID>'    # Replace with the actual session ID
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': '<ORIGIN_URL>',  # Replace with the origin URL
    'Referer': '<REFERER_URL>',  # Replace with the referer URL
    'Connection': 'close'
}

# Loop to post 100 messages
for i in range(1, 101):  # Loop from 1 to 100
    # Step 1: Send GET request to retrieve CSRF token
    response = requests.get(get_url, cookies=cookies, headers=headers)
    if response.status_code == 200:
        print(f"GET request successful for message {i}, extracting CSRF token...")
    else:
        print(f"GET request failed for message {i}. Status code: {response.status_code}")
        continue

    # Step 2: Extract the CSRF token using a regular expression
    pattern = re.search(r'chk:([a-f0-9]{32})', response.text)
    if pattern:
        csrf_token = pattern.group(1)
        print(f"Extracted CSRF token: {csrf_token}")
    else:
        print(f"CSRF token not found for message {i}!")
        continue

    # Step 3: Prepare POST data with message and CSRF token
    msg = f"Message {i} from script"
    post_data = f"msg:{msg}|chk:{csrf_token}"

    # Step 4: Send POST request to submit the message
    post_response = requests.post(post_url, data=post_data, cookies=cookies, headers=headers)
    if post_response.status_code == 200:
        print(f"POST request successful for message {i}!")
    else:
        print(f"POST request failed for message {i}. Status code: {post_response.status_code}")
        print("Response:", post_response.text)

    # Step 5: Introduce a small delay to avoid overwhelming the server
    time.sleep(1)  # Adjust this delay if needed

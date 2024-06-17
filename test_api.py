import requests

def test_api(pc6_value):
    url = "http://localhost:5000/run_analysis"
    params = {'pc6': pc6_value}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        filename = f'{pc6_value}_results.xlsx'
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"File saved as {filename}")
    else:
        print("Failed to fetch results:", response.json())

test_api("123456")  # Replace "123456" with a valid pc6 value for your tests

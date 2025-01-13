import os
import json
import sys

# Base URL for the REST API
BASE_URL = "http://localhost:32098"

def call_health_endpoint():
    """Calls the health endpoint and prints the result."""
    command = f"wget --server-response --output-document health.txt {BASE_URL}/health"
    os.system(command)
    print("\nHealth endpoint response saved to 'health.txt'")
    with open("health.txt", "r") as file:
        print(file.read())

def call_recommend_endpoint(songs):
    """Calls the recommend endpoint with a list of songs."""
    # Convert the list of songs into JSON format
    request_data = json.dumps({"songs": songs})
    # Write the request data to a temporary file
    with open("request.json", "w") as temp_file:
        temp_file.write(request_data)

    # Use wget to send the POST request
    command = f"wget --server-response --output-document recommend.out --header='Content-Type: application/json' --post-file=request.json {BASE_URL}/api/recommend"
    os.system(command)
    print("\nRecommend endpoint response saved to 'recommend.out'")
    with open("recommend.out", "r") as file:
        print(file.read())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cli_client.py [health|recommend] <songs>")
        sys.exit(1)

    endpoint = sys.argv[1].lower()

    if endpoint == "health":
        call_health_endpoint()
    elif endpoint == "recommend":
        if len(sys.argv) < 3:
            print("Usage: python cli_client.py recommend <song1> <song2> ...")
            sys.exit(1)
        songs = sys.argv[2:]
        call_recommend_endpoint(songs)
    else:
        print("Invalid option. Use 'health' or 'recommend'.")

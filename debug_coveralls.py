import os
import sys
from coveralls import Coveralls
from coveralls.api import CoverallsException

print("--- Starting Coveralls Debug Script ---")

# First, confirm the secret token is available in the environment
repo_token = os.environ.get("COVERALLS_REPO_TOKEN")
if not repo_token:
    print("ERROR: COVERALLS_REPO_TOKEN environment variable not found.")
    sys.exit(1)  # Exit with a failure code
else:
    print("OK: Found COVERALLS_REPO_TOKEN environment variable.")

try:
    # Initialize the Coveralls client, passing the token directly
    print("Initializing Coveralls client...")
    coveralls_client = Coveralls(repo_token=repo_token)

    # The wear() method finds the .coverage file, prepares the data, and submits it
    print("Submitting coverage report to the Coveralls API...")
    result = coveralls_client.wear()

    # If the submission is successful, print the response from the server
    print("\n--- S U C C E S S ---")
    print("The report was successfully submitted to Coveralls.")
    print("Server Response:")
    print(result)

except CoverallsException as e:
    # If the Coveralls API returns an error (like 404, 422, etc.)
    print("\n--- F A I L U R E ---")
    print("An API error occurred while submitting the report:")
    print(e)
    sys.exit(1)  # Exit with a failure code so the Travis build fails

except Exception as e:
    # Catch any other unexpected errors (network issues, etc.)
    print("\n--- F A I L U R E ---")
    print("An unexpected error occurred:")
    print(e)
    sys.exit(1)  # Exit with a failure code

print("\n--- Debug Script Finished ---")

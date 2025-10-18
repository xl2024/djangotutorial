import os
import sys
from coveralls import Coveralls
from coveralls.api import CoverallsException

print("--- Starting Coverage Submission Script ---")

# --- Step 1: Get the repo token ---
print("[STEP 1] Getting repository token...")
repo_token = os.environ.get("COVERALLS_REPO_TOKEN")
if not repo_token:
    print("ERROR: COVERALLS_REPO_TOKEN environment variable not found.")
    sys.exit(1)
else:
    print("OK: Found COVERALLS_REPO_TOKEN.")

# --- Step 2: Submit the Report ---
print("[STEP 2] Initializing Coveralls client and submitting report...")
try:
    # Initialize the client, explicitly telling it the service name.
    # It will automatically find all the necessary git info (branch, commit, etc.)
    # from the Travis CI environment variables.
    coveralls_client = Coveralls(service_name="travis-ci", repo_token=repo_token)

    # The wear() method is the correct function to find coverage,
    # gather git info, and submit the report to the Coveralls API.
    result = coveralls_client.wear()

    print("\n--- S U C C E S S ---")
    print("The report was successfully submitted to Coveralls.")
    print("Server Response:")
    print(result)

except (CoverallsException, Exception) as e:
    print("\n--- F A I L U R E ---")
    print("An error occurred while submitting the report to the Coveralls API:")
    print(e)
    sys.exit(1)

print("\n--- Script Finished Successfully ---")

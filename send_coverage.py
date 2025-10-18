import os
import sys
from coveralls import Coveralls
from coveralls.api import CoverallsException

print("--- Starting Manual Coverage Submission Script ---")

# --- Step 1: Manually collect all required CI and Git data ---
print("[STEP 1] Collecting data from Travis CI environment variables...")

# The service_name and repo_token are passed to the constructor.
service_name = "travis-ci"
repo_token = os.environ.get("COVERALLS_REPO_TOKEN")

# The Git metadata is passed later to the wear() method.
git_info = {
    "branch": os.environ.get(
        "TRAVIS_BRANCH", "master"
    ),  # Default to master if not found
    "commit_sha": os.environ.get("TRAVIS_COMMIT"),
    "service_job_id": os.environ.get("TRAVIS_JOB_ID"),
    "service_pull_request": os.environ.get("TRAVIS_PULL_REQUEST", "false"),
}

# --- Step 2: Validate the collected data ---
print("[STEP 2] Validating collected data...")
is_valid = True
# Check the required token first
if not repo_token:
    print("  - ERROR: Required environment variable 'COVERALLS_REPO_TOKEN' is missing.")
    is_valid = False
else:
    print("  - OK: repo_token is set.")

# Check the Git metadata
for key, value in git_info.items():
    if not value:
        print(f"  - WARNING: Environment variable for '{key}' is missing or empty.")
        # Some of these might be optional, so we'll just warn and not fail.
    else:
        print(f"  - OK: {key} = {value}")

if not is_valid:
    print("\nERROR: Cannot proceed without a repository token. Aborting.")
    sys.exit(1)

# --- Step 3: Submit the Report ---
print("[STEP 3] Initializing Coveralls client and submitting report...")
try:
    # Initialize the client with the service name and token.
    coveralls_client = Coveralls(service_name=service_name, repo_token=repo_token)

    # The wear() method will find the .coverage file and use the git_info
    # we provide to enrich the report before sending.
    result = coveralls_client.wear(git_info=git_info)

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

import os
import sys
import subprocess
from coveralls import Coveralls
from coveralls.api import CoverallsException

print("--- Starting Manual Coverage Submission Script ---")

# --- Step 1: Manually Collect Git Information ---
print("[STEP 1] Collecting Git and CI environment data...")
git_info = {
    "branch": os.environ.get("TRAVIS_BRANCH"),
    "commit_sha": os.environ.get("TRAVIS_COMMIT"),
    "service_name": "travis-ci",
    "service_job_id": os.environ.get("TRAVIS_JOB_ID"),
    "repo_token": os.environ.get("COVERALLS_REPO_TOKEN"),
}

# --- Step 2: Validate the Collected Data ---
print("[STEP 2] Validating collected data...")
is_valid = True
for key, value in git_info.items():
    if not value:
        print(
            f"  - ERROR: Required environment variable '{key.upper()}' is missing or empty."
        )
        is_valid = False
    else:
        # Don't print the token itself for security
        if key != "repo_token":
            print(f"  - OK: {key} = {value}")
        else:
            print("  - OK: repo_token is set.")

if not is_valid:
    print("\nERROR: Could not gather all required CI data. Aborting.")
    sys.exit(1)

# --- Step 3: Submit the Report ---
print("[STEP 3] Initializing Coveralls client and submitting report...")
try:
    # Initialize the client and pass the git info directly
    coveralls_client = Coveralls(repo_token=git_info["repo_token"])
    result = coveralls_client.submit(git_info)

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

import os
import sys
from coveralls import Coveralls
from coveralls.api import CoverallsException

print("--- Starting Manual Coverage Submission Script ---")

# --- Step 1: Manually collect all required CI and Git data ---
print("[STEP 1] Collecting data from Travis CI environment variables...")

# The repo_token is passed to the constructor.
repo_token = os.environ.get("COVERALLS_REPO_TOKEN")

# All other service and Git metadata is also passed to the constructor.
service_info = {
    "service_name": "travis-ci",
    "service_job_id": os.environ.get("TRAVIS_JOB_ID"),
    "git": {
        "branch": os.environ.get(
            "TRAVIS_BRANCH", "master"
        ),  # Default to master if not found
        "head": {
            "id": os.environ.get("TRAVIS_COMMIT"),
            "author_name": os.environ.get("GIT_AUTHOR_NAME"),
            "committer_name": os.environ.get("GIT_COMMITTER_NAME"),
            "author_email": os.environ.get("GIT_AUTHOR_EMAIL"),
            "committer_email": os.environ.get("GIT_COMMITTER_EMAIL"),
            "message": "Build from Travis CI",
        },
    },
}

# --- Step 2: Validate the collected data ---
print("[STEP 2] Validating collected data...")
if not repo_token:
    print(
        "  - ERROR: Required environment variable 'COVERALLS_REPO_TOKEN' is missing. Aborting."
    )
    sys.exit(1)
else:
    print("  - OK: repo_token is set.")

print(f"  - OK: branch = {service_info['git']['branch']}")
print(f"  - OK: commit_sha = {service_info['git']['head']['id']}")

# --- Step 3: Submit the Report ---
print("[STEP 3] Initializing Coveralls client and submitting report...")
try:
    # Initialize the client, passing the repo_token and all the service info.
    # This manually overrides the faulty auto-detection.
    coveralls_client = Coveralls(repo_token=repo_token, **service_info)

    # The wear() method will now use the manually provided git_info
    # to enrich the report before sending.
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

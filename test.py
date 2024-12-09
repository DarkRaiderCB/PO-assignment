import os
import json
import pandas as pd
from classifier import classify_email  # Import your classifier function

# Paths to test case directories
IS_PO_DIR = "test_cases/assignment_test_cases/should accept as po"
NOT_PO_DIR = "test_cases/assignment_test_cases/should reject as po"

def load_test_cases(directory):
    """
    Load test cases from a given directory.
    """
    test_cases = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), "r") as file:
                cases = json.load(file)
                test_cases.extend(cases)
    return test_cases

def run_test_cases():
    """
    Run all test cases and display/save results.
    """
    # Load test cases
    is_po_cases = load_test_cases(IS_PO_DIR)
    not_po_cases = load_test_cases(NOT_PO_DIR)
    
    results = []

    # Combine all test cases for iteration
    all_cases = [{"type": "is_po", **case} for case in is_po_cases] + \
                [{"type": "not_po", **case} for case in not_po_cases]

    print("Starting Test Case Execution...\n")
    for idx, test in enumerate(all_cases):
        try:
            # Extract test case details
            subject = test["subject"]
            body = test["body"]
            attachments = test.get("attachments", [])

            # Step 1: Classify email
            classification = classify_email(subject, body, attachments)
            is_po = "non-purchase" not in classification.lower()
            
            # Determine correctness
            expected_type = "is_po" if test["type"] == "is_po" else "not_po"
            status = "Passed" if (is_po and expected_type == "is_po") or (not is_po and expected_type == "not_po") else "Failed"

            # Collect Results
            result = {
                "Test Case": idx + 1,
                "Type": test["type"],
                "Subject": subject,
                "Classification": classification.strip(),
                "Status": status,
            }
            results.append(result)

            # Display the result for the current test case
            print(f"Test Case {idx + 1}:")
            print(f"  Type: {result['Type']}")
            print(f"  Subject: {result['Subject']}")
            print(f"  Classification: {result['Classification']}")
            print(f"  Status: {result['Status']}\n")

        except Exception as e:
            # Handle Errors
            error_result = {
                "Test Case": idx + 1,
                "Type": test["type"],
                "Error": str(e),
                "Status": "Error",
            }
            results.append(error_result)
            print(f"Test Case {idx + 1}: Error encountered - {str(e)}\n")

    # Generate and save the summary table
    df = pd.DataFrame(results)
    summary_file = "test_results_summary.csv"
    df.to_csv(summary_file, index=False)
    print(f"Test results summary saved to {summary_file}")

if __name__ == "__main__":
    run_test_cases()

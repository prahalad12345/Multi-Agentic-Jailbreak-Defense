import subprocess

def check_clingo_file(filepath):
    # Run Clingo
    result = subprocess.run(
        ["clingo", filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stderr = result.stderr.strip()
    print(result.returncode)
    # Only consider lines with 'error' that are not 'info' or 'warning'
    real_errors = [
        line for line in stderr.splitlines()
        if ": error:" in line.lower() #and not any(kw in line.lower() for kw in ["info:", "warning:"])
    ]

    # Also catch 'parsing failed' or return code != 0 as a hard error
    if result.returncode != 0 or "parsing failed" in stderr.lower():
        if real_errors:
            print("❌ Clingo reported an error:\n")
            print("\n".join(real_errors))
        else:
            print("✅ Clingo syntax appears correct.")
        return False

    print("✅ Clingo syntax appears correct.")
    return True

# Example usage
if __name__ == "__main__":
    filepath = "observing"  # Replace with your file
    check_clingo_file(filepath)

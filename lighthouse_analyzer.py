import subprocess
import json
import validators

LIGHTHOUSE_PATH = r"C:\Users\Akansh\AppData\Roaming\npm\lighthouse.cmd"

def run_lighthouse(url, output_file="lighthouse_report.json"):
    # Validate URL
    if not validators.url(url):
        return {"error": "Invalid URL"}

    try:
        # Run Lighthouse in headless mode
        command = [
            LIGHTHOUSE_PATH, url, "--quiet", "--no-update-notifier",
            "--output=json", f"--output-path={output_file}"
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Read and parse the report
        with open(output_file, "r", encoding="utf-8") as f:
            report = json.load(f)

        # Extract key metrics
        return {
            "performance_score": report["categories"]["performance"]["score"] * 100,
            "accessibility_score": report["categories"]["accessibility"]["score"] * 100,
            "seo_score": report["categories"]["seo"]["score"] * 100,
            "best_practices_score": report["categories"]["best-practices"]["score"] * 100,
        }

    except subprocess.CalledProcessError as e:
        return {"error": f"Lighthouse failed: {e}"}
    except json.JSONDecodeError:
        return {"error": "Failed to parse Lighthouse report"}


# Example usage
if __name__ == "__main__":
    url = input("Enter website URL: ")
    result = run_lighthouse(url)
    print(result)

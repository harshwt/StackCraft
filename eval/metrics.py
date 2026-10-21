import json
from pathlib import Path
import sys
import time

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main import run_pipeline

def evaluate():
    dataset_path = PROJECT_ROOT / "eval" / "dataset.json"
    if not dataset_path.exists():
        print(f"Dataset not found at {dataset_path}")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    results = []
    print(f"Running evaluation on {len(dataset)} test prompts...\n")

    for i, item in enumerate(dataset, 1):
        if i > 1:
            time.sleep(2)
        prompt = item.get("prompt", "")
        print(f"[{i}/{len(dataset)}] Testing: {prompt}")

        start = time.time()
        try:
            res = run_pipeline(prompt)
            duration = round(time.time() - start, 2)
            valid = res.get("valid", False)
            code = res.get("generated_code", "")
            has_code = bool(code and len(code) > 50)

            results.append({
                "prompt": prompt,
                "latency_sec": duration,
                "valid_schema": valid,
                "code_generated": has_code,
                "repaired": res.get("repaired", False),
                "error": None if valid else res.get("message")
            })
            status = "PASS" if valid and has_code else "FAIL"
            print(f" -> {status} (Latency: {duration}s, Valid: {valid})")
        except Exception as e:
            duration = round(time.time() - start, 2)
            results.append({
                "prompt": prompt,
                "latency_sec": duration,
                "valid_schema": False,
                "code_generated": False,
                "error": str(e)
            })
            print(f" -> ERROR ({duration}s): {e}")

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r["valid_schema"] and r["code_generated"])
    avg_latency = round(sum(r["latency_sec"] for r in results) / total, 2) if total else 0

    print("\n" + "=" * 50)
    print("EVALUATION SUMMARY")
    print(f"Total Test Cases: {total}")
    print(f"Success Rate:     {passed}/{total} ({round(passed / total * 100, 1) if total else 0}%)")
    print(f"Avg Latency:      {avg_latency}s")
    print("=" * 50)

    output_path = PROJECT_ROOT / "eval" / "results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Detailed results saved to {output_path}")

if __name__ == "__main__":
    evaluate()
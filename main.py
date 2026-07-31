import subprocess
import time
import sys

def run_step(step_name, command):
    print(f"\n{'='*50}")
    print(f"Starting {step_name}...")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*50}")

    start_time = time.time()

    try:
        subprocess.run(command, check=True)
        elapsed = time.time() - start_time
        print(f"✅ {step_name} completed in {elapsed:.2f} sec\n")

    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time
        print(f"❌ {step_name} failed in {elapsed:.2f} sec")
        print(e)
        sys.exit(1)

def main():
    print("🚀 Starting Customer Churn Prediction Pipeline")

    py = sys.executable

    steps = [
        ("Data Generation", [py, "data/generate_data.py"]),
        ("Data Ingestion", [py, "notebooks/01_ingest.py"]),
        ("EDA", [py, "notebooks/02_eda.py"]),
        ("Train Baselines", [py, "-m", "src.train_baselines"]),
        ("Tune Optuna", [py, "-m", "src.tune_optuna"]),
        ("Train Final", [py, "-m", "src.train_final"]),
        ("Evaluate", [py, "-m", "src.evaluate"]),
        ("Predict", [py, "-m", "src.predict"]),
    ]

    total_start = time.time()

    for name, cmd in steps:
        run_step(name, cmd)

    total_elapsed = time.time() - total_start
    print(f"🎉 Full pipeline completed in {total_elapsed:.2f} sec")

if __name__ == "__main__":
    main()
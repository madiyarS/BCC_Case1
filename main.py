#!/usr/bin/env python3
"""
Main script to run all analysis scripts in sequence
"""

import subprocess
import sys
import os
import time
from datetime import datetime

def run_script(script_name):
    """
    Run a Python script and handle errors
    
    Args:
        script_name (str): Name of the script to run (without .py extension)
    
    Returns:
        bool: True if successful, False if failed
    """
    
    script_path = f"{script_name}.py"
    
    print(f"📋 Running {script_name}...")
    print("-" * 50)
    
    # Check if script exists
    if not os.path.exists(script_path):
        print(f"❌ Error: {script_path} not found!")
        return False
    
    try:
        # Record start time
        start_time = time.time()
        
        # Run the script
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        
        # Record end time
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Print output if any
        if result.stdout:
            print("Output:")
            print(result.stdout)
        
        print(f"✅ {script_name} completed successfully in {execution_time:.2f} seconds")
        print()
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}:")
        print(f"Return code: {e.returncode}")
        
        if e.stdout:
            print("Standard Output:")
            print(e.stdout)
        
        if e.stderr:
            print("Error Output:")
            print(e.stderr)
        
        print()
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error running {script_name}: {e}")
        print()
        return False

def main():
    """
    Main function to run all scripts in sequence
    """
    
    # List of scripts to run in order
    scripts = [
        "client_analyzer",
        "transfer_analyzer", 
        "combiner",
        "adder",
        "assumptions",
        "finalres"
    ]
    
    print("🚀 Starting Data Processing Pipeline")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # Track overall progress
    total_scripts = len(scripts)
    successful_scripts = 0
    failed_scripts = []
    
    # Record total start time
    pipeline_start_time = time.time()
    
    # Run each script in sequence
    for i, script in enumerate(scripts, 1):
        print(f"🔄 Step {i}/{total_scripts}: {script}")
        
        success = run_script(script)
        
        if success:
            successful_scripts += 1
            print(f"✅ Step {i} completed successfully")
        else:
            failed_scripts.append(script)
            print(f"❌ Step {i} failed!")
            
            # Ask user if they want to continue
            print()
            choice = input("Do you want to continue with the next script? (y/n): ").lower().strip()
            
            if choice not in ['y', 'yes']:
                print("🛑 Pipeline execution stopped by user.")
                break
        
        print("=" * 60)
    
    # Calculate total execution time
    pipeline_end_time = time.time()
    total_execution_time = pipeline_end_time - pipeline_start_time
    
    # Print final summary
    print()
    print("📊 PIPELINE EXECUTION SUMMARY")
    print("=" * 60)
    print(f"Total scripts: {total_scripts}")
    print(f"Successful: {successful_scripts}")
    print(f"Failed: {len(failed_scripts)}")
    print(f"Total execution time: {total_execution_time:.2f} seconds")
    
    if failed_scripts:
        print(f"Failed scripts: {', '.join(failed_scripts)}")
    
    print("=" * 60)
    
    if successful_scripts == total_scripts:
        print("🎉 All scripts completed successfully!")
        return 0
    else:
        print("⚠️  Some scripts failed. Please check the error messages above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
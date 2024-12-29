import pygame
import json
import os
from subprocess import run

# File to save traces
TRACES_FILE = "traces.json"

def load_previous_traces():
    """Load previous traces from the file."""
    if os.path.exists(TRACES_FILE):
        with open(TRACES_FILE, "r") as file:
            return json.load(file)
    return []

def save_current_traces(traces):
    """Save current traces to the file."""
    with open(TRACES_FILE, "w") as file:
        json.dump(traces, file)

def add_red_trace_code(original_script):
    """Modify the script dynamically to include red traces."""
    # Load the content of the script
    with open(original_script, "r") as file:
        script = file.read()

    # Code to render previous traces
    trace_code = """
# Injected Code: Render previous trials in red
if os.path.exists("traces.json"):
    with open("traces.json", "r") as file:
        previous_traces = json.load(file)
    for trace in previous_traces:
        for point in trace:
            pygame.draw.circle(screen, (255, 0, 0), (int(point[0]), int(point[1])), 1)
"""

    # Inject the code after clearing the screen (assuming `screen.fill` is called)
    modified_script = script.replace("screen.fill((0, 0, 0))", f"screen.fill((0, 0, 0))\n{trace_code}")

    return modified_script

def run_simulation():
    """Run the modified simulation."""
    original_script = "simulation.py"  # Replace with your script's filename
    modified_script_content = add_red_trace_code(original_script)

    # Save modified script temporarily
    temp_script = "temp_simulation.py"
    with open(temp_script, "w") as file:
        file.write(modified_script_content)

    # Run the modified script
    run(["python", temp_script])

    # Cleanup
    if os.path.exists(temp_script):
        os.remove(temp_script)

def main():
    # Load the previous traces
    traces = load_previous_traces()

    # Run the simulation with injected trace functionality
    run_simulation()

    # Save the traces back after running
    # Ensure the simulation script appends traces to a variable named `current_traces`
    current_traces = []  # Replace with logic to extract traces if needed
    save_current_traces(current_traces)

if __name__ == "__main__":
    main()

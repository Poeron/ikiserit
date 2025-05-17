#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
# We don't actually need numpy for this script

# We need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

# Import traci after setting SUMO_HOME
import traci

# Constant definitions
MIN_GREEN_TIME = 20  # Minimum green light duration in seconds
MAX_GREEN_TIME = 60  # Maximum green light duration in seconds
YELLOW_TIME = 3      # Yellow light duration in seconds as in original configuration
JUNCTION_ID = "J8_joined"  # The junction ID from your network

# States in your traffic light:
# G = yeşil (green), y = sarı (yellow), r = kırmızı (red)
# Original phases:
# phase 0: "GGGGrrrrGGGGGGGGrrGGGGrr" - J5 (North) and J7 (South) green
# phase 1: "yyGGrrrrGGyyyyGGrrGGyyrr" - Yellow transition
# phase 2: "rrGGGGGGGGrrrrGGGGGGrrGG" - J6 (East) and J8 (West) green
# phase 3: "rrGGyyyyGGrrrrGGyyGGrryy" - Yellow transition

def run():
    # Start SUMO as a subprocess and connect with traci
    sumoBinary = "sumo-gui"
    sumoCmd = [sumoBinary, "-c", "sumo.sumocfg"]
    traci.start(sumoCmd)
    
    print("Adaptive Traffic Light Control script started...")
    
    # Dictionary mapping junction IDs to their corresponding edges
    junctions = {
        "J5": {"position": "North", "incoming": ["E0"], "outgoing": ["-E0", "E7"]},
        "J6": {"position": "East", "incoming": ["-E3"], "outgoing": ["E3", "E4"]},
        "J7": {"position": "South", "incoming": ["-E2"], "outgoing": ["E2", "E5"]},
        "J8": {"position": "West", "incoming": ["-E1"], "outgoing": ["E1", "E6"]}
    }
    
    # Initialize state
    current_phase = traci.trafficlight.getPhase(JUNCTION_ID)
    last_phase_change = traci.simulation.getTime()
    active_phase = 0  # 0: North-South, 1: East-West
    
    # Main simulation loop
    step = 0
    while step < 3600:  # Run for 1 hour (3600 seconds)
        traci.simulationStep()
        step += 1
        
        # Check if we need to evaluate traffic density
        current_time = traci.simulation.getTime()
        phase_duration = current_time - last_phase_change
        current_phase = traci.trafficlight.getPhase(JUNCTION_ID)
        
        # Only evaluate on green phases (0 or 2) and after minimum green time
        if (current_phase == 0 or current_phase == 2) and phase_duration >= MIN_GREEN_TIME:
            
            # Calculate vehicle density for each junction
            densities = {}
            for junction_id, data in junctions.items():
                total_vehicles = 0
                total_length = 0
                
                # Count vehicles on incoming edges to this junction
                for edge in data["incoming"]:
                    try:
                        lanes = traci.edge.getLaneNumber(edge)
                        edge_length = traci.lane.getLength(f"{edge}_0") * lanes
                        
                        for lane_idx in range(lanes):
                            lane_id = f"{edge}_{lane_idx}"
                            total_vehicles += traci.lane.getLastStepVehicleNumber(lane_id)
                        
                        total_length += edge_length
                    except:
                        print(f"Warning: Could not get data for edge {edge}")
                
                # Calculate vehicle density (vehicles per meter)
                if total_length > 0:
                    densities[junction_id] = total_vehicles / total_length
                else:
                    densities[junction_id] = 0
                
                print(f"{junction_id} ({data['position']}) density: {densities[junction_id]:.4f}")
            
            # Decide if we should switch phases based on densities
            should_switch = False
            
            # Current active directions
            if current_phase == 0:  # North-South green
                current_directions = ["J5", "J7"]
                opposite_directions = ["J6", "J8"]
                active_phase = 0
            else:  # East-West green (phase 2)
                current_directions = ["J6", "J8"]
                opposite_directions = ["J5", "J7"]
                active_phase = 1
            
            # Get average density for current green directions
            current_density = sum(densities[j] for j in current_directions) / len(current_directions)
            
            # Get average density for currently red directions
            opposite_density = sum(densities[j] for j in opposite_directions) / len(opposite_directions)
            
            print(f"Current green density: {current_density:.4f}, Waiting density: {opposite_density:.4f}")
            
            # Logic for switching:
            # 1. If max time reached
            # 2. If opposite directions have significantly higher density
            if phase_duration >= MAX_GREEN_TIME:
                should_switch = True
                reason = "maximum green time reached"
            elif opposite_density > current_density * 1.5:
                should_switch = True
                reason = "significantly higher density in waiting directions"
            
            # Perform the switch if needed
            if should_switch:
                print(f"Switching traffic light phase because {reason}.")
                
                # First switch to yellow
                next_yellow_phase = 1 if current_phase == 0 else 3
                traci.trafficlight.setPhase(JUNCTION_ID, next_yellow_phase)
                
                # Wait for yellow phase
                for i in range(YELLOW_TIME):
                    traci.simulationStep()
                    step += 1
                
                # Then switch to next green phase
                next_phase = 2 if current_phase == 0 else 0
                traci.trafficlight.setPhase(JUNCTION_ID, next_phase)
                
                # Update state
                last_phase_change = traci.simulation.getTime()
                active_phase = 1 - active_phase  # Toggle between 0 and 1
                
                if next_phase == 0:
                    print("Switched to NORTH-SOUTH green")
                else:
                    print("Switched to EAST-WEST green")
    
    traci.close()
    print("Simulation completed")

# Main entry point
if __name__ == "__main__":
    run()

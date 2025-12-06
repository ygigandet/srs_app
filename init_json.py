# pylint: disable=missing-module-docstring

import json

import pandas as pd

# ------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------

data = {
    "theme": ["indexing"],
    "exercise_name": ["indexing1"],
    "json": ["drilling_machine1.json"],
    "last_reviewed": ["1970-01-01"],
    "instructions": ["indexing1.txt"],
    "answer": ["indexing1.py"],
}

memory_state_python_df = pd.DataFrame(data)

# ------------------------------------------------------------
# JSON FILES
# ------------------------------------------------------------

drilling_machines = [
    {
        "machine_id": "DM-001",
        "name": "Deep Driller 3000",
        "location": {
            "latitude": 29.7355,
            "longitude": -95.3635,
            "region": "Gulf of Mexico",
            "country": "USA",
        },
        "status": "Operational",
        "specifications": {
            "type": "Offshore",
            "depth_capacity_meters": 10000,
            "drilling_speed_meters_per_day": 300,
            "crew_size": 40,
            "power_source": ["Diesel, Electric"],
        },
        "last_maintenance_date": "10/07/2024",
        "next_maintenance_due": "10/12/2024",
        "contact_information": {
            "operator_company": "Oceanic Drilling Inc.",
            "contact_person": "John Smith",
            "phone": "+1-555-123-4567",
            "email": "john.smith@oceanicdrilling.com",
        },
    },
    {
        "machine_id": "DM-2",
        "name": "Land Rover 200",
        "location": {
            "latitude": 37.7749,
            "longitude": -107.909,
            "region": "San Juan Basin",
            "country": "USA",
        },
        "status": "Under Maintenance",
        "specifications": {
            "type": "Onshore",
            "depth_capacity_miles": 7,
            "drilling_speed_miles_per_day": 0.3,
            "crew_size": 25,
            "power_source": "Electric",
        },
        "last_maintenance_date": "2024-07-15",
        "next_maintenance_due": "2025-01-15",
    },
    {
        "machine_id": "DM-3",
        "name": "Land Rover 2000",
        "location": {
            "latitude": 38.7749,
            "longitude": -104.909,
            "region": "San Diego Basin",
            "country": "USA",
        },
        "status": "Active",
        "specifications": {
            "type": "Onshore",
            "depth_capacity_miles": 6,
            "drilling_speed_miles_per_day": 0.2,
            "crew_size": 22,
            "power_source": "Electric",
        },
        "last_maintenance_date": "2024-06-22",
        "next_maintenance_due": "2025-01-03",
        "contact_information": {
            "operator_company": "Pacific Drilling Inc.",
            "contact_person": "Smith John",
            "phone": "+1-555-123-4567",
            "email": "john.smith@oceanicdrilling.com",
        },
    },
    {
        "machine_ID": "DM-4",
        "name": "Land Rover 400",
        "location": {
            "latitude": 37.78,
            "longitude": -107.9092,
            "region": "San Juan Basin",
            "country": "USA",
        },
        "status": "Active",
        "specifications": {
            "type": "Onshore",
            "depth_capacity_meters": 10459.5,
            "drilling_speed_meters_per_day": 434,
            "crew_size": 25,
            "power_source": "Electric",
        },
        "last_maintenance_date": "2024-07-19",
        "next_maintenance_due": "2025-01-19",
        "contact_information": {
            "operator_company": "Pacific Drilling Inc.",
            "contact_person": "Smith John",
            "phone": "+1-555-123-4567",
            "email": "john.smith@oceanicdrilling.com",
        },
    },
    {
        "machine_ID": "DM-05",
        "name": "Land Rover 500",
        "location": {
            "latitude": 37.88,
            "longitude": -107.9192,
            "region": "San Diego Basin",
            "country": "USA",
        },
        "status": "Inactive",
        "specifications": {
            "type": "Onshore",
            "depth_capacity_meters": 8459.5,
            "drilling_speed_meters_per_day": 374,
            "crew_size": 20,
            "power_source": ["Electric", "Diesel"],
        },
        "last_maintenance_date": "2024-07-19",
        "next_maintenance_due": "2025-01-19",
        "contact_information": {
            "operator_company": "Pacific Drilling Inc.",
            "contact_person": "Smith John",
            "phone": "+1-555-123-4567",
            "email": "john.smith@oceanicdrilling.com",
        },
        "type": "C",
    },
]

for i, dm in enumerate(drilling_machines):
    file_name = f"data/drilling_machine{i+1}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(dm, f)

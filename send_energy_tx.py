import csv
import requests
import time

csv_file = "p2p_energy_sim_dataset.csv"

with open(csv_file, newline='') as file:
    reader = csv.DictReader(file)

    for row in reader:

        timestamp = row["timestamp"]
        house = row["house"]
        energy = float(row["energy_kwh"])

        # determine buy or sell
        if energy > 0:
            action = "sell"
        else:
            action = "buy"

        tx_data = f"{timestamp},{house},{action},{energy}"

        r = requests.get(
            "http://localhost:26657/broadcast_tx_commit",
            params={"tx": f'"{tx_data}"'}
        )

        print("Sent:", tx_data)

        # simulate real smart meter delay
        time.sleep(1)
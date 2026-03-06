import pandas as pd
from market import energy_market

data = pd.read_csv("meterData/p2p_energy_sim_dataset.csv")
data["interval_start"] = pd.to_datetime(data["interval_start"])
data = data.sort_values("interval_start")
grouped = data.groupby("interval_start")

UTILITY_PRICE = 0.15

for time, group in grouped:

    net = {}
    p2p_prices = {}

    for _, row in group.iterrows():
        house = row["house"]
        consumption = row["consumption_kwh"]
        generation = row["pv_generation_kwh"]
        net_energy = generation - consumption
        net[house] = net_energy

        # Read per-house P2P price from CSV
        p2p_prices[house] = row["p2p_price_usd_per_kwh"]

    transactions = energy_market(net, p2p_prices, UTILITY_PRICE)

    print("\nTime:", time)
    for t in transactions:
        print(t)
    print("Number of transactions:", len(transactions))
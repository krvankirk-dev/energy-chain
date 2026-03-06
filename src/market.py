def energy_market(net_energy, p2p_prices, utility_price):
    """
    net_energy: dict of house -> net energy (positive=seller, negative=buyer)
    p2p_prices: dict of house -> price per kWh (only used for buyers)
    utility_price: fixed price for utility
    """

    sellers = {house: energy for house, energy in net_energy.items() if energy > 0}
    buyers = {house: -energy for house, energy in net_energy.items() if energy < 0}

    transactions = []

    for buyer, demand in buyers.items():
        remaining_demand = demand

        for seller in list(sellers.keys()):
            available = sellers[seller]
            trade = min(remaining_demand, available)

            if trade > 0:
                # Use buyer's P2P price
                price = p2p_prices.get(buyer, 0.10)  # fallback to 0.10 if missing

                transactions.append({
                    "seller": seller,
                    "buyer": buyer,
                    "energy_kwh": trade,
                    "price": price
                })

                sellers[seller] -= trade
                remaining_demand -= trade

            if sellers[seller] == 0:
                del sellers[seller]

            if remaining_demand <= 0:
                break

        # Any remaining energy comes from the Utility
        if remaining_demand > 0:
            transactions.append({
                "seller": "Utility",
                "buyer": buyer,
                "energy_kwh": remaining_demand,
                "price": utility_price
            })

    return transactions
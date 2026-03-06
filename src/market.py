def energy_market(net_energy, p2p_prices, utility_price, utility_buy_price=0.05):
    """
    net_energy: dict of house -> net energy (positive=seller, negative=buyer)
    p2p_prices: dict of house -> price per kWh (for buyers)
    utility_price: price for buying from utility (if demand > supply)
    utility_buy_price: price for utility buying excess energy from sellers
    """

    # Separate sellers and buyers
    sellers = {house: energy for house, energy in net_energy.items() if energy > 0}
    buyers = {house: -energy for house, energy in net_energy.items() if energy < 0}

    transactions = []

    # First, match buyers to sellers
    for buyer, demand in buyers.items():
        remaining_demand = demand

        for seller in list(sellers.keys()):
            available = sellers[seller]
            trade = min(remaining_demand, available)

            if trade > 0:
                price = p2p_prices.get(buyer, 0.10)  # buyer’s P2P price
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

        # Any remaining demand goes to Utility at regular utility price
        if remaining_demand > 0:
            transactions.append({
                "seller": "Utility",
                "buyer": buyer,
                "energy_kwh": remaining_demand,
                "price": utility_price
            })

    # Now check for **excess energy from sellers** that wasn't sold to any buyer
    for seller, remaining in sellers.items():
        if remaining > 0:
            transactions.append({
                "seller": seller,
                "buyer": "Utility",
                "energy_kwh": remaining,
                "price": utility_buy_price
            })

    return transactions
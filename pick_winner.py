import requests
import random

IS_PICK_WINNER = False
SOME_STRING = "BLOAT 69"
CHAIN_ID = 43114
CONTRACT_ADDRESS = "0x21727B2981d7780fd22EfB2b8C8aC926b3E62f3B"
PAGE = 1
OFFSET = 1000  # number of results returned
RAFFLE_MIN_HOLDING = 5_000_000_000 * (10**18)
EXCLUDE_ADDRESSES = ["0xDCCC964Cc5D5641ac4c9133EcCbdA2892C954434"] # Liquidity pool address

print(f"Welcome to $BLOAT raffle - {SOME_STRING}")
print(f"Minimum eligible token balance for the raffle: {RAFFLE_MIN_HOLDING / (10**18):,.0f}")

def get_token_holder_list(chain_id, contract_address, page, offset):
    url = f"https://api.routescan.io/v2/network/mainnet/evm/{chain_id}/etherscan/api"
    params = {
        "module": "token",
        "action": "tokenholderlist",
        "contractaddress": contract_address,
        "page": page,
        "offset": offset,
    }

    response = requests.get(url, params=params)
    return response.json()


def make_raffle(eligible_token_holders):
    for holder in eligible_token_holders:
        holder["TokenHolderQuantity"] = int(holder["TokenHolderQuantity"])

    total_quantity = sum(
        holder["TokenHolderQuantity"] for holder in eligible_token_holders
    )

    ranges = []
    start = 0
    for holder in eligible_token_holders:
        end = start + holder["TokenHolderQuantity"]
        ranges.append(
            {"holder": holder["TokenHolderAddress"], "start": start, "end": end}
        )
        start = end
    random_number = random.randint(0, total_quantity - 1)

    winner = next(
        holder["holder"]
        for holder in ranges
        if holder["start"] <= random_number < holder["end"]
    )
    
    print(f"The winner is: {winner}")


if __name__ == "__main__":
    result = get_token_holder_list(CHAIN_ID, CONTRACT_ADDRESS, PAGE, OFFSET)

    # Check if the request was successful
    if result["status"] == "1":
        token_holders = result["result"]
        print(f"Number of token holders: {len(token_holders )}")

        eligible_token_holders = [
            entry
            for entry in token_holders
            if int(entry["TokenHolderQuantity"]) >= RAFFLE_MIN_HOLDING
            and entry["TokenHolderAddress"] not in EXCLUDE_ADDRESSES
        ]

        print(f"Number of eligible token holders: {len(eligible_token_holders )}")

        if(IS_PICK_WINNER):
            make_raffle(eligible_token_holders)

    else:
        print(f"Error: {result['message']}")

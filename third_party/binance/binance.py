# utils/binance_api.py
import asyncio
from typing import Optional, Tuple
from binance import AsyncClient

ENVIRONMENT = "production"

async def connect_binance(api_key: str, api_secret: str, environment: str = "testnet", retries: int = 5, delay: int = 5) -> Tuple[Optional[AsyncClient], Optional[bool]]:

    """
    Connect to Binance API (testnet or production) with retry logic.
    Returns: (AsyncClient, is_testnet)
    """
    for attempt in range(1, retries + 1):
        try:
            testnet_flag = environment.lower() != ENVIRONMENT
            client = await AsyncClient.create(api_key=api_key, api_secret=api_secret, testnet=testnet_flag)
            print(f"✅ Connected to Binance {'testnet' if testnet_flag else ENVIRONMENT }")
            return client, testnet_flag
        except Exception as e:
            print(f"⚠ Attempt {attempt} failed: {e}")
            if attempt < retries:
                await asyncio.sleep(delay)
    return None, None

async def get_account_balance(client: AsyncClient, asset: str):
    """Return balance for a specific asset"""
    info = await client.get_account()
    balances = {item["asset"]: float(item["free"]) for item in info["balances"]}
    return {asset: balances.get(asset, 0.0)}

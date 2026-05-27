---
name: coindcx-futures-api
description: >
  Use when working with CoinDCX perpetual futures — questions about REST endpoints,
  WebSocket connections, authentication, order placement, position management, margin,
  leverage, funding, or any query referencing CoinDCX, DCX, or docs.coindcx.com.
---

# CoinDCX Futures API Skill

This skill covers the CoinDCX Futures API (REST + WebSocket). All endpoints are for
**perpetual futures contracts** only. For full request/response schemas and code examples,
see `references/endpoints.md`.

**Not covered:** Spot trading, legacy/v1 API, fiat payment APIs.

---

## Authentication

All **private** endpoints require HMAC-SHA256 authentication:

```python
import hmac, hashlib, json, time

key    = "YOUR_API_KEY"
secret = "YOUR_SECRET"
secret_bytes = bytes(secret, encoding='utf-8')

timeStamp = int(round(time.time() * 1000))
body = { "timestamp": timeStamp, ... }  # add your payload fields

json_body = json.dumps(body, separators=(',', ':'))
signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

headers = {
    'Content-Type': 'application/json',
    'X-AUTH-APIKEY': key,
    'X-AUTH-SIGNATURE': signature
}
```

**Key rules:**
- Timestamp must be current EPOCH ms — orders older than **10 seconds** are rejected.
- Public endpoints (market data, instrument info) need **no auth**.
- Private endpoints (orders, positions, wallet) require the headers above.

---

## Base URLs

| Type | URL |
|------|-----|
| Private REST | `https://api.coindcx.com` |
| Public REST | `https://public.coindcx.com` |
| WebSocket | `wss://stream.coindcx.com` |

---

## Endpoint Overview

### Public — Market Data (no auth)

| Purpose | Method | Path |
|---------|--------|------|
| List active instruments | GET | `/exchange/v1/derivatives/futures/data/active_instruments?margin_currency_short_name[]=USDT` |
| Get instrument details | GET | `/exchange/v1/derivatives/futures/data/instrument?pair=B-BTC_USDT&margin_currency_short_name=USDT` |
| Real-time trade history | GET | `/exchange/v1/derivatives/futures/data/trades?pair={instrument_name}` |
| Order book | GET | `https://public.coindcx.com/market_data/v3/orderbook/{instrument}-futures/50` |
| Candlesticks | GET | `https://public.coindcx.com/market_data/candlesticks?pair=&from=&to=&resolution=&pcode=f` |
| Current prices (all pairs) | GET | `https://public.coindcx.com/market_data/v3/current_prices/futures/rt` |

Candlestick resolutions: `1` (1min), `5` (5min), `60` (1hr), `1D` (1day).
Order book depth: `10`, `20`, or `50`.

### Private — Market Data (auth required)

| Purpose | Method | Path |
|---------|--------|------|
| Pair stats (24h change, high/low, long/short %) | GET | `/api/v1/derivatives/futures/data/stats?pair=B-ETH_USDT` |
| Currency conversion rate (USDT↔INR) | GET | `/api/v1/derivatives/futures/data/conversions` |

### Private — Orders (auth required)

| Purpose | Method | Path |
|---------|--------|------|
| List orders | POST | `/exchange/v1/derivatives/futures/orders` |
| Create order | POST | `/exchange/v1/derivatives/futures/orders/create` |
| Cancel order | POST | `/exchange/v1/derivatives/futures/orders/cancel` |
| Cancel all open orders (global) | POST | `/exchange/v1/derivatives/futures/positions/cancel_all_open_orders` |
| Cancel all open orders for position | POST | `/exchange/v1/derivatives/futures/positions/cancel_all_open_orders_for_position` |
| Edit order (USDT only) | POST | `/exchange/v1/derivatives/futures/orders/edit` |

### Private — Positions (auth required)

| Purpose | Method | Path |
|---------|--------|------|
| Get positions (paginated or by pair/id) | POST | `/exchange/v1/derivatives/futures/positions` |
| Update leverage | POST | `/exchange/v1/derivatives/futures/positions/update_leverage` |
| Add margin | POST | `/exchange/v1/derivatives/futures/positions/add_margin` |
| Remove margin | POST | `/exchange/v1/derivatives/futures/positions/remove_margin` |
| Create TP/SL orders | POST | `/exchange/v1/derivatives/futures/positions/create_tpsl` |
| Exit position (quick close) | POST | `/exchange/v1/derivatives/futures/positions/exit` |
| Change margin type (isolated↔crossed) | POST | `/exchange/v1/derivatives/futures/positions/margin_type` |
| Cross margin details | GET | `/exchange/v1/derivatives/futures/positions/cross_margin_details` |
| Position transactions (PnL history) | POST | `/exchange/v1/derivatives/futures/positions/transactions` |

### Private — Wallet & History (auth required)

| Purpose | Method | Path |
|---------|--------|------|
| Wallet details | GET | `/exchange/v1/derivatives/futures/wallets` |
| Wallet transfer (spot↔futures) | POST | `/exchange/v1/derivatives/futures/wallets/transfer` |
| Wallet transactions | GET | `/exchange/v1/derivatives/futures/wallets/transactions?page=1&size=1000` |
| Trade history | POST | `/exchange/v1/derivatives/futures/trades` |

---

## Order Types

| Type | Description |
|------|-------------|
| `market_order` | Fills immediately at best available price |
| `limit_order` | Fills at specified price or better |
| `stop_limit` | Triggers a limit order when stop price is hit |
| `stop_market` | Triggers a market order when stop price is hit |
| `take_profit_limit` | TP trigger → limit order |
| `take_profit_market` | TP trigger → market order |

**Stop/TP price rules:**
- Buy Stop Limit: stop > LTP, limit > stop
- Buy TP Limit: stop < LTP, limit > stop and limit < LTP
- Sell Stop Limit: stop < LTP, limit < stop
- Sell TP Limit: stop > LTP, limit < stop and limit > LTP

**Time-in-force options:** `good_till_cancel`, `immediate_or_cancel`, `fill_or_kill`
*Do not include `time_in_force` for market orders.*

---

## Key Concepts

- **Margin modes:** `USDT` or `INR`. Default is USDT. Cross margin only supported on USDT.
- **Position margin type:** `crossed` (cross) or `isolated`. NULL = isolated.
- **Leverage:** Must match the existing position's leverage or order will be rejected. Set it once via `update_leverage` before placing orders.
- **active_pos:** Positive = long, negative = short. Units are in the underlying asset.
- **Funding:** Happens every `funding_frequency` hours (typically 8h).
- **Pair format:** Always `B-{ASSET}_USDT` or `B-{ASSET}_INR`, e.g. `B-BTC_USDT`.

---

## WebSocket (Socket.IO)

Connect to `wss://stream.coindcx.com` using `socketio.AsyncClient`.

### Joining channels

```python
# Public channel (no auth needed)
await sio.emit('join', {'channelName': 'B-BTC_USDT@trades-futures'})

# Private channel (auth required)
body = {"channel": "coindcx"}
json_body = json.dumps(body, separators=(',', ':'))
signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
await sio.emit('join', {'channelName': 'coindcx', 'authSignature': signature, 'apiKey': key})
```

Send a **ping every 25 seconds** to keep the connection alive.

### WebSocket Events

| Channel | Event | Data |
|---------|-------|------|
| `B-{pair}@trades-futures` | `new-trade` | price, quantity, timestamp, is_maker |
| `B-{pair}@prices-futures` | `price-change` | LTP price |
| `B-{pair}@orderbook@{depth}-futures` | `depth-snapshot` | asks/bids dict |
| `B-{pair}_{interval}-futures` | `candlestick` | OHLCV + timestamps |
| `currentPrices@futures@rt` | `currentPrices@futures#update` | mark prices for all pairs |
| `coindcx` (private) | `df-order-update` | order status updates |
| `coindcx` (private) | `df-position-update` | position updates (same fields as REST position) |
| `coindcx` (private) | `balance-update` | wallet balance |

Candlestick intervals: `1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `8h`, `1d`, `3d`, `1w`, `1M`

---

## Common Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad request (invalid params, insufficient funds, out-of-range price) |
| 401 | Unauthorized — wrong API key or signature |
| 404 | Not found |
| 422 | Unprocessable — e.g. leverage mismatch, quantity out of range |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
| 503 | Service Unavailable — temporarily offline for maintenance |

---

## Reference Files

- `references/endpoints.md` — Full request/response field definitions for every endpoint,
  with Python code examples. Read this when you need exact field names, types, or constraints
  not covered in the summary above.
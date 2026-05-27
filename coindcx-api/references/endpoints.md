# CoinDCX Futures API — Full Endpoint Reference

This file contains comprehensive request/response schemas and field definitions.
For quick reference and overview, see the parent SKILL.md.

---

## Table of Contents
1. [Instrument Endpoints](#1-instrument-endpoints)
2. [Order Endpoints](#2-order-endpoints)
3. [Position Endpoints](#3-position-endpoints)
4. [Wallet & History](#4-wallet--history)
5. [WebSocket — Full Details](#5-websocket--full-details)
6. [Glossary / Field Abbreviations](#6-glossary--field-abbreviations)

---

## 1. Instrument Endpoints

### Get Active Instruments
```
GET https://api.coindcx.com/exchange/v1/derivatives/futures/data/active_instruments
  ?margin_currency_short_name[]=USDT
  # or: ?margin_currency_short_name[]=INR
```
Returns a flat list of active pair strings, e.g. `["B-BTC_USDT", "B-ETH_USDT", ...]`

---

### Get Instrument Details
```
GET https://api.coindcx.com/exchange/v1/derivatives/futures/data/instrument
  ?pair=B-BTC_USDT&margin_currency_short_name=USDT
```

**Key response fields:**

| Field | Description |
|-------|-------------|
| `pair` | Instrument identifier, e.g. `B-AAVE_USDT` |
| `status` | `active` or `inactive` |
| `kind` | Always `perpetual` |
| `settlement` | Always `never` for perpetuals |
| `settle_currency_short_name` | Currency in which contracts are bought/sold (e.g. `USDT`) |
| `quote_currency_short_name` | Currency in which the price is quoted |
| `position_currency_short_name` | Underlying crypto asset (e.g. `AAVE`) |
| `underlying_currency_short_name` | Same as `position_currency_short_name` |
| `unit_contract_value` | Always `1.0` for perpetual contracts |
| `price_increment` | Tick size for price. Limit order prices must be multiples. |
| `quantity_increment` | Tick size for quantity. |
| `min_trade_size` | Minimum quantity of a trade that can be settled on exchange |
| `min_quantity` / `max_quantity` | Quantity bounds |
| `min_price` / `max_price` | Price bounds |
| `min_notional` | Minimum order value in USDT |
| `max_market_order_quantity` | Max quantity for market orders |
| `max_notional` | Ignore this |
| `maker_fee` / `taker_fee` | Fee rates (e.g. 0.025 = 0.025%) |
| `funding_frequency` | Hours between funding events (usually 8) |
| `exit_only` | If `true`, no new positions; can only reduce/cancel |
| `expiry_time` | Ignore this (perpetuals never expire) |
| `multiplier_up` | Buy limit orders: price ≤ LTP × (1 + multiplier_up/100) |
| `multiplier_down` | Sell limit orders: price ≥ LTP × (1 − multiplier_down/100) |
| `liquidation_fee` | Fee on liquidation trades |
| `dynamic_position_leverage_details` | `{ "leverage": max_notional }` — tiered leverage limits |
| `dynamic_safety_margin_details` | `{ "notional": rate }` — tiered maintenance margin rates |
| `time_in_force_options` | Supported TIF values |
| `order_types` | Supported order types |
| `margin_currency_short_name` | `USDT` or `INR` |
| `safety_percentage` | Ignore this |
| `quanto_to_settle_multiplier` | Ignore this (always `1`) |
| `is_inverse` | Ignore this (always `false`) |
| `is_quanto` | Ignore this (always `false`) |
| `allow_post_only` | Ignore this |
| `allow_hidden` | Ignore this |

**Maintenance margin example:**
Response `{"50000": 1.5, "100000": 2.0, ...}` means:
- Position 60K USDT → maintenance = 50K×1.5% + 10K×2.0% = 950 USDT
- Position liquidates when available margin < 950 USDT

---

### Get Trade History (Public — real-time)
```
GET https://api.coindcx.com/exchange/v1/derivatives/futures/data/trades?pair=B-MKR_USDT
```
Returns list of recent trades: `price`, `quantity`, `timestamp`, `is_maker`.
Prefer WebSocket for real-time data.

---

### Get Current Prices RT (Public)
```
GET https://public.coindcx.com/market_data/v3/current_prices/futures/rt
```
No auth needed. Returns current prices for all futures pairs.

Response structure:
```json
{
  "ts": 1720429586580,
  "vs": 54009972,
  "prices": {
    "B-NTRN_USDT": {
      "fr": 5e-05,
      "h": 0.4027,
      "l": 0.3525,
      "v": 18568384.9349,
      "ls": 0.4012,
      "pc": 4.834,
      "mkt": "NTRNUSDT",
      "btST": 1720429583629,
      "mp": 0.40114525,
      "efr": 5e-05,
      "bmST": 1720429586000
    }
  }
}
```

| Field | Meaning |
|-------|---------|
| `fr` | Funding rate |
| `h` | 24h high |
| `l` | 24h low |
| `v` | 24h volume |
| `ls` | Last price |
| `pc` | Price change percent |
| `mkt` | Market symbol (e.g. `NTRNUSDT`) |
| `btST` | TPE tick send time |
| `ctRT` | CoinDCX receive time of the TPE tick |
| `skw` | Skew value (internal metric, informational) |
| `mp` | Mark price |
| `efr` | Effective funding rate |
| `bmST` | TPE mark price send time |
| `cmRT` | CoinDCX receive time of the mark price |

---

### Get Pair Stats (Auth required)
```
GET https://api.coindcx.com/api/v1/derivatives/futures/data/stats?pair=B-ETH_USDT
```
Body: `{ "timestamp": ... }`

Response:
```json
{
  "price_change_percent": { "1H": -0.15, "1D": 1.41, "1W": -11.95, "1M": -17.34 },
  "high_and_low": {
    "1D": { "h": 3098.0, "l": 2821.26 },
    "1W": { "h": 3498.91, "l": 2800.0 }
  },
  "position": {
    "count_percent": { "long": 93.2, "short": 6.8 },
    "value_percent": { "long": 91.48, "short": 8.52 }
  }
}
```

Periods: `1H`, `1D`, `1W`, `1M`. `position` shows percentage of traders long vs short.

---

### Get Currency Conversion (Auth required)
```
GET https://api.coindcx.com/api/v1/derivatives/futures/data/conversions
```
Body: `{ "timestamp": ... }`

Returns USDT ↔ INR conversion price used by CoinDCX for INR-margined futures.

| Field | Description |
|-------|-------------|
| `symbol` | e.g. `USDTINR` |
| `conversion_price` | The fixed conversion rate applied to INR futures |
| `last_updated_at` | When the rate was last changed (may change on extreme market moves) |

---

### Get Order Book (Public)
```
GET https://public.coindcx.com/market_data/v3/orderbook/{instrument}-futures/{depth}
  # depth: 10, 20, or 50
  # Example: /market_data/v3/orderbook/B-MKR_USDT-futures/50
```
Response: `{ "ts": epoch_ms, "vs": version, "asks": {"price":"qty",...}, "bids": {...} }`

---

### Get Candlesticks (Public)
```
GET https://public.coindcx.com/market_data/candlesticks
  ?pair=B-MKR_USDT&from=1704100940&to=1705483340&resolution=1D&pcode=f
```

| Param | Values |
|-------|--------|
| `resolution` | `1` (1min), `5` (5min), `60` (1hr), `1D` (1day) |
| `from` / `to` | EPOCH seconds |
| `pcode` | Always `f` for futures |

Response fields per bar: `open`, `high`, `low`, `close`, `volume`, `time` (EPOCH ms).

---

## 2. Order Endpoints

All order endpoints require authentication. POST bodies must be signed.

### List Orders
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/orders
```

**Request body:**
```json
{
  "timestamp": 1705000000000,
  "status": "open",
  "side": "buy",
  "page": "1",
  "size": "10",
  "margin_currency_short_name": ["USDT"]
}
```

| Field | Required | Values |
|-------|----------|--------|
| `status` | YES | `open`, `filled`, `cancelled`, `partially_filled`, `partially_cancelled`, `rejected`, `untriggered` |
| `side` | YES | `buy` or `sell` |
| `page` | YES | Page number |
| `size` | YES | Records per page |
| `margin_currency_short_name` | OPTIONAL | `["USDT"]` (default), `["INR"]`, or `["INR","USDT"]` |

**Key response fields per order:**

> **Note:** `fee_amount` and `ideal_margin` values are in USDT even for INR-margined futures orders.

| Field | Description |
|-------|-------------|
| `id` | Order UUID |
| `pair` | e.g. `B-ETH_USDT` |
| `side` | `buy` / `sell` |
| `status` | `OPEN`, `FILLED`, `CANCELED`, `PARTIALLY_FILLED`, `PARTIALLY_CANCELED`, `REJECTED`, `UNTRIGGERED` |
| `order_type` | `limit_order`, `market_order`, `stop_limit`, `stop_market`, `take_profit_limit`, `take_profit_market` |
| `notification` | `no_notification` or `email_notification` |
| `price` | Limit price (market price at placement for market orders) |
| `stop_price` | Trigger price for stop/TP orders |
| `avg_price` | Average fill price |
| `total_quantity` | Total quantity placed |
| `remaining_quantity` | Unfilled quantity |
| `cancelled_quantity` | Cancelled quantity |
| `leverage` | Leverage used |
| `maker_fee` / `taker_fee` / `fee_amount` | Fee details |
| `ideal_margin` | Ignore this |
| `stop_trigger_instruction` | Ignore this |
| `order_category` | Ignore this |
| `stage` | `default`, `exit`, `liquidate`, `tpsl_exit` |
| `group_id` | ID shared by all split parts of a large order |
| `liquidation_fee` | Fee if the trade was for a liquidation order |
| `position_margin_type` | `crossed` or `isolated` (NULL = isolated) |
| `display_message` | Ignore this |
| `group_status` | Ignore this |
| `metatags` | Ignore this |
| `created_at` / `updated_at` | Timestamps (EPOCH ms) |
| `take_profit_price` / `stop_loss_price` | TP/SL attached to order; applies to entire position once order begins to fill |
| `margin_currency_short_name` | `USDT` or `INR` |
| `settlement_currency_conversion_price` | INR/USDT conversion (INR futures only) |

---

### Create Order
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/orders/create
```

**Request body:**
```json
{
  "timestamp": 1705647376759,
  "order": {
    "side": "sell",
    "pair": "B-ID_USDT",
    "order_type": "market_order",
    "price": null,
    "stop_price": null,
    "total_quantity": 33,
    "leverage": 10,
    "notification": "no_notification",
    "time_in_force": null,
    "take_profit_price": 0.40,
    "stop_loss_price": 0.25
  }
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `side` | YES | `buy` or `sell` |
| `pair` | YES | e.g. `B-ETH_USDT` |
| `order_type` | YES | `market_order`, `limit_order`, `stop_limit`, `stop_market`, `take_profit_limit`, `take_profit_market` |
| `price` | YES (limit) | NULL for market orders |
| `stop_price` | YES (stop/TP orders) | Trigger price |
| `total_quantity` | YES | Must meet min/max/increment constraints |
| `leverage` | OPTIONAL | Must match existing position leverage |
| `notification` | YES | `no_notification` or `email_notification` |
| `time_in_force` | OPTIONAL | `good_till_cancel`, `fill_or_kill`, `immediate_or_cancel`. **Omit for market orders.** |
| `margin_currency_short_name` | OPTIONAL | `USDT` (default) or `INR` |
| `position_margin_type` | OPTIONAL | `isolated` or `crossed`. Cross only on USDT. |
| `take_profit_price` | OPTIONAL | Only on `market_order` / `limit_order`. Applies to whole position. |
| `stop_loss_price` | OPTIONAL | Only on `market_order` / `limit_order`. Applies to whole position. |
| `hidden` | NO | Ignore this — not supported |
| `post_only` | NO | Ignore this — not supported |

**Stop/TP price constraints:**

| Order Type | Side | Constraints |
|-----------|------|-------------|
| stop_limit | buy | stop > LTP; limit > stop |
| take_profit_limit | buy | stop < LTP; limit > stop AND limit < LTP |
| stop_limit | sell | stop < LTP; limit < stop |
| take_profit_limit | sell | stop > LTP; limit < stop AND limit > LTP |

**Error codes:**

| Code | Message | Reason |
|------|---------|--------|
| 422 | Order leverage must equal position leverage | Leverage in request doesn't match current position leverage |
| 422 | Quantity for limit variant orders should be less than X | Total quantity exceeds max allowed for limit orders |
| 422 | Quantity for market variant orders should be less than X | Total quantity exceeds `max_market_order_quantity` |
| 422 | Quantity should be greater than Y | Quantity is below `min_quantity` |
| 422 | Price can't be empty for limit_order | `price` was null on a limit order |
| 422 | Liquidation will be triggered instantly | Order would immediately liquidate the position |
| 400 | Price is out of permissible range | price > `max_price` or < `min_price` for the instrument |
| 400 | Please enter a value lower than X | Limit price exceeds max (LTP × (1 + multiplier_up/100)) |
| 400 | Please enter a value higher than X | Limit price is below min (LTP × (1 − multiplier_down/100)) |
| 400 | Price should be divisible by 0.01 | Price isn't a multiple of `price_increment` |
| 400 | Insufficient funds | Not enough wallet balance |
| 400 | Minimum order value should be X USDT | Order value below `min_notional` |
| 400 | Instrument is in exit-only mode | `exit_only = true` — new positions blocked |
| 400 | You've exceeded the max allowed position of X USDT | Current position exceeds position size threshold |
| 400 | Order is exceeding the max allowed position of X USDT | Position + order value > position size threshold |
| 400 | Trigger price should be greater than the current price | Buy stop order: trigger < LTP |
| 400 | Trigger price should be less than the current price | Sell stop order: trigger > LTP |
| 400 | Limit price should be greater than the trigger price | Buy stop limit: limit price < trigger price |
| 400 | Limit price should be less than the trigger price | Sell stop limit: limit price > trigger price |
| 500 | Invalid input | General invalid input error |

---

### Cancel Order
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/orders/cancel
```
Body: `{ "timestamp": ..., "id": "order-uuid" }`

---

### Cancel All Open Orders (Global)
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/positions/cancel_all_open_orders
```
Body: `{ "timestamp": ..., "margin_currency_short_name": ["USDT"] }`

---

### Cancel All Open Orders for Position
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/positions/cancel_all_open_orders_for_position
```
Body: `{ "timestamp": ..., "id": "position-uuid" }` (position id, not order id)

---

### Edit Order
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/orders/edit
```
**Note: Edit order is only supported on USDT-margined Futures.**

Body: `{ "timestamp": ..., "id": "order-uuid", "price": 2100.0, "total_quantity": 0.05, "take_profit_price": 2200.0, "stop_loss_price": 2000.0 }`

---

## 3. Position Endpoints

### Get Positions
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/positions
```

This endpoint serves two purposes depending on the body params passed:

**A) List all positions (paginated):**
```json
{ "timestamp": ..., "page": "1", "size": "10", "margin_currency_short_name": ["USDT"] }
```

**B) Filter by specific pairs or position IDs:**
```json
{
  "timestamp": ...,
  "page": "1",
  "size": "10",
  "pairs": "B-BTC_USDT,B-ETH_USDT",
  "margin_currency_short_name": ["USDT"]
}
```
Use either `pairs` OR `position_ids` (comma-separated string). Not both.

**Key response fields per position:**

> **Note:** All margin values (`locked_margin`, `locked_user_margin`, `locked_order_margin`, `maintenance_margin`) are in USDT even for INR-margined futures.

| Field | Description |
|-------|-------------|
| `id` | Position UUID (stable per pair) |
| `pair` | e.g. `B-BTC_USDT` |
| `active_pos` | Quantity held. Positive = long, negative = short. |
| `inactive_pos_buy` | Pending buy order quantities |
| `inactive_pos_sell` | Pending sell order quantities |
| `avg_price` | Average entry price |
| `liquidation_price` | Liquidation price (isolated margin only; ignore for cross) |
| `locked_margin` | Margin in position after fees and funding |
| `locked_user_margin` | Initially invested margin excluding fees/funding |
| `locked_order_margin` | Margin locked in open orders |
| `take_profit_trigger` / `stop_loss_trigger` | Full-position TP/SL triggers |
| `leverage` | Current leverage |
| `maintenance_margin` | Margin required to avoid liquidation |
| `mark_price` | Mark price at last update (not real-time) |
| `margin_type` | `crossed` or `isolated` (NULL = isolated) |
| `settlement_currency_avg_price` | Average USDT↔INR conversion price for the position (INR futures only) |
| `margin_currency_short_name` | `USDT` or `INR` |
| `updated_at` | Last update EPOCH ms — triggered by trade, funding, margin change, or TP/SL update |

---

### Update Leverage
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/positions/update_leverage
```
Body: `{ "timestamp": ..., "leverage": "5", "pair": "B-LTC_USDT", "margin_currency_short_name": "USDT" }`

Use either `pair` or `id` (position id). **Set leverage before placing orders** to avoid rejections.

Error codes: leverage < 1x, exceeds tiered max, insufficient funds, instant liquidation triggered.

---

### Add Margin
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/positions/add_margin
```
Body: `{ "timestamp": ..., "id": "position-uuid", "amount": 10 }`

Amount in USDT (USDT futures) or INR (INR futures). Makes position safer (improves liquidation price).

---

### Remove Margin
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/positions/remove_margin
```
Body: `{ "timestamp": ..., "id": "position-uuid", "amount": 10 }`

Increases liquidation risk. Errors: exit/liquidation in progress, inactive position, insufficient margin, instant liquidation.

---

### Change Position Margin Type
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/positions/margin_type
```
**Note: Cross margin is only supported on USDT-margined Futures. Can only change when no active position or open orders exist for the pair.**

Body:
```json
{
  "timestamp": ...,
  "pair": "B-JTO_USDT",
  "margin_type": "isolated"
}
```

| Field | Required | Values |
|-------|----------|--------|
| `pair` | YES | e.g. `B-JTO_USDT` |
| `margin_type` | YES | `isolated` or `crossed` |

Returns the updated position object (same fields as the position response).

---

### Get Cross Margin Details (Auth required)
```
GET https://api.coindcx.com/exchange/v1/derivatives/futures/positions/cross_margin_details
```
**Note: Cross margin is not supported on INR-margined Futures.**

Body: `{ "timestamp": ... }`

| Response Field | Description |
|----------------|-------------|
| `pnl` | Unrealised PnL across all cross margin positions |
| `maintenance_margin` | Cumulative maintenance margin of all cross margin positions |
| `total_wallet_balance` | Total wallet balance excluding PnL, funding, and fees of active positions |
| `total_initial_margin` | Cumulative initial margin for cross + isolated positions and orders |
| `total_initial_margin_isolated` | Initial margin for isolated positions and orders only |
| `total_initial_margin_crossed` | Initial margin for cross positions only (excluding orders) |
| `total_open_order_initial_margin_crossed` | Initial margin locked in open cross margin orders |
| `available_balance_cross` | Balance available for cross margin trading |
| `available_balance_isolated` | Balance available for isolated margin trading |
| `margin_ratio_cross` | Cross margin ratio — position liquidated when ≥ 1 |
| `withdrawable_balance` | Balance that can be withdrawn to spot wallet |
| `total_account_equity` | `total_wallet_balance` + `pnl` |

---

### Quick Exit Position
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/positions/exit
```
Body: `{ "timestamp": ..., "id": "position-uuid" }`

Closes entire position immediately at market. Large positions may be split (same `group_id`).

---

### Create TP/SL Orders for Position
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/positions/create_tpsl
```
Body:
```json
{
  "timestamp": ...,
  "id": "position-uuid",
  "take_profit": {
    "stop_price": "1.0",
    "limit_price": "0.9",
    "order_type": "take_profit_market"
  },
  "stop_loss": {
    "stop_price": "0.271",
    "limit_price": "0.270",
    "order_type": "stop_market"
  }
}
```
Currently only `take_profit_market` and `stop_market` are supported for full-position TP/SL. The `limit_price` field exists in the request schema but is **not supported** — ignore it.
Response includes separate `take_profit` and `stop_loss` objects. `success: false` + `error` if creation failed (e.g. "TP already exists").

---

### Get Transactions (Position PnL History)
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/positions/transactions
```
Body: `{ "timestamp": ..., "stage": "all", "page": "1", "size": "10" }`

Stage values: `all`, `default` (regular orders), `funding`, `exit`, `tpsl_exit`, `liquidation`.

> **Note:** `amount`, `fee_amount`, and `settlement_amount` are in INR for INR-margined futures; USDT otherwise.

| Field | Description |
|-------|-------------|
| `pair` | Instrument pair |
| `stage` | Transaction stage (default, funding, exit, tpsl_exit, liquidation) |
| `amount` | PnL from this transaction |
| `fee_amount` | Fee charged for this transaction (per trade of an order) |
| `price_in_inr` | Trade price in INR |
| `price_in_btc` | Trade price in BTC |
| `price_in_usdt` | Trade price in USDT |
| `source` | `user` for user-placed orders; `system` for system-placed orders (e.g. liquidations) |
| `parent_type` | Order type reference (e.g. `Derivatives::Futures::Order`) |
| `parent_id` | Order UUID that generated this transaction |
| `position_id` | Position UUID |
| `settlement_amount` | Ignore this |
| `margin_currency_short_name` | `USDT` or `INR` |
| `created_at` / `updated_at` | Timestamps (EPOCH ms) |

---

## 4. Wallet & History

### Get Wallet Details
```
GET https://api.coindcx.com/exchange/v1/derivatives/futures/wallets
```
Body: `{ "timestamp": ... }`

Returns both INR & USDT futures wallet details.

| Field | Description |
|-------|-------------|
| `id` | Futures wallet id |
| `currency_short_name` | `USDT` or `INR` |
| `balance` | Ignore this |
| `locked_balance` | Total initial margin locked in isolated orders and positions |
| `cross_order_margin` | Total initial margin locked in cross margin orders |
| `cross_user_margin` | Total initial margin locked in cross margin positions |

> **Total wallet balance** = `balance` + `locked_balance`

---

### Wallet Transfer (Spot ↔ Futures)
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/wallets/transfer
```

Body:
```json
{
  "timestamp": ...,
  "transfer_type": "withdraw",
  "amount": 10,
  "currency_short_name": "USDT"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `transfer_type` | YES | `deposit` (spot → futures) or `withdraw` (futures → spot) |
| `amount` | YES | Amount in the currency's units |
| `currency_short_name` | YES | `USDT` or `INR` |

Response: same wallet object as Wallet Details above.

---

### Wallet Transactions
```
GET https://api.coindcx.com/exchange/v1/derivatives/futures/wallets/transactions?page=1&size=1000
```
Body: `{ "timestamp": ... }`

| Field | Description |
|-------|-------------|
| `derivatives_futures_wallet_id` | Futures wallet id |
| `transaction_type` | `credit` (into futures) or `debit` (from futures) |
| `amount` | Transaction amount |
| `currency_short_name` / `currency_full_name` | Currency |
| `reason` | `by_universal_wallet` (spot↔futures transfer), `by_futures_order` (order trade), `by_futures_funding` (cross margin funding) |
| `created_at` | EPOCH ms |

---

### Get Trades History (Private)
```
POST https://api.coindcx.com/exchange/v1/derivatives/futures/trades
```

Body:
```json
{
  "timestamp": ...,
  "pair": "B-ID_USDT",
  "order_id": "9b37c924-...",
  "from_date": "2024-01-01",
  "to_date": "2024-01-22",
  "page": "1",
  "size": "10",
  "margin_currency_short_name": ["USDT"]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `pair` | YES | Instrument pair |
| `order_id` | OPTIONAL | Filter by specific order |
| `from_date` | YES | Format: `YYYY-MM-DD` |
| `to_date` | YES | Format: `YYYY-MM-DD` |
| `margin_currency_short_name` | YES | `["USDT"]` or `["INR"]` |

Response fields per trade: `price`, `quantity`, `is_maker`, `fee_amount`, `pair`, `side`, `timestamp`, `order_id`, `settlement_currency_conversion_price`, `margin_currency_short_name`.
Note: `fee_amount` is in USDT for INR futures.

---

## 5. WebSocket — Full Details

### Connection Setup (Python)
```python
import socketio, hmac, hashlib, json, asyncio
from datetime import datetime

socketEndpoint = 'wss://stream.coindcx.com'
sio = socketio.AsyncClient()

key = "YOUR_API_KEY"
secret = "YOUR_SECRET"
secret_bytes = bytes(secret, encoding='utf-8')

# Auth signature for private channel
body = {"channel": "coindcx"}
json_body = json.dumps(body, separators=(',', ':'))
signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

async def ping_task():
    while True:
        await asyncio.sleep(25)
        await sio.emit('ping', {'data': 'Ping message'})

@sio.event
async def connect():
    print("Connected!")
    # Join private channel
    await sio.emit('join', {'channelName': 'coindcx', 'authSignature': signature, 'apiKey': key})
    # Join public channels
    await sio.emit('join', {'channelName': 'B-BTC_USDT@trades-futures'})

async def main():
    await sio.connect(socketEndpoint, transports='websocket')
    asyncio.create_task(ping_task())
    await sio.wait()

asyncio.run(main())
```

### All WebSocket Channels & Events

| Channel Name | Event | Payload Fields |
|---|---|---|
| `B-{pair}@trades-futures` | `new-trade` | `T` (timestamp), `RT`, `p` (price), `q` (qty), `m` (is_maker bool), `s` (pair), `pr` (`f`) |
| `B-{pair}@prices-futures` | `price-change` | `T`, `p` (LTP), `pr` (`f`) |
| `B-{pair}@orderbook@{depth}-futures` | `depth-snapshot` | `ts`, `vs` (version), `asks` `{price:qty}`, `bids` `{price:qty}`, `pr` |
| `B-{pair}_{interval}-futures` | `candlestick` | `data[]` (OHLCV + pair + duration), `Ets`, `i`, `channel`, `pr` |
| `currentPrices@futures@rt` | `currentPrices@futures#update` | `vs`, `ts`, `pr`, `pST`, `prices: {pair: {mp, bmST, cmRT}}` |
| `coindcx` (private) | `df-order-update` | Full order object (same as REST order fields) |
| `coindcx` (private) | `df-position-update` | Full position object (same as REST position fields, includes `margin_currency_short_name`, `settlement_currency_avg_price`) |
| `coindcx` (private) | `balance-update` | `id`, `balance`, `locked_balance`, `currency_id`, `currency_short_name` |

**Candlestick intervals:** `1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `8h`, `1d`, `3d`, `1w`, `1M`

**Order book depth options:** `10`, `20`, `50`

---

## 6. Glossary / Field Abbreviations

| Abbreviation | Meaning |
|---|---|
| `e` | Event type |
| `p` | Price (LTP — Last Traded Price) |
| `q` | Quantity (trade quantity) |
| `pr` | Product (`f` = futures, `s` = spot) |
| `T` | Timestamp |
| `m` | Is maker (boolean: true = maker, false = taker) |
| `RT` | Range timestamp |
| `ts` | Timestamp |
| `vs` | Version |
| `Ets` | Event timestamp from TPE (candlestick data) |
| `i` | Interval |
| `E` | Event timestamp (order book data) |
| `pST` | Price sent time |
| `v` | 24h volume |
| `ls` | Last price |
| `pc` | Price change percent |
| `btST` | TPE tick send time |
| `mp` | Mark price |
| `bmST` | TPE mark price send time |
| `LTP` | Last Traded Price |
| `TP` | Take Profit |
| `SL` | Stop Loss |
| `TIF` | Time In Force |
# Tron Address Info API

A FastAPI service that retrieves and stores information about Tron blockchain addresses.

## Features

- Retrieve address information (balance, bandwidth, energy) from Tron network
- Store request history in PostgreSQL database
- Paginated request history access
- Supports both Shasta testnet and Tron mainnet

## Requirements

- Python 3.8+
- PostgreSQL
- TronGrid API key (optional)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tron-address-api.git
   cd tron-address-api
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   python init_db.py
   uvicorn app.main:app --reload
   test by using test_tron_api.py file or by http://127.0.0.1:8000/docs
   

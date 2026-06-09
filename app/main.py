from app.etl.extract import download_market_data, TICKERS
from app.etl.transform import prepare_data
from app.etl.load import save_to_postgres


def main():
    raw_data = download_market_data(TICKERS)
    clean_data = prepare_data(raw_data, TICKERS)
    save_to_postgres(clean_data)


if __name__ == "__main__":
    main()
from bot import start_client
from db_setup import create_tables

def main():
    create_tables()
    start_client()


if __name__ == "__main__":
    main()
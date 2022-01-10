from bot import start_client
from db_setup import create_tables

def main():
    start_client()
    create_tables()


if __name__ == "__main__":
    main()
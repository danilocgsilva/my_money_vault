from start_server_src.build_database_with_data import build_database_with_data
from start_server_src.build_database_with_data import check_database_exists

if not check_database_exists():
    build_database_with_data()

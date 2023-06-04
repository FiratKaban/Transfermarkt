# -*- coding: utf-8 -*-
""".
Created on Mon Jun 05 02:19 2023
...
@author: FIRATKABAN
@contributer: cerebnismus
"""

import psycopg2

def create_tables(cur, conn):
    """
    This function creates the necessary tables in the database.
    """
    # Create a cursor object
    cur = conn.cursor()

    # Create leagues table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leagues (
            league_name TEXT,
            league_country TEXT,
            league_clubs TEXT,
            league_players TEXT,
            league_avg_age TEXT,
            league_foreigners TEXT,
            league_total_market_value TEXT
        );
    """)

    # Create teams table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            team_name TEXT,
            team_country TEXT,
            team_league_id INTEGER
        );
    """)

    # Create players table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            player_name TEXT,
            player_age TEXT,
            player_nationality TEXT,
            player_team_id INTEGER
        );
    """)

    # Commit the changes to the database
    conn.commit()

    # Close the cursor
    cur.close()


def database_connection():
    """.
    This function connects to the database.
    """
    conn = psycopg2.connect(
        host="44.204.235.127",
        database="postgres",
        user="postgres",
        password="myPassword",
    )

    cur = conn.cursor()
    cur.execute("SELECT version();")
    # cur.execute('DELETE FROM public.test_table')
    # conn.commit()
    # cur.close()
    # conn.close()
    record = cur.fetchone()
    print("You are connected to - ", record, "\n")
    return cur, conn


def main():
    """
    This is the main function that controls the flow of the program.
    """
    # Connect to the database
    cur, conn = database_connection()
    # Create tables if they don't exist
    create_tables(cur, conn)

    # Close the database connection
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()

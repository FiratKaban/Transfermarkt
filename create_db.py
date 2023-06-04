# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 13:24 2022
Updated on Sun Feb 26 12:13 2023
Updated on Wed May 31 13:29 2023
Updated on Mon Jun 05 01:29 2023
...
@author: FIRATKABAN
@contributer: cerebnismus
"""

from datetime import datetime
import psycopg2
import requests
from bs4 import BeautifulSoup
from parsel import Selector

def create_tables(cur):
    """
    This function creates the necessary tables in the database.
    """
    # Create leagues table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leagues (
            league_id SERIAL PRIMARY KEY,
            league_name VARCHAR(255),
            league_country VARCHAR(255),
            league_clubs INTEGER,
            league_players INTEGER,
            league_avg_age FLOAT,
            league_foreigners FLOAT,
            league_total_market_value VARCHAR(255)
        );
    """)

    # Create teams table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            team_id SERIAL PRIMARY KEY,
            team_name VARCHAR(255),
            team_country VARCHAR(255),
            team_league_id INTEGER,
            FOREIGN KEY (team_league_id) REFERENCES leagues (league_id)
        );
    """)

    # Create players table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            player_id SERIAL PRIMARY KEY,
            player_name VARCHAR(255),
            player_age INTEGER,
            player_nationality VARCHAR(255),
            player_team_id INTEGER,
            FOREIGN KEY (player_team_id) REFERENCES teams (team_id)
        );
    """)
    
def create_tables(cur):
    """
    This function creates the necessary tables in the database.
    """
    # Create leagues table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leagues (
            league_id SERIAL PRIMARY KEY,
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
            team_id SERIAL PRIMARY KEY,
            team_name TEXT,
            team_country TEXT,
            team_league_id INTEGER,
            FOREIGN KEY (team_league_id) REFERENCES leagues (league_id)
        );
    """)

    # Create players table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            player_id SERIAL PRIMARY KEY,
            player_name TEXT,
            player_age TEXT,
            player_nationality TEXT,
            player_team_id INTEGER,
            FOREIGN KEY (player_team_id) REFERENCES teams (team_id)
        );
    """)



def insert_league(cur, conn, league_data):
    """
    This function inserts league data into the database.
    """
    cur.execute("""
        INSERT INTO leagues (
            league_name,
            league_country,
            league_clubs,
            league_players,
            league_avg_age,
            league_foreigners,
            league_total_market_value
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING league_id;
    """, league_data)
    league_id = cur.fetchone()[0]
    conn.commit()
    return league_id

def insert_team(cur, conn, team_data, league_id):
    """
    This function inserts team data into the database.
    """
    cur.execute("""
        INSERT INTO teams (
            team_name,
            team_country,
            team_league_id
        )
        VALUES (%s, %s, %s)
        RETURNING team_id;
    """, (*team_data, league_id))
    team_id = cur.fetchone()[0]
    conn.commit()
    return team_id

def insert_player(cur, conn, player_data, team_id):
    """
    This function inserts player data into the database.
    """
    cur.execute("""
        INSERT INTO players (
            player_name,
            player_age,
            player_nationality,
            player_team_id
        )
        VALUES (%s, %s, %s, %s)
        RETURNING player_id;
    """, (*player_data, team_id))
    player_id = cur.fetchone()[0]
    conn.commit()
    return player_id

def database_connection():
    """
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
    print(f"Connected to: {cur.fetchone()[0]}")

    return conn, cur






def main():
    """
    This is the main function that controls the flow of the program.
    """

    # Connect to the database
    conn, cur = database_connection()
    # Create tables if they don't exist
    create_tables(cur)

    

    
    # Insert league data into the database
    league_id = insert_league(cur, conn, league_data)
    # Extract teams data
    teams_data = get_teams_data(selector)
    # Insert teams data into the database
    for team_data in teams_data:
        team_id = insert_team(cur, conn, team_data, league_id)
        # Extract players data for each team

        
        # Insert players data into the database
        insert_player(cur, conn, player_data, team_id)


if __name__ == "__main__":
    main()

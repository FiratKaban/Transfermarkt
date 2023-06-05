def insert_leagues(cur, conn, league_url, league_name, league_country, league_clubs, league_players, league_avg_age, league_foreigners, league_total_market_value):
    """
    This function inserts league data into the database.
    """
    cur.execute("""
        INSERT INTO leagues (
            league_url,
            league_name,
            league_country,
            league_clubs,
            league_players,
            league_avg_age,
            league_foreigners,
            league_total_market_value
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, league_url, league_name, league_country, league_clubs, league_players, league_avg_age, league_foreigners, league_total_market_value)
    conn.commit()

def insert_leagues_data(cur, conn, league_data):
    """
    This function inserts season data into the database.
    """
    cur.execute("""
        INSERT INTO leagues_data (
            league_url,
            league_href,
            league_country_name,
            league_reigning_champion,
            league_record_holding_champion,
            league_record_holding_champion_value,
            league_uefa_coefficient,
            league_uefa_coefficient_value,
            league_num_of_clubs,
            league_num_of_players,
            league_num_of_foreigners,
            league_market_value,
            league_avg_market_value,
            league_most_player_valuable
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, league_data)
    conn.commit()

def insert_teams(cur, conn, team):
    """
    This function inserts team data into the database.
    """
    cur.execute("""
        INSERT INTO teams (
            team,
            team_link,
            team_href,
            squad,
            team_avg_age,
            team_foreigners,
            t_avg_market_value,
            t_ttl_market_value
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, team)
    conn.commit()

def insert_teams_data(cur, conn, team_data):
    """
    This function inserts team data into the database.
    """
    cur.execute("""
        INSERT INTO teams_data (
            league,
            team_country,
            team_href,
            league_level,
            teams_position,
            in_league_since,
            teams_foreigner_players_percant,
            teams_stadium_name,
            teams_stadium_seats,
            teams_transfer_record
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, team_data)
    conn.commit()

def insert_players(cur, conn, player):
    """
    This function inserts team data into the database.
    """
    cur.execute("""
        INSERT INTO players (
            shirt_number,
            player,
            playerlink,
            playerhref,
            mainposition,
            dateofbirth,
            birthday,
            birthmonth,
            birthyear
            age,
            nat1,
            nat2,
            height,
            foot,
            joined,
            joined_day,
            joined_month
            joined_year,
            previousteam,
            contractdate,
            contractday,
            contractmonth,
            contractyear,
            marketvalue
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s);
    """, player)
    conn.commit()

def insert_players_data(cur, conn, player_data):
    """
    This function inserts player data into the database.
    """
    cur.execute("""
        INSERT INTO players_data (
            player_href,
            place_of_birth,
            foot,
            player_agent,
            player_agent_url,
            expires,
            player_outfitter,
            twitter,
            facebook,
            instagram
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, player_data)
    conn.commit()

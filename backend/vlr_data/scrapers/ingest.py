from django.utils import timezone
import re

from ..models import Event, Map, Match, Player, PlayerStats, Team


def get_team_id_from_url(url: str) -> str:
    """Gets the team's VLR ID from it's URL

    Args:
        url (str): URL for the team's VLR page

    Raises:
        ValueError: if the URL is not in the expected format

    Returns:
        str: the team's VLR ID
    """
    match = re.search(r"/team/(\d+)/", url)
    if not match:
        raise ValueError(f"Could not extract team ID from URL: {url}")
    return match.group(1)


def get_match_id_from_url(url: str) -> str:
    """Gets the match's VLR ID from it's URL

    Args:
        url (str): URL for the match's VLR page

    Raises:
        ValueError: if the URL is not in the expected format

    Returns:
        str: the match's VLR ID
    """
    match = re.search(r"/(\d+)/", url)
    if not match:
        raise ValueError(f"Could not extract match ID from URL: {url}")
    return match.group(1)


def get_player_id_from_url(url: str) -> str:
    """Gets the player's VLR ID from it's URL

    Args:
        url (str): URL for the player's VLR page

    Raises:
        ValueError: if the URL is not in the expected format

    Returns:
        str: the player's VLR ID
    """
    match = re.search(r"/player/(\d+)/", url)
    if not match:
        raise ValueError(f"Could not extract player ID from URL: {url}")
    return match.group(1)


def ingest_team(team_data: dict, team_url: str):
    """Ingests the team data and stores it in the database

    Args:
        team_data (dict): Parsed data about the team, should include keys:
                            - "team_name": str - full name of the team
                            - "team_tag": str - shortened name for the team
                            - "team_rating": int - VLR team rating
                            - "player": List[dict] - List of active player info with keys:
                                - "real_name": str - player's real name
                                - "ign": str - player's in game name
        team_url (str): URL for the team's VLR page
    """
    try:
        team_id = get_team_id_from_url(team_url)

        team, _ = Team.objects.update_or_create(
            vlr_id=team_id,
            defaults={
                "name": team_data["team_name"],
                "team_tag": team_data["team_tag"],
                "team_rating": team_data["team_rating"],
                "last_updated": timezone.now(),
            },
        )

        for player in team_data["players"]:
            player_id = get_player_id_from_url(player["url"])

            player, _ = Player.objects.update_or_create(
                vlr_id=player_id,
                defaults={
                    "real_name": player["real_name"],
                    "ign": player["ign"],
                    "team": team,
                    "last_updated": timezone.now(),
                },
            )

    except Exception as e:
        print(f"Error while ingesting team data: {e}")


def ingest_player(player_data: dict, player_url: str):
    """Ingests the player data and stores it in the database

    Args:
        player_data (dict): Parsed data about the player, should include keys:
                            - "real_name": str - player's real name
                            - "ign": str - player's in game name
                            - "team": str - URL of the VLR page of the team the player belongs to
        player_url (str): URL for the player's VLR page

    Raises:
        ValueError: If the team specified in the player data does not yet exist in the database
    """

    try:
        player_id = get_player_id_from_url(player_url)
        team_id = get_team_id_from_url(player_data["team"])

        team = Team.objects.get(vlr_id=team_id)

        _, _ = Player.objects.update_or_create(
            vlr_id=player_id,
            defaults={
                "real_name": player_data["real_name"],
                "ign": player_data["ign"],
                "team": team,
                "last_updated": timezone.now(),
            },
        )
    except Team.DoesNotExist:
        raise ValueError(
            f"Team with ID {team_id} must be created before ingesting players in the team."
        )
    except Exception as e:
        print(f"Error while ingesting player data: {e}")


def ingest_event(event_data: dict):
    """Ingests the event data and stores it in the database

    Args:
        event_data (dict): Parsed data about the event, should include keys:
                            - "name": str,                # the name of the event
                            - "stages": List[str]         # names of the stages in the event
                            - "stages_url": List[str]     # URL of the stages in the event
    """
    try:
        for i, stage_url in enumerate(event_data["stages_url"]):
            _, _ = Event.objects.update_or_create(
                vlr_url=stage_url,
                defaults={
                    "name": event_data["name"],
                    "series": event_data["stages"][i],
                },
            )
    except Exception as e:
        print(f"Error while ingesting event data: {e}")


def ingest_match(match_data: dict, match_url: str):
    """Ingests the match data and stores it in the database

    Args:
        match_data (dict): Parsed data about the match, should include keys:
                        If the match is not finished:
                            - "event": str,               # URL of the event's VLR page
                            - "date": datetime,           # Match start time in UTC
                            - "team_1": str,              # URL of the first team's VLR page
                            - "team_2": str,              # URL of the second team's VLR page
                            - "finished": bool,           # whether the match is finished
                        If the match is finished:
                            - "event": str,               # URL of the event's VLR page
                            - "date": datetime,           # Match start time in UTC
                            - "team_1": str,              # URL of the first team's VLR page
                            - "team_2": str,              # URL of the second team's VLR page
                            - "finished": bool,           # whether the match is finished
                            - "team_1_match_score": int,  # maps won by the first team
                            - "team_2_match_score": int,  # maps won by the second team
                            - "maps_played": int,         # number of maps played
                            - "maps": List[dict]          # stats for each map
                        Where each maps dict should contain the keys:
                            - "team_1_score": int,        # rounds won in this map by the first team
                            - "team_2_score": int,        # rounds won in this map by the second team
                            - "map_played": str,          # which map was played
                            - "game_id": str,             # VLR game id for this map
                            - "team_1_stats": List[dict]  # the stats for the first team (5 players)
                            - "team_2_stats": List[dict]  # the stats for the the second team (5 players)
                        Where each team_x_stats dict should contain the keys:
                            - "player": str,              # URL of the player's VLR page
                            - "kills": int,               # number of kills the player got
                            - "deaths": int,              # number of times the player died
                            - "assists": int,             # number of assists the player got
                            - "agent_played": str,        # the agent the player played
                            - "acs": int,                 # player's acs for this map
        match_url (str): URL for the match's VLR page

    Raises:
        ValueError: If the event the match is part of does not yet exist in the database
        ValueError: If the teams who are playing in the match does not yet exist in the database
        ValueError: If the player whose stats is trying to be created does not yet exist in the database
    """
    try:
        event_url = match_data["event"]
        event = Event.objects.get(vlr_url=event_url)

        team_1_id = get_team_id_from_url(match_data["team_1"])
        team_2_id = get_team_id_from_url(match_data["team_2"])

        team_1 = Team.objects.get(vlr_id=team_1_id)
        team_2 = Team.objects.get(vlr_id=team_2_id)

        date_played = match_data["date"]
        match_id = get_match_id_from_url(match_url)

        is_finished = match_data["finished"]
        if not is_finished:
            _, _ = Match.objects.update_or_create(
                vlr_id=match_id,
                defaults={
                    "event": event,
                    "team1": team_1,
                    "team2": team_2,
                    "date_played": date_played,
                    "is_finished": is_finished,
                    "team1_score": 0,
                    "team2_score": 0,
                },
            )
            return

        team_1_score = match_data["team_1_match_score"]
        team_2_score = match_data["team_2_match_score"]

        match, _ = Match.objects.update_or_create(
            vlr_id=match_id,
            defaults={
                "event": event,
                "team1": team_1,
                "team2": team_2,
                "date_played": date_played,
                "is_finished": is_finished,
                "team1_score": team_1_score,
                "team2_score": team_2_score,
            },
        )
        
        maps = match_data["maps"]
        for i in range(match_data["maps_played"]):
            map_data = maps[i]
            team1_map_score = map_data["team_1_score"]
            team2_map_score = map_data["team_2_score"]
            map_played = map_data["map_played"]
            game_id = map_data["game_id"]
            map, _ = Map.objects.update_or_create(
                game_id=game_id,
                defaults={
                    "match": match,
                    "name": map_played,
                    "map_number": i + 1,
                    "team1_score": team1_map_score,
                    "team2_score": team2_map_score,
                },
            )

            team_1_stats = map_data["team_1_stats"]
            team_2_stats = map_data["team_2_stats"]

            for player_stat in team_1_stats + team_2_stats:
                player_id = get_player_id_from_url(player_stat["player"])
                kills = player_stat["kills"]
                deaths = player_stat["deaths"]
                assists = player_stat["assists"]
                acs = player_stat["acs"]
                agent_played = player_stat["agent_played"]

                player = Player.objects.get(vlr_id=player_id)

                _, _ = PlayerStats.objects.get_or_create(
                    player=player,
                    map=map,
                    defaults={
                        "kills": kills,
                        "deaths": deaths,
                        "assists": assists,
                        "acs": acs,
                        "agent": agent_played,
                    },
                )

    except Event.DoesNotExist:
        raise ValueError(
            f'Event with URL: "{event_url}" must be created before ingesting matches in the event.'
        )

    except Team.DoesNotExist:
        raise ValueError(
            f"Team with IDs: {team_1_id}, {team_2_id} must be created before ingesting teams in this match."
        )

    except Player.DoesNotExist:
        raise ValueError(
            f"Players must be created before ingesting players' stats in this match."
        )

    except Exception as e:
        print(f"Error while ingesting match data: {e}")

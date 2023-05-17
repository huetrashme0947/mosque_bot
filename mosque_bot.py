# Mosque Bot for TS3 v1.0.0
# (c) 2023 HUE_TrashMe
# https://github.com/huetrashme0947/mosque_bot
# mosque_bot.py
# TeamSpeak 3 bot for moving users to a specific channel at prayer times


import ts3
import requests
import configparser
import time
import json
from datetime import datetime


def move_everyone_to_masjid(conn, channel_id, message, config):
	excluded_servergroups = None
	excluded_clients = None
	excluded_channels = None

	# Servergroup based filtering
	if config["ExcludeClients"]["ServerGroups"] != "no":
		excluded_servergroups = json.loads(config["ExcludeClients"]["ServerGroups"])
	# Client based filtering
	if config["ExcludeClients"]["Clients"] != "no":
		excluded_clients = json.loads(config["ExcludeClients"]["Clients"])
	# Channel based filtering
	if config["ExcludeClients"]["Channels"] != "no":
		excluded_channels = json.loads(config["ExcludeClients"]["Channels"])

	# Get all currently online clients, filter and move every one to mosque channel
	clients_online = conn.clientlist(away=True, groups=True, uid=True)
	for client in clients_online.parsed:
		# Servergroup based filtering
		if excluded_servergroups != None and int(client["client_servergroups"]) in excluded_servergroups:
			continue
		# Client based filtering
		if excluded_clients != None and client["client_unique_identifier"] in excluded_clients:
			continue
		# Channel based filtering
		if excluded_channels != None and int(client["cid"]) in excluded_channels:
			continue
		# Away status based filtering
		if config["ExcludeClients"]["AwayClients"] == "yes" and client["client_away"] == "1":
			continue
		# Temporary channel based filtering
		if config["ExcludeClients"]["InTemporaryChannel"] == "yes" and conn.channelinfo(cid=client["cid"]).parsed[0]["channel_flag_permanent"] == "0":
			continue

		try:
			conn.clientmove(cid=channel_id, clid=client["clid"])

			# If Client.PokeOnMove == "yes", poke instead of sending of text message
			if config["Client"]["PokeOnMove"] == "yes":
				conn.clientpoke(msg=message, clid=client["clid"])
			else:
				conn.sendtextmessage(targetmode=1, target=client["clid"], msg=message)
		except Exception as err:
			continue


def masjid_bot(conn, config):
	# Update client data
	print("Starting bot with display name '%s'..." % config["Client"]["Name"], end="")
	conn.clientupdate(client_nickname=config["Client"]["Name"])
	print(" done")

	while True:
		# get today's prayer times for Berlin
		print("Retrieving prayer times for %s, %s..." % (config["PrayerTimes"]["City"], config["PrayerTimes"]["Country"]), end="")
		prayer_times = requests.get("https://api.aladhan.com/v1/timingsByCity?city=%s&country=%s" % (config["PrayerTimes"]["City"], config["PrayerTimes"]["Country"])).json()["data"]["timings"]
		print(" done")
		print("Waiting for prayer times...")

		while True:
			# get current time
			curr_time = datetime.now().strftime("%H:%M")

			# using if statements because python is a dumbass language which's switch case implementation refuses to work properly with dicts
			if curr_time == prayer_times["Sunrise"]:
				print("Fajr time alhamdulillah! Moving clients to mosque...", end="")
				move_everyone_to_masjid(conn, config["MoveToMosque"]["FajrChannel"], config["MoveMessages"]["FajrMessage"], config);
				print(" done")
				break
			elif curr_time == prayer_times["Dhuhr"]:
				print("Dhuhr time alhamdulillah! Moving clients to mosque...", end="")
				move_everyone_to_masjid(conn, config["MoveToMosque"]["DhuhrChannel"], config["MoveMessages"]["DhuhrMessage"], config);
				print(" done")
				break
			elif curr_time == prayer_times["Asr"]:
				print("Asr time alhamdulillah! Moving clients to mosque...", end="")
				move_everyone_to_masjid(conn, config["MoveToMosque"]["AsrChannel"], config["MoveMessages"]["AsrMessage"], config);
				print(" done")
				break
			elif curr_time == prayer_times["Maghrib"]:
				print("Maghrib time alhamdulillah! Moving clients to mosque...", end="")
				move_everyone_to_masjid(conn, config["MoveToMosque"]["MaghribChannel"], config["MoveMessages"]["MaghribMessage"], config);
				print(" done")
				break
			elif curr_time == prayer_times["Isha"]:
				print("Isha time alhamdulillah! Moving clients to mosque...", end="")
				move_everyone_to_masjid(conn, config["MoveToMosque"]["IshaChannel"], config["MoveMessages"]["IshaMessage"], config);
				print(" done")
				break
			elif True:
				print("Isha time alhamdulillah! Moving clients to mosque...", end="")
				move_everyone_to_masjid(conn, config["MoveToMosque"]["IshaChannel"], config["MoveMessages"]["IshaMessage"], config);
				print(" done")
				break
			else:
				time.sleep(60)
				conn.send_keepalive()

		time.sleep(60)
		conn.send_keepalive()

def main():
	print("Mosque Bot for TS3 v1.0.0\n(c) 2023 HUE_TrashMe")

	# Read mosque_bot.ini
	print("Parsing mosque_bot.ini...", end="")
	config = configparser.ConfigParser()
	config.read("mosque_bot.ini")
	print(" done")

	# Connect to TS3 serverquery and start bot
	print("Connecting to ServerQuery on %s:%s as %s..." % (config["ServerQuery"]["Host"], config["ServerQuery"]["Port"], config["ServerQuery"]["Username"]), end="")
	try:
		with ts3.query.TS3Connection(config["ServerQuery"]["Host"], config["ServerQuery"]["Port"]) as conn:
			conn.login(client_login_name=config["ServerQuery"]["Username"], client_login_password=config["ServerQuery"]["Password"])
			conn.use(sid=config["ServerQuery"]["VirtualServer"])
			print(" done")
			masjid_bot(conn, config)
	except Exception as err:
		print(" failed")
		raise err

if __name__ == "__main__":
	main()
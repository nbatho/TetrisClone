import socket
from _thread import *
import pickle

server = "0.0.0.0"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(5 )
print("Waiting for a connection, Server Started")

# Lưu trạng thái 2 người chơi
players = [{}, {}]  # game_state của từng người
connections = 0


def threaded_client(conn, player):
    print(f"Player {player} connected.")
    conn.send(pickle.dumps(player))

    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            players[player] = data
            if not data:
                print("Disconnected")
                break

            opponent = 1 - player
            reply = players[opponent] if players[opponent] else {}

            if 'ready' in players[0] and 'ready' in players[1]:
                reply["both_ready"] = True
                # print("Ca 2 da vao phong")

            if 'game_over' in players[0] and 'game_over' in players[1]:
                if players[0]['game_over'] and players[1]['game_over']:
                    p0_score = players[0].get("score", 0)
                    p1_score = players[1].get("score", 0)

                    if p0_score > p1_score:
                        players[0]["result"] = "win"
                        players[1]["result"] = "lose"
                    elif p0_score < p1_score:
                        players[0]["result"] = "lose"
                        players[1]["result"] = "win"
                    else:
                        players[0]["result"] = "draw"
                        players[1]["result"] = "draw"
                else:
                    players[0]["result"] = None
                    players[1]["result"] = None
                reply["result"] = players[player].get("result", None)
            conn.sendall(pickle.dumps(reply))

        except:
            break

    print("Lost connection to player", player)
    players[player] = {}
    conn.close()

# Chờ tối đa 2 người chơi
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, connections))
    connections += 1
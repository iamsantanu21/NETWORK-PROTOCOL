import socket
import threading
import json
import time
import sys

class Router:
    def __init__(self, name, port, neighbors):
        self.name = name
        self.port = port
        self.neighbors = neighbors  # {router_name: port}
        self.routing_table = {name: (0, name)}  # {destination: (cost, next_hop)}

    def start(self):
        threading.Thread(target=self.listen).start()
        threading.Thread(target=self.broadcast).start()
        threading.Thread(target=self.command_input).start()

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('localhost', self.port))
            while True:
                data, _ = s.recvfrom(2048)
                msg = json.loads(data.decode())

                if msg["type"] == "routing":
                    self.update_routing_table(msg["sender"], msg["table"])
                elif msg["type"] == "message":
                    self.forward_message(msg)

    def update_routing_table(self, sender, received_table):
        updated = False
        for dest, (cost, _) in received_table.items():
            new_cost = cost + 1
            if dest not in self.routing_table or new_cost < self.routing_table[dest][0]:
                self.routing_table[dest] = (new_cost, sender)
                updated = True

        if updated:
            print(f"[{self.name}] Updated Routing Table: {self.routing_table}")

    def broadcast(self):
        while True:
            time.sleep(5)
            msg = {
                "type": "routing",
                "sender": self.name,
                "table": self.routing_table
            }
            for neighbor, port in self.neighbors.items():
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.sendto(json.dumps(msg).encode(), ('localhost', port))

    def command_input(self):
        while True:
            user_input = input(f"[{self.name}] Enter 'send <destination> <message>': ")
            if user_input.startswith("send"):
                parts = user_input.split()
                if len(parts) >= 3:
                    dest = parts[1]
                    msg_body = " ".join(parts[2:])
                    self.send_message(dest, msg_body)

    def send_message(self, destination, body):
        if destination not in self.routing_table:
            print(f"[{self.name}] No route to {destination}")
            return

        next_hop = self.routing_table[destination][1]
        next_port = self.neighbors.get(next_hop)

        if next_port:
            msg = {
                "type": "message",
                "source": self.name,
                "destination": destination,
                "body": body,
                "path": [self.name]
            }
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(json.dumps(msg).encode(), ('localhost', next_port))
            print(f"[{self.name}] Sent message to {destination} via {next_hop}")
        else:
            print(f"[{self.name}] Next hop {next_hop} not reachable.")

    def forward_message(self, msg):
        msg["path"].append(self.name)
        if msg["destination"] == self.name:
            print(f"[{self.name}] Received message from {msg['source']}: {msg['body']}")
            print(f"[{self.name}] Path taken: {' -> '.join(msg['path'])}")
        else:
            if msg["destination"] not in self.routing_table:
                print(f"[{self.name}] No route to {msg['destination']}")
                return

            next_hop = self.routing_table[msg["destination"]][1]
            next_port = self.neighbors.get(next_hop)
            if next_port:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.sendto(json.dumps(msg).encode(), ('localhost', next_port))
                print(f"[{self.name}] Forwarding message to {msg['destination']} via {next_hop}")
            else:
                print(f"[{self.name}] Next hop {next_hop} not reachable.")


if __name__ == "__main__":
    config = json.load(open('network_config.json'))
    router_name = sys.argv[1]
    info = config[router_name]
    router = Router(router_name, info["port"], info["neighbors"])
    router.start()

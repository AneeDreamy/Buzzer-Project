import pygame
import sys
import bluetooth
import time
import threading

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
GREY = (169, 169, 169)
LIGHT_GREY = (211, 211, 211)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bluetooth Connection")

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class BluetoothApp:
    def __init__(self):
        self.devices = [
            {"name": "Team A", "bd_addr": "98:D3:61:F5:D7:C0", "port": 1},
            {"name": "Team G", "bd_addr": "00:24:01:01:04:7E", "port": 1},
            # Add more devices as needed
        ]
        self.socks = []
        self.connected_devices = []
        self.startup = True
        self.main_page = False
        self.connect_requested = False
        self.text = ''
        self.setup_startup_page()
        self.buzzers_joined = 0
        self.num_teams = 0
        self.connect_button_clicked = False
        self.message_ranking = []
        self.rankings = {}
        self.message_received = False

    def setup_startup_page(self):
        self.startup = True
        self.main_page = False
        self.input_rect = pygame.Rect((SCREEN_WIDTH - 170) // 2, 170, 150, 50)
        self.active = False
        self.instruction_text1 = font.render("Welcome to WhichBuzz!", True, BLACK)
        self.instruction_text2 = small_font.render("Input the number of teams into the box below", True, BLACK)
        self.instruction_text3 = small_font.render("and press the enter key on your keyboard to continue.", True, BLACK)
        self.instruction_pos1 = self.instruction_text1.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.instruction_pos2 = self.instruction_text2.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.instruction_pos3 = self.instruction_text3.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.cursor = pygame.Rect((self.input_rect.x + 5, self.input_rect.y + 10, 2, self.input_rect.height - 20))

    def setup_main_page(self):
        self.startup = False
        self.main_page = True
        self.update_status_label()
        # Buttons
        button_width = 80
        button_height = 30
        margin = 20
        self.connect_button_rect = pygame.Rect(margin, 20, button_width + 100, button_height)
        self.back_button_rect = pygame.Rect(SCREEN_WIDTH - button_width - margin, 20, button_width, button_height)
        self.reset_button_rect = pygame.Rect(margin, SCREEN_HEIGHT - button_height - margin, button_width + 50, button_height)
        
        self.connect_button_text = small_font.render("Connect Bluetooth", True, BLACK)
        self.back_button_text = font.render("Back", True, BLACK)
        self.reset_button_text = small_font.render("Reset Rankings", True, BLACK)

    def update_status_label(self):  # number of buzzers joined
        color = ORANGE if self.buzzers_joined < self.num_teams else GREEN
        self.status_label = small_font.render(f"{self.buzzers_joined}/{self.num_teams} buzzers joined", True, color)
        self.status_pos = (200, 350)

    def connect_bluetooth_devices(self):
        try:
            # Close all existing connections
            for sock in self.socks:
                sock.close()
            self.socks = []
            self.connected_devices = []
            self.buzzers_joined = 0

            for i, device in enumerate(self.devices):
                if i < self.num_teams:
                    bd_addr = device["bd_addr"]
                    port = device["port"]

                    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                    sock.connect((bd_addr, port))
                    print(f"Connected to {bd_addr} ({device['name']})")

                    # Store the socket object
                    self.socks.append(sock)

                    # Store the connected device's name
                    self.connected_devices.append({"name": device["name"], "rank": None})
                    self.buzzers_joined += 1
                    self.update_status_label()

            # Start threads to receive messages from each device
            for i, sock in enumerate(self.socks):
                threading.Thread(target=self.receive_data, args=(sock, self.connected_devices[i]['name']), daemon=True).start()

        except bluetooth.BluetoothError as e:
            print(f"Bluetooth error: {e}")
        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Exiting...")

    def receive_data(self, sock, device_name):
        received_message = ''
        while True:
            data = sock.recv(1024)  # Receive data from the Bluetooth connection
            if data:
                dataed = data.decode('utf-8')  # Decode the received data as UTF-8
                received_message += dataed  # Append received data to the message

                # Check if the special character '*' is present in the received data
                if '*' in dataed:
                    # Extract the team identifier from the message
                    if len(received_message) >= 7 and received_message[:6] == "BUZZED":
                        team_char = received_message[6]
                        if team_char.isalpha():
                            team_name = self.get_team_name(team_char)
                            print(f"Received message from {team_name}: {received_message}")
                            self.team_buzzed(team_char, team_name)

                    # Empty the received message string for reuse
                    received_message = ''

    def get_team_name(self, team_char):
        for device in self.devices:
            if device["name"].endswith(team_char):
                return device["name"]
        return "Unknown"

    def team_buzzed(self, team_char, device_name):
        for device in self.connected_devices:
            if device["name"] == device_name and device["rank"] is None:
                device["rank"] = len(self.message_ranking) + 1
                self.message_ranking.append(device)
                self.rankings = {device['name']: device['rank'] for device in self.message_ranking}
                self.message_ranking.sort(key=lambda x: x["rank"])
                self.message_received = True

    def reset_rankings(self):
        for device in self.connected_devices:
            device["rank"] = None
        self.message_ranking = []
        self.rankings = {}
        self.message_received = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.startup:
                    if event.key == pygame.K_RETURN:
                        try:
                            self.num_teams = int(self.text)
                            self.setup_main_page()
                        except ValueError:
                            self.text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.main_page:
                    if self.connect_button_rect.collidepoint(event.pos):
                        self.connect_requested = True
                        self.connect_button_clicked = True
                    elif self.back_button_rect.collidepoint(event.pos):
                        self.setup_startup_page()
                    elif self.reset_button_rect.collidepoint(event.pos):
                        self.reset_rankings()

    def draw_startup_page(self):
        screen.fill(WHITE)
        screen.blit(self.instruction_text1, self.instruction_pos1)
        screen.blit(self.instruction_text2, self.instruction_pos2)
        screen.blit(self.instruction_text3, self.instruction_pos3)
        pygame.draw.rect(screen, BLACK, self.input_rect, 2)
        text_surface = font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 10))
        if time.time() % 1 > 0.5:
            text_rect = text_surface.get_rect(topleft=(self.input_rect.x + 5, self.input_rect.y + 10))
            self.cursor.midleft = text_rect.midright
            pygame.draw.rect(screen, BLACK, self.cursor)
        pygame.display.flip()

    def draw_main_page(self):
        screen.fill(WHITE)
        # Draw status label
        screen.blit(self.status_label, self.status_pos)

        # Bluetooth Connect Button
        button_color = LIGHT_GREY if self.connect_button_clicked else GREY
        pygame.draw.rect(screen, button_color, self.connect_button_rect)
        connect_text_pos = self.connect_button_text.get_rect(center=self.connect_button_rect.center)
        screen.blit(self.connect_button_text, connect_text_pos)

        # Back button
        pygame.draw.rect(screen, GREY, self.back_button_rect)
        back_text_pos = self.back_button_text.get_rect(center=self.back_button_rect.center)
        screen.blit(self.back_button_text, back_text_pos)

        # Reset Rankings button
        pygame.draw.rect(screen, RED, self.reset_button_rect)
        reset_text_pos = self.reset_button_text.get_rect(center=self.reset_button_rect.center)
        screen.blit(self.reset_button_text, reset_text_pos)

        # Draw connected devices and their rankings
        x_offset = 50
        y_offset = 100
        team_rect_width = 150
        team_rect_height = 50
        margin = 20

        for device in self.connected_devices:
            pygame.draw.rect(screen, LIGHT_GREEN, (x_offset, y_offset, team_rect_width, team_rect_height), border_radius=5)
            rank_text = small_font.render(f"{self.rankings.get(device['name'], '')} {device['name']}", True, BLACK)
            text_pos = rank_text.get_rect(center=(x_offset + team_rect_width // 2, y_offset + team_rect_height // 2))
            screen.blit(rank_text, text_pos)
            x_offset += team_rect_width + margin
            if x_offset + team_rect_width > SCREEN_WIDTH:
                x_offset = 50
                y_offset += team_rect_height + margin

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            if self.startup:
                self.draw_startup_page()
            elif self.main_page:
                self.draw_main_page()
            if self.connect_requested:
                self.connect_bluetooth_devices()
                self.connect_requested = False
                self.connect_button_clicked = False

# Start the application
if __name__ == "__main__":
    app = BluetoothApp()
    app.run()

# TEE PELI TÄHÄN
import pygame
from pygame.constants import K_r
# floor: f, wall: w, teleport: t, player: p, enemy: e, button: b, goal: v


class Game:

    def __init__(self):
        pygame.init()
        self.naytto = pygame.display.set_mode((1400, 900))
        self.clock = pygame.time.Clock()
        self.my_font = pygame.font.SysFont('Arial', 30)

    def start_new_game(self):
        self.naytto.fill((0, 0, 0))

        self.world_map = [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
                          ['w', 'p', 'f', 'f', 'f', 'f', 'f', 'f', 't1', 'w', 't4', 'w'],
                          ['w', 'f', 't3', 'f', 'f', 'w', 'f', 'f', 'f', 'w', 'f', 'w'],
                          ['w', 't2', 'f', 'f', 'w', 'w', 'w', 'f', 'f', 'w', 'f', 'w'],
                          ['w', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'e1', 'w', 'f', 'w'],
                          ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'f', 'w'],
                          ['w', 'b', 'w', 'f', 'f', 'f', 'f', 'f', 'f', 'w', 'f', 'w'],
                          ['w', 'f', 'w', 'w', 'w', 'w', 'f', 'f', 'f', 'w', 'f', 'w'],
                          ['w', 'f', 'f', 'f', 'f', 'f', 'w', 'f', 'f', 'w', 'v', 'w'],
                          ['w', 'w', 'w', 'w', 'w', 'f', 'w', 'f', 'f', 'w', 'f', 'w'],
                          ['w', 'e2', 'f', 'f', 'f', 'f', 'w', 'f', 'f', 'w', 'f', 'w'],
                          ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
                          ]

        self.exit_coords = self.find_on_map('v')
        self.world_map[self.exit_coords[0]][self.exit_coords[1]] = 'f'  # hide exit until button is pressed

        self.teleport_links = {'t1': 't2',
                               't2': 't1',
                               't3': 't4',
                               't4': 't3'}
        self.teleport_coords = {}

        for teleport in self.teleport_links:
            pos = self.find_on_map(teleport)
            self.teleport_coords[teleport] = pos

        self.map_height = len(self.world_map)
        self.map_width = len(self.world_map[0])
        self.map_size = self.map_height*self.map_width
        self.skaala = 75

        self.enemies = []
        for y in self.world_map:
            for tile in y:
                if tile.startswith('e'):
                    self.enemies.append(tile)

        self.images = []
        self.images.append(pygame.image.load('ovi.png'))
        self.images.append(pygame.image.load('robo.png'))
        self.images.append(pygame.image.load('hirvio.png'))
        self.images.append(pygame.image.load('kolikko.png'))

        self.turn = 0
        self.start_turn()

    def draw_map(self):
        self.naytto.fill((50, 25, 10))
        for y in range(self.map_height):
            for x in range(self.map_width):
                tile = self.world_map[y][x]
                if tile == 'w':
                    pygame.draw.rect(self.naytto, (100, 50, 0), (x*self.skaala, y*self.skaala, self.skaala, self.skaala), 2)
                elif tile in self.teleport_links:
                    self.naytto.blit(self.images[0], (x*self.skaala, y*self.skaala))
                elif tile == 'p':
                    self.naytto.blit(self.images[1], (x*self.skaala, y*self.skaala))
                elif tile == 'b':
                    self.naytto.blit(self.images[3], (x*self.skaala, y*self.skaala))
                elif tile == 'v':
                    pygame.draw.rect(self.naytto, (0, 150, 50), (x*self.skaala, y*self.skaala, self.skaala, self.skaala))
                elif tile in self.enemies:
                    self.naytto.blit(self.images[2], (x*self.skaala, y*self.skaala))
        moves = self.my_font.render(f'Moves: {self.turn}', 30, (0, 200, 100))
        self.naytto.blit(moves, (self.naytto.get_width()-150, 20))
        guide1 = self.my_font.render('Ghosts move twice ', 30, (0, 200, 100))
        guide2 = self.my_font.render('as fast as you.', 30, (0, 200, 100))
        self.naytto.blit(guide1, (self.naytto.get_width()-400, 70))
        self.naytto.blit(guide2, (self.naytto.get_width()-400, 100))
        pygame.display.flip()

    def find_on_map(self, tile: str):  # returns coordinates of tile
        for y in self.world_map:
            for x in y:
                if x == tile:
                    return (self.world_map.index(y), y.index(x))

    def regen_teleports(self):  # teleports disappear from map when someone stands on them, this will regenerate them
        for tp, coords in self.teleport_coords.items():
            if self.world_map[coords[0]][coords[1]] == 'p':
                continue
            if self.world_map[coords[0]][coords[1]] in self.enemies:
                continue
            self.world_map[coords[0]][coords[1]] = tp

    def move_entity(self, entity, direction):  # returns True if movement is completed, otherwise False
        entity_pos = self.find_on_map(entity)
        if direction == 'UP':
            if entity_pos[0]-1 < 0:
                return False
            new_entity_pos = (entity_pos[0]-1, entity_pos[1])
        elif direction == 'RIGHT':
            if entity_pos[1]+1 >= self.map_width:
                return False
            new_entity_pos = (entity_pos[0], entity_pos[1]+1)
        elif direction == 'DOWN':
            if entity_pos[0]+1 >= self.map_height:
                return False
            new_entity_pos = (entity_pos[0]+1, entity_pos[1])
        elif direction == 'LEFT':
            if entity_pos[1]-1 < 0:
                return False
            new_entity_pos = (entity_pos[0], entity_pos[1]-1)

        new_tile = self.world_map[new_entity_pos[0]][new_entity_pos[1]]
        if new_tile == 'w':
            return False
        elif new_tile == 'b':
            self.world_map[self.exit_coords[0]][self.exit_coords[1]] = 'v'
        elif new_tile == 'p' or new_tile in self.enemies:
            self.world_map[entity_pos[0]][entity_pos[1]] = 'f'
            self.world_map[new_entity_pos[0]][new_entity_pos[1]] = entity
            self.end_game('LOST')
        elif new_tile == 'v':
            if entity == 'p':
                self.world_map[entity_pos[0]][entity_pos[1]] = 'f'
                self.world_map[new_entity_pos[0]][new_entity_pos[1]] = entity
                self.end_game('WON')
        elif new_tile in self.teleport_links:
            teleport_to = self.find_on_map(self.teleport_links[new_tile])
            new_entity_pos = teleport_to
        self.world_map[entity_pos[0]][entity_pos[1]] = 'f'
        self.world_map[new_entity_pos[0]][new_entity_pos[1]] = entity
        return True

    def end_turn(self):
        self.turn += 1
        self.regen_teleports()
        player_pos = self.find_on_map('p')
        for enemy in self.enemies:
            enemy_pos = self.find_on_map(enemy)
            if player_pos == enemy_pos:
                self.end_game('LOST')

        for i in range(2):  # this is here because ghosts move twice
            self.regen_teleports()
            for enemy in self.enemies:
                enemy_pos = self.find_on_map(enemy)
                player_direction = []
                if player_pos == enemy_pos:
                    self.end_game('LOST')
                if player_pos[0] > enemy_pos[0]:
                    player_direction.append('DOWN')
                if player_pos[0] < enemy_pos[0]:
                    player_direction.append('UP')
                if player_pos[1] < enemy_pos[1]:
                    player_direction.append('LEFT')
                if player_pos[1] > enemy_pos[1]:
                    player_direction.append('RIGHT')
                movement = self.move_entity(enemy, player_direction[0])
                if not movement and len(player_direction) == 2:
                    self.move_entity(enemy, player_direction[1])
                self.draw_map()
                pygame.time.wait(10)
                enemy_pos = self.find_on_map(enemy)
        if player_pos == enemy_pos:
            self.end_game('LOST')

    def start_turn(self):
        while True:
            self.draw_map()
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_r:
                        self.start_new_game()
                    if tapahtuma.key == pygame.K_UP:
                        self.move_entity('p', 'UP')
                    if tapahtuma.key == pygame.K_RIGHT:
                        self.move_entity('p', 'RIGHT')
                    if tapahtuma.key == pygame.K_DOWN:
                        self.move_entity('p', 'DOWN')
                    if tapahtuma.key == pygame.K_LEFT:
                        self.move_entity('p', 'LEFT')
                    self.end_turn()

    def end_game(self, type):
        self.draw_map()
        if type == 'LOST':
            text = self.my_font.render('You lost :(', 30, (0, 200, 100))
            self.naytto.blit(text, (self.naytto.get_width()-400, 400))
        elif type == 'WON':
            text = self.my_font.render('You won!', 30, (0, 200, 100))
            self.naytto.blit(text, (self.naytto.get_width()-400, 400))
        text = self.my_font.render('Press R to restart,', 30, (0, 200, 100))
        self.naytto.blit(text, (self.naytto.get_width()-400, 430))
        text = self.my_font.render('or any other key to quit.', 30, (0, 200, 100))
        self.naytto.blit(text, (self.naytto.get_width()-400, 460))
        pygame.display.flip()
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_r:
                        self.start_new_game()
                    else:
                        exit()


def run():
    game = Game()
    game.start_new_game()


if __name__ == '__main__':
    run()

import os
import random
import time
import sys

from events import *

colision_enemy_player: Event = Event(
    name="colision_enemy_player", arguments_template=()
)
colision_enemy_enemy: Event = Event(
    name="colision_enemy_enemy", arguments_template=("colisor", "colidido")
)
player_movement: Event = Event(name="player_movement", arguments_template=("position"))
enemy_movement: Event = Event(name="enemy_movement", arguments_template=("position"))
game_starts: Event = Event(name="game_starts", arguments_template=(""))


class Movable(EventTrigger):

    x = 0
    y = 1

    @property
    def position(self) -> tuple:
        return self._position

    @property
    def game(self) -> "Game":
        return self._game

    def __init__(self, initial_position: tuple, game: "Game", movement_event: Event):
        self._position = initial_position
        self._game = game
        self._movement_event = movement_event

    def move(self):
        self._movement_event.trigger(self, position=self.position)


class RandomWalker(Movable):

    def _move_up(self):
        self._position = (self._position[Movable.x], self._position[Movable.y] - 1)

    def _move_down(self):
        self._position = (self._position[Movable.x], self._position[Movable.y] + 1)

    def _move_left(self):
        self._position = (self._position[Movable.x] - 1, self._position[Movable.y])

    def _move_right(self):
        self._position = (self._position[Movable.x] + 1, self._position[Movable.y])

    def _stay_still(self):
        pass

    @property
    def _valid_movements(self) -> tuple:
        map_min_value: int = 0
        valid_movements = [self._stay_still]
        if self._position[Movable.y] > map_min_value:
            valid_movements.append(self._move_up)
        if self._position[Movable.y] < self._game.map_height - 1:
            valid_movements.append(self._move_down)
        if self._position[Movable.x] > map_min_value:
            valid_movements.append(self._move_left)
        if self._position[Movable.x] < self._game.map_width - 1:
            valid_movements.append(self._move_right)
        return valid_movements

    def move(self):
        random.choice(self._valid_movements)()
        Movable.move(self)


class Player(RandomWalker, EventListener):

    @staticmethod
    def _on_enemy_move(listener: EventListener, trigger: EventTrigger, _):
        if listener.position == trigger.position:
            listener.trigger(colision_enemy_player)

    def __init__(self, initial_position: tuple, game: "Game"):
        EventListener.__init__(self)
        RandomWalker.__init__(self, initial_position, game, player_movement)
        self.listen_event(enemy_movement, (Player._on_enemy_move,))


class Enemy(RandomWalker, EventListener):

    @staticmethod
    def _on_collides_with_enemy(listener: EventListener, _, trigger_data: dict):
        if trigger_data["colisor"] == listener:
            listener.move()

    @staticmethod
    def _on_move(listener: EventListener, trigger: EventTrigger, trigger_data: dict):
        if trigger.position == listener.position and trigger != listener:
            listener.trigger(colision_enemy_enemy, colisor=trigger)

    def __init__(self, initial_position: tuple, game: "Game"):
        EventListener.__init__(self)
        RandomWalker.__init__(self, initial_position, game, enemy_movement)
        self.listen_event(colision_enemy_enemy, (Enemy._on_collides_with_enemy,))
        self.listen_event(enemy_movement, (Enemy._on_move,), 1)


def pick_position(width: int, height: int, occupied_positions: list):
    position: tuple = (
        random.randrange(width),
        random.randrange(height),
    )
    while position in occupied_positions:
        position: tuple = (
            random.randrange(width),
            random.randrange(height),
        )
    return position


class Game(EventListener, EventTrigger):

    @staticmethod
    def _on_player_dies(listener: EventListener, _, __):
        listener.finalize()

    def __init__(self):
        EventListener.__init__(self)
        EventTrigger.__init__(self)
        self._enemies = []
        self._player = None
        self._map_height = 0
        self._map_width = 0
        self._is_running = False
        self.listen_event(colision_enemy_player, (Game._on_player_dies,))

    @property
    def map_height(self) -> int:
        return self._map_height

    @property
    def map_width(self) -> int:
        return self._map_width

    def __initialize(self, enemies_count: int):
        occupied_positions: list = []

        for _ in range(enemies_count):
            position = pick_position(
                self.map_width, self.map_height, occupied_positions
            )
            self._enemies.append(Enemy(position, self))
            occupied_positions.append(position)
        position = pick_position(self.map_height, self.map_height, occupied_positions)
        self._player: Player = Player(position, self)

    def execute(
        self,
        enemies_count: int = 10,
        map_width: int = 10,
        map_height: int = 10,
        chance: int = 100,
        sleep_time: int = 250,
        *args
    ):
        self._is_running: bool = True
        self._map_height: int = map_height
        self._map_width: int = map_width
        self.__initialize(enemies_count)
        self.__update_screen()
        score = lambda a, b, c, d: (a * (2.0 - b / 100.0)) / (c * d)
        lucky: float = -score(enemies_count, chance, self.map_height, self.map_width)

        while self._is_running:
            time.sleep(sleep_time / 1000.0)
            self._player.move()
            for i in self._enemies:
                i.move()
            self.__update_screen()
            lucky += score(enemies_count, chance, self.map_height, self.map_width)
            if random.random() > chance / 100:
                try:
                    del self._enemies[-1]
                except IndexError:
                    print("You Win!")
                    print("Luck: " + str(int(lucky * 100)))
                    input("Press ENTER to exit\n")
                    return

        print("GAME OVER")
        print("Luck: " + str(int(lucky * 100)))
        input("Press ENTER to exit\n")

    def finalize(self):
        self._is_running = False

    def __update_screen(self):
        self.__clean_screen()
        position_enemies: list = []
        position_player: tuple = self._player.position
        screen: str = ""
        for e in self._enemies:
            position_enemies.append(e.position)
        for i in range(self.map_height):
            for j in range(self.map_width):
                current_panel: tuple = (j, i)
                if current_panel in position_enemies:
                    if current_panel == position_player:
                        screen += "[X] "
                    else:
                        screen += "[I] "
                else:
                    if current_panel == position_player:
                        screen += "[O] "
                    else:
                        screen += "[ ] "
            screen += "\n"
        print(screen + "\n\n")

    def __clean_screen(self):
        if sys.platform == "linux":
            os.system("clear")
        else:
            os.system("cls")


if __name__ == "__main__":
    args: list = [int(arg) for arg in sys.argv[1:7]]
    GAME = Game()
    GAME.execute(*args)

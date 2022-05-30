from uuid import UUID, uuid4
from games import standart_classes
from dataclasses import dataclass, asdict

class InvalidPlaceException(Exception):
    def __init__(self, points: tuple[int, int]):
        super.__init__(f"Invalid ships placament {points}")

@dataclass
class SeaBattleTurn:
    player: UUID
    point: tuple[int, int]

@dataclass
class SeaBattlePlayer:
    id: UUID
    field: list[list[None|int]]
    hits: int = 20

@dataclass
class SeaBattleGameState(standart_classes.BaseGameState):
    playersData: tuple[SeaBattlePlayer, SeaBattlePlayer]
    isOver: bool = False

class SeaBattleGame(standart_classes.BaseGameClass): 
    def __init__(self, players: tuple[UUID] = None, ships: tuple[tuple[int, int], tuple[int, int]] = None, **kwargs):
        print(ships)
        if not players and not kwargs["players"]:
            raise Exception("players")
        elif not players and kwargs["players"]:
            players = kwargs["players"]

        if not ships and not kwargs["ships"]:
            raise Exception("no ships")
        elif not ships and kwargs["ships"]:
            ships = kwargs["ships"]

        self.__check_positions(ships)
        self.__state = SeaBattleGameState(
            (
                SeaBattlePlayer(players[0], field=self.__fill_field_with_ships(self.__create_field(), ships[0])),
                SeaBattlePlayer(players[1], field=self.__fill_field_with_ships(self.__create_field(), ships[1]))
            )
        )
        print(self.__state)
        self.__currentPlayerIdx = 1
        self.__currentPlayer = players[self.__currentPlayerIdx]
        

    def makeTurn(self, turn: SeaBattleTurn):
        if turn.player != self.__currentPlayer:
            raise

        if turn.point[0] > 9 or turn.point[1]: 
            raise

        if self.__state.isOver:
            raise

        old_state = self.__state

        another_player_idx = int(not self.__currentPlayerIdx)

        if self.__state.playersData[another_player_idx].field[turn.point[0]][turn.point[1]] == 1:
            self.__state.playersData[another_player_idx].field[turn.point[0]][turn.point[1]] = 0
            status = "hit"
            self.__state.playersData[another_player_idx].hits -= 1

        else:
            status = "miss"

        self.__winCheck()
        self.__changePlayers()
        return (status, asdict(old_state), asdict(self.__state))

        

    @staticmethod
    def __check_positions(ships):
        statement = True
        if not statement: raise InvalidPlaceException

    @staticmethod
    def __create_field():
        return [[None for x in range(10)] for y in range(10)]

    @staticmethod
    def __fill_field_with_ships(field, ships):
        print(ships)
        for point in ships:
            field[point[0]][point[1]] = 1
        return field

    def __changePlayers(self):
        self.__currentPlayerIdx = int(not self.__currentPlayerIdx)
        self.__currentPlayer = self.__state.playersData[self.__currentPlayerIdx].id

    def __winCheck(self):
        for player in self.__state.playersData:
            if player.hits <= 0:
                self.__state.isOver = True

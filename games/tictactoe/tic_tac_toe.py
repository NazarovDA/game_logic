from uuid import UUID
from games import standart_classes
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class TicTacToeTurn(standart_classes.BaseGameTurn):
    point: tuple[int, int]
    player: UUID


@dataclass()
class TicTacToeGameState(standart_classes.BaseGameState): 
    players: list[UUID]
    field: list[list[int|None]]
    win_streak: list[tuple[int, int]] | None = None

        
class TicTacToeGameClass(standart_classes.BaseGameClass):
    def __init__(self, players: list[UUID], timer: float = 60, length: int = 3, width: int = 3, winCon: int = 3) -> None:
        self.__state = TicTacToeGameState(
                players, 
                self.__createField((length, width))
            )
        self.__length, self.__width = length, width
        self.__current_value = 1
        self.__turnOf: UUID = players[0]
        self.__winCon = winCon
        self.__isOver = False


    def makeTurn(self, turn: TicTacToeTurn) -> Exception | tuple[dict, dict]:
        if turn.player != self.__turnOf: 
            print(turn.player, self.__turnOf, self.__state.players)
            raise
        if self.__isOver: raise

        if turn.point[0] > self.__length or turn.point[1] > self.__width: NotImplemented

        pointIsEmpty = True if self.__state.field[turn.point[0]][turn.point[1]] is None else False

        if not pointIsEmpty: NotImplemented

        else:
            old_state = self.__state
            self.__state.field[turn.point[0]][turn.point[1]] = self.__current_value
            self.__changeValue()
            self.__changePlayer()
            self.__winCheck()
            return (asdict(old_state), asdict(self.__state))

    def __changePlayer(self) -> None:
        self.__turnOf = self.__state.players[0] if self.__turnOf == self.__state.players[1] else self.__state.players[1]

    def __changeValue(self) -> None:
        self.__current_value = int(not self.__current_value)
    
    def __winCheck(self) -> None:
        for col in range(self.__length):
            for row in range(self.__width):
                rows = []
                cols = []
                diag_left = []
                diag_right = []
                current = self.__state.field[row][col]
                if current == None:
                    continue
                for shift in range(self.__winCon):
                    if col+shift < self.__length and current == self.__state.field[row][col + shift]:
                        cols.append((row, col + shift))
                    if row + shift < self.__width and current == self.__state.field[row + shift][col]:
                        rows.append((row + shift, col))
                    if row + shift < self.__width and col+shift < self.__length \
                            and current == self.__state.field[row + shift][col + shift]:
                        diag_right.append((row + shift, col + shift))
                    if row + shift < self.__width and col-shift >= 0 and \
                            current == self.__state.field[row+shift][col-shift]:
                        diag_left.append((row + shift, col-shift))
                if len(rows) == self.__winCon:
                    self.__isOver = True
                    self.__state.win_streak = rows
                if len(cols) == self.__winCon:
                    self.__isOver = True
                    self.__state.win_streak = cols
                if len(diag_left) == self.__winCon:
                    self.__isOver = True
                    self.__state.win_streak = diag_left
                if len(diag_right) == self.__winCon:
                    self.__isOver = True
                    self.__state.win_streak = diag_right

    def __createField(self, dims: tuple[int, int]) -> list:
        return [[None for x in range(dims[0])] for y in range(dims[1])]

    def getCurrentState(self) -> dict:
        return asdict(self.__state)

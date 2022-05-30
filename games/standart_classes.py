from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class BaseGameTurn: pass

@dataclass()
class BaseGameState: pass


class BaseGameClass():
    def __init__(self) -> None: pass

    def makeTurn(self, turn: BaseGameTurn) -> Exception|tuple[BaseGameState, BaseGameState]: pass

    def allReady(self, flag): pass

    def getCurrentState(self) -> BaseGameState: 
        return self.__state.asdict()


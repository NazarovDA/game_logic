from games.standart_classes import BaseGameClass
from games.tictactoe.tic_tac_toe import TicTacToeGameClass as TTT, TicTacToeTurn
from games.seabattle.sea_battle import SeaBattleGame as SBG, SeaBattleTurn


class GameCreator:
    __implementedGames = { 1: "tic-tac-toe", 2: "sea battle"}
    __gamesInits = { 1: TTT, 2: SBG}

    @staticmethod
    def get_implemented_games() -> dict[str, int]:
        return GameCreator.__implementedGames

    @staticmethod
    def create_game(gameCode: int, **kwargs) -> BaseGameClass: 
        if gameCode not in GameCreator.__implementedGames.keys(): return NotImplemented
        return GameCreator.__gamesInits[gameCode](**kwargs)

def ttt_test():
    from uuid import uuid4

    player1, player2 = uuid4(), uuid4()

    ttt = GameCreator.create_game(1, players=[player1, player2])

    print(ttt.makeTurn(TicTacToeTurn((0, 0), player1)))
    print(ttt.makeTurn(TicTacToeTurn((1, 0), player2)))
    print(ttt.makeTurn(TicTacToeTurn((0, 1), player1)))
    print(ttt.makeTurn(TicTacToeTurn((1, 1), player2)))
    print(ttt.makeTurn(TicTacToeTurn((0, 2), player1))) 
    print(ttt.makeTurn(TicTacToeTurn((1, 2), player2)))

def sbg_test():
    from uuid import uuid4

    player1, player2 = uuid4(), uuid4()

    sbg = GameCreator.create_game(
        2, 
        players=[player1, player2], 
        ships=(
            ((1, 1), (2, 2), (3, 3)), ((1, 1), (2, 2), (3, 3))
        )
    )

if __name__ == "__main__":
    #try: ttt_test()
    #except Exception as e: print(e)

    try: sbg_test()
    except Exception as e: print(e)

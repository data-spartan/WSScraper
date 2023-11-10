from dataclasses import dataclass
from typing import NamedTuple, Optional
from utils.queue import ResolvingQueue

@dataclass
class FootballAllowedGames:
    period: Optional[str] = "1"
    match_minutes:Optional[str] = 0
    resolving_queue: ResolvingQueue =ResolvingQueue

    def get_data(self) -> list:
        """
        returns live resolved games

        :return:
        """
        # return list(self.resolving_queue)
        return self.resolving_queue.return_()

    # self.resolving_queue.append_resolved_games(
    #     f"Next goal - Current score: {self.competitor_1_old_result}:{self.competitor_2_old_result}|2", "won")

    def run_games(self):
        self.check_result_change()
        # if self.period == "Ended":
        self.resolve_ended_game()

    def live_games(self):
        self.live_next_goal()
        self.live_btts()
        self.live_total_goals()

    def live_next_goal(self):

        for sum_ in range(1,9,1):
            if sum_==1:       
                sufix='st'
                # print(sum_,sufix)
            elif sum_==2:
                sufix='nd'
            elif sum_==3:
                sufix='rd'
            else:
                sufix='th'
            self.resolving_queue.append_resolved_games(
                f"{sum_}{sufix} Goal To Score|2",
                "won")
            self.resolving_queue.append_resolved_games(
                f"{sum_}{sufix} Goal To Score|1",
                "lost")
            self.resolving_queue.append_resolved_games(
                f"{sum_}{sufix} Goal To Score|no more goals",
                "lost")
            self.resolving_queue.append_resolved_games(
                f"1st Half {sum_}{sufix} Goal To Score|2",
                "won")
            self.resolving_queue.append_resolved_games(
                f"1st Half {sum_}{sufix} Goal To Score||1",
                "lost")
            self.resolving_queue.append_resolved_games(
                f"1st Half {sum_}{sufix} Goal To Score||no more goals",
                "lost")
            # else:
            self.resolving_queue.append_resolved_games(
                f"{sum_}{sufix} Goal To Score|1",
                "won")
            self.resolving_queue.append_resolved_games(
                f"{sum_}{sufix} Goal To Score|2",
                "lost")
            self.resolving_queue.append_resolved_games(
                f"{sum_}{sufix} Goal To Score|no more goals",
                "lost")
                # if self.period == "1":
            self.resolving_queue.append_resolved_games(
                f"1st Half {sum_}{sufix} Goal To Score|1",
                "won")
            self.resolving_queue.append_resolved_games(
                f"1st Half {sum_}{sufix} Goal To Score|2",
                "lost")
            self.resolving_queue.append_resolved_games(
                f"1st Half {sum_}{sufix} Goal To Score||no more goals",
                "lost")

    def live_btts(self):
        
        self.resolving_queue.append_resolved_games(
            f"Both Teams To Score|Yes",
            "won"
        )
        self.resolving_queue.append_resolved_games(
            f"Both Teams To Score|No",
            "lost"
        )

    def live_total_goals(self):
        for total in range(0, 8, 1):
            # if complete_result > (total + 0.5):
            self.resolving_queue.append_resolved_games(
                f"Total Goals {total + 0.5}|Over",
                "won"
            )
            self.resolving_queue.append_resolved_games(
                f"Total Goals {total + 0.5}|Under",
                "lost"
            )
            # else:
            self.resolving_queue.append_resolved_games(
                f"Total Goals {total + 0.5}|Over",
                "lost"
            )
            self.resolving_queue.append_resolved_games(
                f"Total Goals {total + 0.5}|Under",
                "won"
            )

    def check_result_change(self):
        self.live_games()
        # complete_result = self.competitor_1_result + self.competitor_2_result
        # complete_result_old = self.competitor_1_old_result + self.competitor_2_old_result
        # if complete_result != complete_result_old:
        #     self.live_games()
        # else:
        #     return

    def resolve_ended_game(self):
        self._game_correct_score()

    def _game_correct_score(self):
        
        pairs = [(x, y) for x in range(8) for y in range(8)]

        for i in pairs:
            # if ft == i:
            a, b = i
            self.resolving_queue.append_resolved_games(
                f"Correct Score|{a}-{b}",
                "won"
            )
            # else:
            x, y = i
            self.resolving_queue.append_resolved_games(f"Correct Score|{x}-{y}",
                                                        "lost"
                                                        )

if __name__ == "__main__":
    resolving_queue=ResolvingQueue()
    allowed_football_games=FootballAllowedGames(resolving_queue=resolving_queue)
    allowed_football_games.run_games()
    allowed={i['type'] for i in allowed_football_games.get_data()}
    print(allowed)
    # for i in allowed:
    #     del i['id'], i['status']
    # print(allowed)
from dataclasses import dataclass
from typing import NamedTuple, Optional
from utils.queue import ResolvingQueue

@dataclass
class FootballResolver:
    competitor_1_result: Optional[int] = 0
    competitor_2_result: Optional[int] = 0
    competitor_1_period_1_result: Optional[int] = 0
    competitor_2_period_1_result: Optional[int] = 0
    competitor_1_period_2_result: Optional[int] = 0
    competitor_2_period_2_result: Optional[int] = 0
    competitor_1_overtime1_result: Optional[int] = 0
    competitor_2_overtime1_result: Optional[int] = 0
    competitor_1_overtime2_result: Optional[int] = 0
    competitor_2_overtime2_result: Optional[int] = 0
    competitor_1_penalties_result: Optional[int] = 0
    competitor_2_penalties_result: Optional[int] = 0
    competitor_1_old_result: Optional[int] = 0
    competitor_2_old_result: Optional[int] = 0
    competitor_1_period_1_old_result: Optional[int] = 0
    competitor_2_period_1_old_result: Optional[int] = 0
    competitor_1_period_2_old_result: Optional[int] = 0
    competitor_2_period_2_old_result: Optional[int] = 0
    competitor_1_overtime1_old_result: Optional[int] = 0
    competitor_2_overtime1_old_result: Optional[int] = 0
    competitor_1_overtime2_old_result: Optional[int] = 0
    competitor_2_overtime2_old_result: Optional[int] = 0
    competitor_1_penalties_old_result: Optional[int] = 0
    competitor_2_penalties_old_result: Optional[int] = 0
    corners: Optional[int] = 0
    yellow_cards_comp1: Optional[int] = 0
    yellow_cards_comp2: Optional[int] = 0
    red_cards_comp1: Optional[int] = 0
    red_cards_comp2: Optional[int] = 0
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
        if self.period == "Ended":
            self.resolve_ended_game()

    def live_games(self):
        self.live_next_goal()
        self.live_btts()
        self.live_total_goals()

    def live_next_goal(self):
        sum_ = self.competitor_1_result + self.competitor_2_result + 1
        sum_half = self.competitor_1_period_1_result + self.competitor_2_period_1_result + 1
        if sum_==1:
            sufix='st'
        elif sum_==2:
            sufix='nd'
        elif sum_==3:
            sufix='rd'
        else:
            sufix='th'

        if self.competitor_2_result > self.competitor_2_old_result:

            self.resolving_queue.append_resolved_games(
                f"{sum_}{sufix} Goal To Score|2",
                "won")
            self.resolving_queue.append_resolved_games(
                f"{sum_}{sufix} Goal To Score|1",
                "lost")
            self.resolving_queue.append_resolved_games(
                f"{sum_}{sufix} Goal To Score|no more goals",
                "lost")
            if self.period == "1":
                '"1st Half 1st Goal To Score'
                self.resolving_queue.append_resolved_games(
                    f"1st Half {sum_}{sufix} Goal To Score|2",
                    "won")
                self.resolving_queue.append_resolved_games(
                    f"1st Half {sum_}{sufix} Goal To Score||1",
                    "lost")
                self.resolving_queue.append_resolved_games(
                    f"1st Half {sum_}{sufix} Goal To Score||no more goals",
                    "lost")
        else:
            self.resolving_queue.append_resolved_games(
                f"{sum_}{sufix} Goal To Score|1",
                "won")
            self.resolving_queue.append_resolved_games(
                f"{sum_}{sufix} Goal To Score|2",
                "lost")
            self.resolving_queue.append_resolved_games(
                f"{sum_}{sufix} Goal To Score|no more goals",
                "lost")
            if self.period == "1":
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
        if self.competitor_1_result > 0 and self.competitor_2_result > 0:
            self.resolving_queue.append_resolved_games(
                f"Both Teams To Score|Yes",
                "won"
            )
            self.resolving_queue.append_resolved_games(
                f"Both Teams To Score|No",
                "lost"
            )

    def live_total_goals(self):
        complete_result = self.competitor_1_result + self.competitor_2_result
        for total in range(0, 8, 1):
            if complete_result > (total + 0.5):
                self.resolving_queue.append_resolved_games(
                    f"Total Goals {total + 0.5}|Over",
                    "won"
                )
                self.resolving_queue.append_resolved_games(
                    f"Total Goals {total + 0.5}|Under",
                    "lost"
                )
            else:
                self.resolving_queue.append_resolved_games(
                    f"Total Goals {total + 0.5}|Over",
                    "lost"
                )
                self.resolving_queue.append_resolved_games(
                    f"Total Goals {total + 0.5}|Under",
                    "won"
                )

    def check_result_change(self):
        complete_result = self.competitor_1_result + self.competitor_2_result
        complete_result_old = self.competitor_1_old_result + self.competitor_2_old_result
        if complete_result != complete_result_old:
            self.live_games()
        else:
            return

    def resolve_ended_game(self):
        self._game_correct_score()

    def _game_correct_score(self):
        competitor_1_result = self.competitor_1_result
        competitor_2_result = self.competitor_2_result
        pairs = [(x, y) for x in range(8) for y in range(8)]
        ft = (competitor_1_result, competitor_2_result)

        for i in pairs:
            if ft == i:
                a, b = i
                self.resolving_queue.append_resolved_games(
                    f"Correct Score|{a}-{b}",
                    "won"
                )
            else:
                x, y = i
                self.resolving_queue.append_resolved_games(f"Correct Score|{x}-{y}",
                                                           "lost"
                                                           )

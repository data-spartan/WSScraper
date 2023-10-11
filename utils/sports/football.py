from dataclasses import dataclass
from typing import NamedTuple, Optional

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

    def __post_init__(self):
        self.games_resolved_live: list = []

    def append_resolved_games(self, game_type, status) -> None:
        """
        :param status:
        :param game_type:

        :return:
        """

        game_resolved = {
            "type": game_type,
            "status": status
        }
        self.games_resolved_live.append(game_resolved)


    def get_data(self) -> tuple:
        """
        returns live resolved games

        :return:
        """
        return self.games_resolved_live

    def run_games(self):
        self.check_result_change()
        if self.period == "finished":
            self.resolve_ended_game()

    def resolve_first_half(self):
        self._game_handicap_1_half()
        self._game_which_team_wins_rest_of_1_half()
        self._game_draw_no_bet_1_half()
        self._game_first_half_result()
        self._game_1_half_double_chance()
        self._game_matchbet_1_half_totals_ou()
        self._game_matchbet_1_half()
        self._game_1_half_totals()


    def check_result_change(self):
        complete_result = self.competitor_1_result + self.competitor_2_result
        complete_result_old = self.competitor_1_old_result + self.competitor_2_old_result

        if complete_result > complete_result_old:
            if self.competitor_2_result > self.competitor_2_old_result:

                self.append_resolved_games(f"main|Next goal - Current score: {self.competitor_1_old_result}:{self.competitor_2_old_result}|2","won")
                self.append_resolved_games(f"main|Next goal - Current score: {self.competitor_1_old_result}:{self.competitor_2_old_result}|1","lost")
                self.append_resolved_games(f"main|Next goal - Current score: {self.competitor_1_old_result}:{self.competitor_2_old_result}|no more goals","lost")
                if self.period == "1":
                    self.append_resolved_games(f"main|1. Half Next Goal - Current score: {self.competitor_1_period_1_old_result}:{self.competitor_2_period_1_old_result}|2", "won")
                    self.append_resolved_games(f"main|1. Half Next Goal - Current score: {self.competitor_1_period_1_old_result}:{self.competitor_2_period_1_old_result}|1", "lost")
                    self.append_resolved_games(f"main|1. Half Next Goal - Current score: {self.competitor_1_period_1_old_result}:{self.competitor_2_period_1_old_result}|no more goals", "lost")
                elif self.period == "2":
                    self.append_resolved_games(f"main|2. Half Next Goal - Current score: {self.competitor_1_period_2_old_result}:{self.competitor_2_period_2_old_result}|2", "won")
                    self.append_resolved_games(f"main|2. Half Next Goal - Current score: {self.competitor_1_period_2_old_result}:{self.competitor_2_period_2_old_result}|1", "lost")
                    self.append_resolved_games(f"main|2. Half Next Goal - Current score: {self.competitor_1_period_2_old_result}:{self.competitor_2_period_2_old_result}|no more goals", "lost")
            else:
                self.append_resolved_games(f"main|Next goal - Current score: {self.competitor_1_old_result}:{self.competitor_2_old_result}|1","won")
                self.append_resolved_games(f"main|Next goal - Current score: {self.competitor_1_old_result}:{self.competitor_2_old_result}|2","lost")
                self.append_resolved_games(f"main|Next goal - Current score: {self.competitor_1_old_result}:{self.competitor_2_old_result}|no more goals","lost")
                if self.period == "1":
                    self.append_resolved_games(f"main|1. Half Next Goal - Current score: {self.competitor_1_period_1_old_result}:{self.competitor_2_period_1_old_result}|1", "won")
                    self.append_resolved_games(f"main|1. Half Next Goal - Current score: {self.competitor_1_period_1_old_result}:{self.competitor_2_period_1_old_result}|2", "lost")
                    self.append_resolved_games(f"main|1. Half Next Goal - Current score: {self.competitor_1_period_1_old_result}:{self.competitor_2_period_1_old_result}|no more goals", "lost")
                elif self.period == "2":
                    self.append_resolved_games(f"main|2. Half Next Goal - Current score: {self.competitor_1_period_2_old_result}:{self.competitor_2_period_2_old_result}|1", "won")
                    self.append_resolved_games(f"main|2. Half Next Goal - Current score: {self.competitor_1_period_2_old_result}:{self.competitor_2_period_2_old_result}|2", "lost")
                    self.append_resolved_games(f"main|2. Half Next Goal - Current score: {self.competitor_1_period_2_old_result}:{self.competitor_2_period_2_old_result}|no more goals", "lost")


            if self.competitor_1_result > 0 and self.competitor_2_result > 0:
                self.append_resolved_games(
                        f"main|Both Teams to Score|yes",
                        "won"
                    )
                self.append_resolved_games(
                        f"main|Both Teams to Score|no",
                        "lost"
                    )

            self.append_resolved_games(
                f"main|Total Goals ({complete_result - 0.5})|over",
                "won"
                )
            self.append_resolved_games(
                f"main|Total Goals ({complete_result - 0.5})|under",
                "lost"
            )
            if self.competitor_1_period_2_result != self.competitor_1_period_2_old_result or self.competitor_2_period_2_old_result != self.competitor_2_period_2_result:
                self.append_resolved_games(
                    f"main|1. Half Total Goals ({self.competitor_1_period_1_result + self.competitor_2_period_1_result - 0.5})|over",
                    "won"
                )
                self.append_resolved_games(
                    f"main|1. Half Total Goals ({self.competitor_1_period_1_result + self.competitor_2_period_1_result - 0.5})|under",
                    "lost"
                )

            if self.competitor_1_result != self.competitor_1_old_result:
                self.append_resolved_games(f"main|Total Goals Team 1 ({self.competitor_1_result - 0.5})|over", "won")
                self.append_resolved_games(f"main|Total Goals Team 1 ({self.competitor_1_result - 0.5})|under","lost")
            if self.competitor_2_result != self.competitor_2_old_result:
                self.append_resolved_games(f"main|Total Goals Team 2 ({self.competitor_2_result - 0.5})|over", "won")
                self.append_resolved_games(f"main|Total Goals Team 2 ({self.competitor_2_result - 0.5})|under", "lost")

            if self.competitor_1_period_1_result != self.competitor_1_period_1_old_result:
                self.append_resolved_games(f"main|1. Half Total Goals Team 1 ({self.competitor_1_period_1_result - 0.5})|over", "won")
                self.append_resolved_games(f"main|1. Half Total Goals Team 1 ({self.competitor_1_period_1_result - 0.5})|under","lost")
            if self.competitor_2_period_1_result != self.competitor_2_period_1_old_result:
                self.append_resolved_games(f"main|1. Half Total Goals Team 2 ({self.competitor_2_period_1_result - 0.5})|over", "won")
                self.append_resolved_games(f"main|1. Half Total Goals Team 2 ({self.competitor_2_period_1_result - 0.5})|under", "lost")

            if self.competitor_1_result != self.competitor_1_old_result and self.competitor_1_result == 3:
                self.append_resolved_games(
                    f"main|Exact Number of Goals Team 1|3+",
                    "won"
                )
                self.append_resolved_games(
                    f"main|Exact Number of Goals Team 1|2",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|Exact Number of Goals Team 1|1",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|Exact Number of Goals Team 1|0",
                    "lost"
                )

            if self.competitor_2_result != self.competitor_2_old_result and self.competitor_2_result == 3:
                self.append_resolved_games(
                    f"main|Exact Number of Goals Team 2|3+",
                    "won"
                )
                self.append_resolved_games(
                    f"main|Exact Number of Goals Team 2|2",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|Exact Number of Goals Team 2|1",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|Exact Number of Goals Team 2|0",
                    "lost"
                )
        else:
            return


    def resolve_ended_game(self):
        self.resolve_first_half()
        self._game_double_chance()
        self._game_2_half_total_goals()
        self._game_2_half_double_chance()
        self._game_total_over_under()
        self._game_second_half_result()
        self._game_both_teams_to_score()
        self._game_correct_score()
        self._game_handicap()
        self._game_handicap_2_half()
        self._game_exact_goals()
        self._game_exact_goals_comp1()
        self._game_exact_goals_comp2()
        self._game_over_under_home()
        self._game_over_under_away()
        self._game_any_team_win()
        self._game_home_win()
        self._game_away_win()
        self._game_match_results_and_both_teams_to_score()
        self._game_double_chance_and_total_goals()
        self._game_double_chance_and_both_teams_to_score()
        self._game_draw_no_bet()
        self._game_total_even_odd()
        self._game_draw_no_bet_2_half()
        self._game_which_team_wins_rest()
        self._game_gg_second_half()
        self._game_team_1_more_goals_which_half()
        self._game_matchbet_2_half_yes()
        self._game_matchbet_2_half_totals()
        self._game_endnextgoal()
        self._game_corners_even_odd()

        complete_result = self.competitor_1_result + self.competitor_2_result

        if self.competitor_1_result > self.competitor_2_result:
            self.append_resolved_games(
                    f"main|Final Result|1",
                    "won"
                )
            self.append_resolved_games(
                    f"main|Final Result|2",
                    "lost"
                )
            self.append_resolved_games(
                    f"main|Final Result|draw",
                    "lost"
                )
        elif self.competitor_1_result < self.competitor_2_result:
            self.append_resolved_games(
                    f"main|Final Result|2",
                    "won"
                )
            self.append_resolved_games(
                    f"main|Final Result|1",
                    "lost"
                )
            self.append_resolved_games(
                    f"main|Final Result|draw",
                    "lost"
                )
        else:
            self.append_resolved_games(
                    f"main|Final Result|2",
                    "lost"
                )
            self.append_resolved_games(
                    f"main|Final Result|1",
                    "lost"
                )
            self.append_resolved_games(
                    f"main|Final Result|draw",
                    "won"
                )

        for total in range(0, 10, 1):
            if complete_result > (total + 0.5):
                self.append_resolved_games(
                    f"main|Total Goals ({total+0.5})|over",
                    "won"
                    )
                self.append_resolved_games(
                    f"main|Total Goals ({total + 0.5})|under",
                    "lost"
                )
            else:
                self.append_resolved_games(
                    f"main|Total Goals ({total + 0.5})|over",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|Total Goals ({total + 0.5})|under",
                    "won"
                )
            if total <= 3:
                if total == self.competitor_1_result:
                    if total == 3:
                        self.append_resolved_games(
                        f"main|Total Exact Number of Goals Team 1|{total}+",
                        "won"
                        )
                    else:
                        self.append_resolved_games(
                        f"main|Total Exact Number of Goals Team 1|{total}",
                        "won"
                        )
                else:
                    if total == 3:
                        self.append_resolved_games(
                        f"main|Total Exact Number of Goals Team 1|{total}+",
                        "lost"
                        )
                    else:
                        self.append_resolved_games(
                        f"main|Total Exact Number of Goals Team 1|{total}",
                        "lost"
                        )

                if total == self.competitor_2_result:
                    if total == 3:
                        self.append_resolved_games(
                        f"main|Total Exact Number of Goals Team 2|{total}+",
                        "won"
                        )
                    else:
                        self.append_resolved_games(
                        f"main|Total Exact Number of Goals Team 2|{total}",
                        "won"
                        )
                else:
                    if total == 3:
                        self.append_resolved_games(
                        f"main|Total Exact Number of Goals Team 2|{total}+",
                        "lost"
                        )
                    else:
                        self.append_resolved_games(
                        f"main|Total Exact Number of Goals Team 2|{total}",
                        "lost"
                        )

            if self.competitor_2_result > total:
                self.append_resolved_games(
                    f"main|Total Goals Team 2 ({total + 0.5})|over",
                    "won"
                    )
                self.append_resolved_games(
                    f"main|Total Goals Team 2 ({total + 0.5})|under",
                    "lost"
                )
            else:
                self.append_resolved_games(
                    f"main|Total Goals Team 2 ({total + 0.5})|over",
                    "lost"
                    )
                self.append_resolved_games(
                    f"main|Total Goals Team 2 ({total + 0.5})|under",
                    "won"
                )

            if self.competitor_1_result > total:
                self.append_resolved_games(
                    f"main|Total Goals Team 1 ({total + 0.5})|over",
                    "won"
                    )
                self.append_resolved_games(
                    f"main|Total Goals Team 1 ({total + 0.5})|under",
                    "lost"
                )
            else:
                self.append_resolved_games(
                    f"main|Total Goals Team 1 ({total + 0.5})|over",
                    "lost"
                    )
                self.append_resolved_games(
                    f"main|Total Goals Team 1 ({total + 0.5})|under",
                    "won"
                )


        if self.competitor_1_result != self.competitor_1_old_result and self.competitor_1_result == 3:
            self.append_resolved_games(
                f"main|Exact Number of Goals Team 1|3+",
                "won"
            )
            self.append_resolved_games(
                f"main|Exact Number of Goals Team 1|2",
                "lost"
            )
            self.append_resolved_games(
                f"main|Exact Number of Goals Team 1|1",
                "lost"
            )
            self.append_resolved_games(
                f"main|Exact Number of Goals Team 1|0",
                "lost"
            )

        if self.competitor_2_result != self.competitor_2_old_result and self.competitor_2_result == 3:
            self.append_resolved_games(
                f"main|Exact Number of Goals Team 2|3+",
                "won"
            )
            self.append_resolved_games(
                f"main|Exact Number of Goals Team 2|2",
                "lost"
            )
            self.append_resolved_games(
                f"main|Exact Number of Goals Team 2|1",
                "lost"
            )
            self.append_resolved_games(
                f"main|Exact Number of Goals Team 2|0",
                "lost"
            )

    def _game_endnextgoal(self):
        self.append_resolved_games(f"main|Next goal - Current score: {self.competitor_1_old_result}:{self.competitor_2_old_result}|2","lost")
        self.append_resolved_games(f"main|Next goal - Current score: {self.competitor_1_old_result}:{self.competitor_2_old_result}|1","lost")
        self.append_resolved_games(f"main|Next goal - Current score: {self.competitor_1_old_result}:{self.competitor_2_old_result}|no more goals","won")

        self.append_resolved_games(f"main|2. Half Next Goal - Current score: {self.competitor_1_period_2_old_result}:{self.competitor_2_period_2_old_result}|2", "lost")
        self.append_resolved_games(f"main|2. Half Next Goal - Current score: {self.competitor_1_period_2_old_result}:{self.competitor_2_period_2_old_result}|1", "lost")
        self.append_resolved_games(f"main|2. Half Next Goal - Current score: {self.competitor_1_period_2_old_result}:{self.competitor_2_period_2_old_result}|no more goals", "won")

    def _game_double_chance(self):

        if self.competitor_1_result >= self.competitor_2_result:
            self.append_resolved_games(
                "main|Double Chance|1X",
                "won"
            )
        if self.competitor_1_result < self.competitor_2_result:
            self.append_resolved_games(
                "main|Double Chance|1X",
                "lost"
            )
        if self.competitor_1_result != self.competitor_2_result:
            self.append_resolved_games(
                "main|Double Chance|12",
                "won"
            )
        if self.competitor_1_result == self.competitor_2_result:
            self.append_resolved_games(
                "main|Double Chance|12",
                "lost"
            )
        if self.competitor_1_result <= self.competitor_2_result:
            self.append_resolved_games(
                "main|Double Chance|X2",
                "won"
            )
        if self.competitor_1_result > self.competitor_2_result:
            self.append_resolved_games(
                "main|Double Chance|X2",
                "lost"
            )
    def _game_1_half_double_chance(self):

        if self.competitor_1_period_1_result >= self.competitor_2_period_1_result:
            self.append_resolved_games(
                "main|1. Half Double Chance|1X",
                "won"
            )
        if self.competitor_1_period_1_result < self.competitor_2_period_1_result:
            self.append_resolved_games(
                "main|1. Half Double Chance|1X",
                "lost"
            )
        if self.competitor_1_period_1_result != self.competitor_2_period_1_result:
            self.append_resolved_games(
                "main|1. Half Double Chance|12",
                "won"
            )
        if self.competitor_1_period_1_result == self.competitor_2_period_1_result:
            self.append_resolved_games(
                "main|1. Half Double Chance|12",
                "lost"
            )
        if self.competitor_1_period_1_result <= self.competitor_2_period_1_result:
            self.append_resolved_games(
                "main|1. Half Double Chance|X2",
                "won"
            )
        if self.competitor_1_period_1_result > self.competitor_2_period_1_result:
            self.append_resolved_games(
                "main|1. Half Double Chance|X2",
                "lost"
            )
    def _game_2_half_total_goals(self):
        for total in range(0, 10, 1):
            if self.competitor_2_period_2_result > total:
                self.append_resolved_games(
                    f"main|2. Half Total Goals Team 2 ({total + 0.5})|over",
                    "won"
                    )
                self.append_resolved_games(
                    f"main|2. Half Total Goals Team 2 ({total + 0.5})|under",
                    "lost"
                )
            else:
                self.append_resolved_games(
                    f"main|2. Half Total Goals Team 2 ({total + 0.5})|over",
                    "lost"
                    )
                self.append_resolved_games(
                    f"main|2. Half Total Goals Team 2 ({total + 0.5})|under",
                    "won"
                )

            if self.competitor_1_period_2_result > total:
                self.append_resolved_games(
                    f"main|2. Half Total Goals Team 1 ({total + 0.5})|over",
                    "won"
                    )
                self.append_resolved_games(
                    f"main|2. Half Total Goals Team 1 ({total + 0.5})|under",
                    "lost"
                )
            else:
                self.append_resolved_games(
                    f"main|2. Half Total Goals Team 1 ({total + 0.5})|over",
                    "lost"
                    )
                self.append_resolved_games(
                    f"main|2. Half Total Goals Team 1 ({total + 0.5})|under",
                    "won"
                )

            if self.competitor_1_period_2_result + self.competitor_2_period_2_result > total:
                self.append_resolved_games(
                    f"main|2. Half Total Goals ({total + 0.5})|over",
                    "won"
                    )
                self.append_resolved_games(
                    f"main|2. Half Total Goals ({total + 0.5})|under",
                    "lost"
                )
            else:
                self.append_resolved_games(
                    f"main|2. Half Total Goals ({total + 0.5})|over",
                    "lost"
                    )
                self.append_resolved_games(
                    f"main|2. Half Total Goals ({total + 0.5})|under",
                    "won"
                )
    def _game_2_half_double_chance(self):

        if self.competitor_1_period_2_result >= self.competitor_2_period_2_result:
            self.append_resolved_games(
                "main|2. Half Double Chance|1X",
                "won"
            )
        if self.competitor_1_period_2_result < self.competitor_2_period_2_result:
            self.append_resolved_games(
                "main|2. Half Double Chance|1X",
                "lost"
            )
        if self.competitor_1_period_2_result != self.competitor_2_period_2_result:
            self.append_resolved_games(
                "main|2. Half Double Chance|12",
                "won"
            )
        if self.competitor_1_period_2_result == self.competitor_2_period_2_result:
            self.append_resolved_games(
                "main|2. Half Double Chance|12",
                "lost"
            )
        if self.competitor_1_period_2_result <= self.competitor_2_period_2_result:
            self.append_resolved_games(
                "main|2. Half Double Chance|X2",
                "won"
            )
        if self.competitor_1_period_2_result > self.competitor_2_period_2_result:
            self.append_resolved_games(
                "main|2. Half Double Chance|X2",
                "lost"
            )

    def _game_total_over_under(self):
        complete_result = self.competitor_1_result + self.competitor_2_result
        for total in range(0, 10, 1):
            if complete_result > (total + 0.5):
                self.append_resolved_games(
                    f"main|O/U ({total + 0.5})|over",
                    "won"
                )
                self.append_resolved_games(
                    f"main|O/U ({total + 0.5})|under",
                    "lost"
                )
            else:
                self.append_resolved_games(
                    f"main|O/U ({total + 0.5})|over",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|O/U ({total + 0.5})|under",
                    "won"
                )

    def _game_first_half_result(self):
        if self.competitor_1_period_1_result > self.competitor_2_period_1_result:
            self.append_resolved_games(
                    f"main|1. Half Result|1",
                    "won"
                )
            self.append_resolved_games(
                    f"main|1. Half Result|2",
                    "lost"
                )
            self.append_resolved_games(
                    f"main|1. Half Result|draw",
                    "lost"
                )
        elif self.competitor_1_period_1_result < self.competitor_2_period_1_result:
            self.append_resolved_games(
                    f"main|1. Half Result|2",
                    "won"
                )
            self.append_resolved_games(
                    f"main|1. Half Result|1",
                    "lost"
                )
            self.append_resolved_games(
                    f"main|1. Half Result|draw",
                    "lost"
                )
        else:
            self.append_resolved_games(
                    f"main|1. Half Result|2",
                    "lost"
                )
            self.append_resolved_games(
                    f"main|1. Half Result|1",
                    "lost"
                )
            self.append_resolved_games(
                    f"main|1. Half Result|draw",
                    "won"
                )

    def _game_second_half_result(self):
        if self.competitor_1_period_2_result > self.competitor_2_period_2_result:
            self.append_resolved_games(
                    f"main|2. Half Result|1",
                    "won"
                )
            self.append_resolved_games(
                    f"main|2. Half Result|2",
                    "lost"
                )
            self.append_resolved_games(
                    f"main|2. Half Result|draw",
                    "lost"
                )
        elif self.competitor_1_period_2_result < self.competitor_2_period_2_result:
            self.append_resolved_games(
                    f"main|2. Half Result|2",
                    "won"
                )
            self.append_resolved_games(
                    f"main|2. Half Result|1",
                    "lost"
                )
            self.append_resolved_games(
                    f"main|2. Half Result|draw",
                    "lost"
                )
        else:
            self.append_resolved_games(
                    f"main|2. Half Result|2",
                    "lost"
                )
            self.append_resolved_games(
                    f"main|2. Half Result|1",
                    "lost"
                )
            self.append_resolved_games(
                    f"main|2. Half Result|draw",
                    "won"
                )

    def _game_both_teams_to_score(self):

        if self.competitor_1_result == 0 or self.competitor_2_result == 0:
            self.append_resolved_games(
                "main|Both Teams To Score|yes",
                "lost"
            )
            self.append_resolved_games(
                "main|Both Teams To Score|no",
                "won"
            )
        if self.competitor_1_result > 0 and self.competitor_2_result > 0:
            self.append_resolved_games(
                "main|Both Teams To Score|yes",
                "won"
            )
            self.append_resolved_games(
                "main|Both Teams To Score|no",
                "lost"
            )

    def _game_correct_score(self):

        competitor_1_result=self.competitor_1_result
        competitor_2_result=self.competitor_2_result
        pairs=[(x,y) for x in range(4) for y in range(4)]
        ft=(competitor_1_result, competitor_2_result)

        for i in pairs:
            if ft == i:
                a,b = i
                self.append_resolved_games(
                    f"main|Correct score|{a}:{b}",
                    "won"
                )
            else:
                x,y = i
                self.append_resolved_games(f"main|Correct score|{x}:{y}",
                        "lost"
                    )

    def _game_handicap(self):
        comp1_res=self.competitor_1_result
        comp2_res=self.competitor_2_result

        range_=list(x for x in range(1,6))
        for num in range_:
            if comp1_res + num > comp2_res:
                self.append_resolved_games(
                    f"main|Handicap ({num}:0)|1",
                    "won"
                )

                self.append_resolved_games(
                    f"main|Handicap ({num}:0)|2",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|Handicap ({num}:0)|draw",
                    "lost"
                )
            if comp1_res + num == comp2_res:
                self.append_resolved_games(
                    f"main|Handicap ({num}:0)|1",
                    "lost"
                )

                self.append_resolved_games(
                    f"main|Handicap ({num}:0)|2",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|Handicap ({num}:0)|draw",
                    "won"
                )
            if comp1_res + num < comp2_res:
                self.append_resolved_games(
                    f"main|Handicap ({num}:0)|1",
                    "lost"
                )

                self.append_resolved_games(
                    f"main|Handicap ({num}:0)|2",
                    "won"
                )
                self.append_resolved_games(
                    f"main|Handicap ({num}:0)|draw",
                    "lost"
                )
            if comp1_res > comp2_res + num:
                self.append_resolved_games(
                    f"main|Handicap (0:{num})|1",
                    "won"
                )

                self.append_resolved_games(
                    f"main|Handicap (0:{num})|2",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|Handicap (0:{num})|draw",
                    "lost"
                )
            if comp1_res == comp2_res + num:
                self.append_resolved_games(
                    f"main|Handicap (0:{num})|1",
                    "lost"
                )

                self.append_resolved_games(
                    f"main|Handicap (0:{num})|2",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|Handicap (0:{num})|draw",
                    "won"
                )
            if comp1_res < comp2_res + num:
                self.append_resolved_games(
                    f"main|Handicap (0:{num})|1",
                    "lost"
                )

                self.append_resolved_games(
                    f"main|Handicap (0:{num})|2",
                    "won"
                )
                self.append_resolved_games(
                    f"main|Handicap (0:{num})|draw",
                    "lost"
                )

    def _game_handicap_1_half(self):
        comp1_res=self.competitor_1_period_1_result
        comp2_res=self.competitor_2_period_1_result

        range_=list(x for x in range(1,6))
        for num in range_:
            if comp1_res + num > comp2_res:
                self.append_resolved_games(
                    f"main|Handicap for first half ({num}:0)|1",
                    "won"
                )

                self.append_resolved_games(
                    f"main|Handicap for first half ({num}:0)|2",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|Handicap for first half ({num}:0)|x",
                    "lost"
                )
            if comp1_res + num == comp2_res:
                self.append_resolved_games(
                    f"main|Handicap for first half ({num}:0)|1",
                    "lost"
                )

                self.append_resolved_games(
                    f"main|Handicap for first half ({num}:0)|2",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|Handicap for first half ({num}:0)|x",
                    "won"
                )
            if comp1_res + num < comp2_res:
                self.append_resolved_games(
                    f"main|Handicap for first half ({num}:0)|1",
                    "lost"
                )

                self.append_resolved_games(
                    f"main|Handicap for first half ({num}:0)|2",
                    "won"
                )
                self.append_resolved_games(
                    f"main|Handicap for first half ({num}:0)|x",
                    "lost"
                )
            if comp1_res > comp2_res + num:
                self.append_resolved_games(
                    f"main|Handicap for first half (0:{num})|1",
                    "won"
                )

                self.append_resolved_games(
                    f"main|Handicap for first half (0:{num})|2",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|Handicap for first half (0:{num})|x",
                    "lost"
                )
            if comp1_res == comp2_res + num:
                self.append_resolved_games(
                    f"main|Handicap for first half (0:{num})|1",
                    "lost"
                )

                self.append_resolved_games(
                    f"main|Handicap for first half (0:{num})|2",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|Handicap for first half (0:{num})|x",
                    "won"
                )
            if comp1_res < comp2_res + num:
                self.append_resolved_games(
                    f"main|Handicap for first half (0:{num})|1",
                    "lost"
                )

                self.append_resolved_games(
                    f"main|Handicap for first half (0:{num})|2",
                    "won"
                )
                self.append_resolved_games(
                    f"main|Handicap for first half (0:{num})|x",
                    "lost"
                )
    def _game_handicap_2_half(self):
        comp1_res=self.competitor_1_period_2_result
        comp2_res=self.competitor_2_period_2_result

        range_=list(x for x in range(1,6))
        for num in range_:
            if comp1_res + num > comp2_res:
                self.append_resolved_games(
                    f"main|2nd Half - Handicap ({num}:0)|1",
                    "won"
                )

                self.append_resolved_games(
                    f"main|2nd Half - Handicap ({num}:0)|2",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|2nd Half - Handicap ({num}:0)|draw",
                    "lost"
                )
            if comp1_res + num == comp2_res:
                self.append_resolved_games(
                    f"main|2nd Half - Handicap ({num}:0)|1",
                    "lost"
                )

                self.append_resolved_games(
                    f"main|2nd Half - Handicap ({num}:0)|2",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|2nd Half - Handicap ({num}:0)|draw",
                    "won"
                )
            if comp1_res + num < comp2_res:
                self.append_resolved_games(
                    f"main|2nd Half - Handicap ({num}:0)|1",
                    "lost"
                )

                self.append_resolved_games(
                    f"main|2nd Half - Handicap ({num}:0)|2",
                    "won"
                )
                self.append_resolved_games(
                    f"main|2nd Half - Handicap ({num}:0)|draw",
                    "lost"
                )
            if comp1_res > comp2_res + num:
                self.append_resolved_games(
                    f"main|2nd Half - Handicap (0:{num})|1",
                    "won"
                )

                self.append_resolved_games(
                    f"main|2nd Half - Handicap (0:{num})|2",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|2nd Half - Handicap (0:{num})|x",
                    "lost"
                )
            if comp1_res == comp2_res + num:
                self.append_resolved_games(
                    f"main|2nd Half - Handicap (0:{num})|1",
                    "lost"
                )

                self.append_resolved_games(
                    f"main|2nd Half - Handicap (0:{num})|2",
                    "lost"
                )
                self.append_resolved_games(
                    f"main|2nd Half - Handicap (0:{num})|x",
                    "won"
                )
            if comp1_res < comp2_res + num:
                self.append_resolved_games(
                    f"main|2nd Half - Handicap (0:{num})|1",
                    "lost"
                )

                self.append_resolved_games(
                    f"main|2nd Half - Handicap (0:{num})|2",
                    "won"
                )
                self.append_resolved_games(
                    f"main|2nd Half - Handicap (0:{num})|x",
                    "lost"
                )

    def _game_exact_goals(self):
        goals=[i for i in range(0,7)]
        total=self.competitor_1_result+self.competitor_2_result
        for i in goals:
            if i==total and i < 6:
                self.append_resolved_games(f"main|Exact goals|{i}","won")
                self.append_resolved_games(f"main|Exact goals|6+","lost")
            elif i != total and i < 6:
                self.append_resolved_games(f"main|Exact goals|{i}","lost")
            elif (i==total and i==6) or (total > 6):
                self.append_resolved_games(f"main|Exact goals|6+","won")

    def _game_exact_goals_comp1(self):
        goals=[i for i in range(0,4)]
        total=self.competitor_1_result
        for i in goals:
            if i==total and i < 3:
                self.append_resolved_games(f"main|Exact Number of Goals Team 1|{i} goals","won")
                self.append_resolved_games(f"main|Exact Number of Goals Team 1|3+ goals","lost")
            elif i != total and i < 3:
                self.append_resolved_games(f"main|Exact Number of Goals Team 1|{i} goals","lost")
            elif (i==total and i==3) or (total > 3):
                self.append_resolved_games(f"main|Exact Number of Goals Team 1|3+ goals","won")

    def _game_exact_goals_comp2(self):
        goals=[i for i in range(0,4)]
        total=self.competitor_2_result
        for i in goals:
            if i==total and i < 3:
                self.append_resolved_games(f"main|Exact Number of Goals Team 2|{i} goals","won")
                self.append_resolved_games(f"main|Exact Number of Goals Team 2|3+ goals","lost")
            elif i != total and i < 3:
                self.append_resolved_games(f"main|Exact Number of Goals Team 2|{i} goals","lost")
            elif (i==total and i==3) or (total > 3):
                self.append_resolved_games(f"main|Exact Number of Goals Team 2|3+ goals","won")

    def _game_over_under_home(self):
        competitor_1_result=self.competitor_1_result
        for total in range(0, 10, 1):
            if competitor_1_result > total + 0.5:

                self.append_resolved_games(
                    f"main|Team 1 Total Goals ({total + 0.5})|over",
                    "won")

            else:
                self.append_resolved_games(
                    f"main|Team 1 Total Goals ({total + 0.5})|over",
                    "lost")

            if competitor_1_result < total + 0.5:
                self.append_resolved_games(
                    f"main|Team 1 Total Goals ({total + 0.5})|under",
                    "won")
            else:
                self.append_resolved_games(
                    f"main|Team 1 Total Goals ({total + 0.5})|under",
                    "lost")


    def _game_over_under_away(self):
        competitor_2_result=self.competitor_2_result
        for total in range(0, 10, 2):
            if competitor_2_result > total + 0.5:

                self.append_resolved_games(
                    f"main|Team 2 Total Goals ({total + 0.5})|over",
                    "won")

            else:
                self.append_resolved_games(
                    f"main|Team 2 Total Goals ({total + 0.5})|over",
                    "lost")

            if competitor_2_result < total + 0.5:
                self.append_resolved_games(
                    f"main|Team 2 Total Goals ({total + 0.5})|under",
                    "won")
            else:
                self.append_resolved_games(
                    f"main|Team 2 Total Goals ({total + 0.5})|under",
                    "lost")


    def _game_any_team_win(self):
        competitor_1_result= self.competitor_1_result
        competitor_2_result= self.competitor_2_result
        if competitor_1_result>competitor_2_result or competitor_1_result<competitor_2_result:
            self.append_resolved_games("main|Any team to win|Yes","won")
        else:
            self.append_resolved_games("main|Any team to win|No","lost")

    def _game_home_win(self):
        competitor_1_result= self.competitor_1_result
        competitor_2_result= self.competitor_2_result
        if competitor_1_result > competitor_2_result:
            self.append_resolved_games("main|Team 1 to win|Yes","won")
        else:
            self.append_resolved_games("main|Team 1 to win|No","lost")

    def _game_away_win(self):
        competitor_1_result= self.competitor_1_result
        competitor_2_result= self.competitor_2_result
        if competitor_2_result>competitor_1_result:
            self.append_resolved_games("main|Team 2 to win|Yes","won")
        else:
            self.append_resolved_games("main|Team 2 to win|No","lost")


    def _game_match_results_and_both_teams_to_score(self):

        both_teams_to_score = self.competitor_1_result > 0 and self.competitor_2_result > 0
        if self.competitor_1_result > self.competitor_2_result:
            result = "1"
        elif self.competitor_1_result < self.competitor_2_result:
            result = "2"
        else:
            result = "X"
        possible_winners = ["1", "X", "2"]
        for winner in possible_winners:
            if both_teams_to_score is True:
                if winner == result:
                    self.append_resolved_games(
                        f"main|Final Result + Both Teams to Score|{winner} & gg",
                        "won"
                    )
                else:
                    self.append_resolved_games(
                        f"main|Final Result + Both Teams to Score|{winner} & gg",
                        "lost"
                    )
                self.append_resolved_games(
                    f"main|Final Result + Both Teams to Score|{winner} & ng",
                    "lost"
                )
            if both_teams_to_score is False:
                if winner == result:
                    self.append_resolved_games(
                        f"main|Final Result + Both Teams to Score|{winner} & ng",
                        "won"
                    )
                else:
                    self.append_resolved_games(
                        f"main|Final Result + Both Teams to Score|{winner} & ng",
                        "lost"
                    )
                self.append_resolved_games(
                    f"main|Final Result + Both Teams to Score|{winner} & gg",
                    "lost"
                )

    def _game_double_chance_and_total_goals(self):
        competitor_1_result = self.competitor_1_result
        competitor_2_result = self.competitor_2_result
        status = []
        if competitor_1_result >= competitor_2_result:
            status.append("1X")
        if competitor_1_result != competitor_2_result:
            status.append("12")
        if competitor_1_result <= competitor_2_result:
            status.append("X2")

        total_goals = competitor_1_result + competitor_2_result
        for score in range(0, 12):
            over = (score + 0.5) < total_goals
            under = (score + 0.5) > total_goals
            if all(["1X" in status, over is True]):
                self.append_resolved_games(f"main|Double Chance + Total Goals ({score + 0.5})|1X & over", 'won')
            else:
                self.append_resolved_games(f"main|Double Chance + Total Goals ({score + 0.5})|1X & over", 'lost')

            if all(["12" in status, over is True]):
                self.append_resolved_games(f"main|Double Chance + Total Goals ({score + 0.5})|12 & over", 'won')
            else:
                self.append_resolved_games(f"main|Double Chance + Total Goals ({score + 0.5})|12 & over", 'lost')

            if all(["X2" in status, over is True]):
                self.append_resolved_games(f"main|Double Chance + Total Goals ({score + 0.5})|X2 & over", 'won')
            else:
                self.append_resolved_games(f"main|Double Chance + Total Goals ({score + 0.5})|X2 & over", 'lost')

            if all(["1X" in status, under is True]):
                self.append_resolved_games(f"main|Double Chance + Total Goals ({score + 0.5})|1X & under", 'won')
            else:
                self.append_resolved_games(f"main|Double Chance + Total Goals ({score + 0.5})|1X & under", 'lost')

            if all(["12" in status, under is True]):
                self.append_resolved_games(f"main|Double Chance + Total Goals ({score + 0.5})|12 & under", 'won')
            else:
                self.append_resolved_games(f"main|Double Chance + Total Goals ({score + 0.5})|12 & under", 'lost')

            if all(["X2" in status, under is True]):
                self.append_resolved_games(f"main|Double Chance + Total Goals ({score + 0.5})|X2 & under", 'won')
            else:
                self.append_resolved_games(f"main|Double Chance + Total Goals ({score + 0.5})|X2 & under", 'lost')

    def _game_double_chance_and_both_teams_to_score(self):

        competitor_1_result = self.competitor_1_result
        competitor_2_result = self.competitor_2_result
        both_to_score = competitor_1_result > 0 and competitor_2_result > 0
        final_result = competitor_1_result + competitor_2_result
        only_one_score = competitor_1_result > 0 or competitor_2_result > 0
        no_one_scores = competitor_1_result == 0 and competitor_2_result == 0

        if competitor_1_result > 0 and competitor_2_result > 0:
            if competitor_1_result >= competitor_2_result:
                self.append_resolved_games(
                    "main|Double Chance + Both Teams to Score|1 & gg",
                    "won"
                )
                self.append_resolved_games(
                    "main|Double Chance + Both Teams to Score|1 & ng",
                    "lost"
                )
            else:
                self.append_resolved_games(
                    "main|Double Chance + Both Teams to Score|1 & gg",
                    "lost"
                )
                self.append_resolved_games(
                    "main|Double Chance + Both Teams to Score|1 & ng",
                    "lost"
                )

            if competitor_1_result < competitor_2_result or competitor_1_result == competitor_2_result:
                self.append_resolved_games(
                    "main|Double Chance + Both Teams to Score|2 & gg",
                    "won"
                )
                self.append_resolved_games(
                    "main|Double Chance + Both Teams to Score|2 & ng",
                    "lost"
                )
            else:
                self.append_resolved_games(
                    "main|Double Chance + Both Teams to Score|2 & gg",
                    "lost"
                )
                self.append_resolved_games(
                    "main|Double Chance + Both Teams to Score|2 & ng",
                    "lost"
                )

            if competitor_1_result > competitor_2_result or competitor_1_result < competitor_2_result:
                self.append_resolved_games(
                    "main|Double Chance + Both Teams to Score|X & gg",
                    "won"
                )
                self.append_resolved_games(
                    "main|Double Chance + Both Teams to Score|X & ng",
                    "lost"
                )
            else:
                self.append_resolved_games(
                    "main|Double Chance + Both Teams to Score|X & gg",
                    "lost"
                )
                self.append_resolved_games(
                    "main|Double Chance + Both Teams to Score|X & ng",
                    "lost"
                )
        else:
            if only_one_score and competitor_1_result>competitor_2_result:
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|1 & gg",
                "lost"
            )
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|1 & ng",
                "won"
            )
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|2 & gg",
                "lost"
            )
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|2 & ng",
                "lost"
            )
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|X & gg",
                "lost"
            )
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|X & ng",
                "won"
            )

            elif only_one_score and competitor_1_result<competitor_2_result:
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|1 & gg",
                "lost"
            )
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|1 & ng",
                "lost"
            )

                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|2 & gg",
                "lost"
            )
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|2 & ng",
                "won"
            )
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|X & gg",
                "lost"
            )
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|X & ng",
                "won"
            )

            elif no_one_scores:
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|1 & gg",
                "lost"
            )
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|1 & ng",
                "won"
            )

                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|2 & gg",
                "lost"
            )
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|2 & ng",
                "won"
            )
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|X & gg",
                "lost"
            )
                self.append_resolved_games(
                "main|Double Chance + Both Teams to Score|X & ng",
                "lost"
            )

    def _game_draw_no_bet(self):
        competitor_1_result = self.competitor_1_result
        competitor_2_result = self.competitor_2_result

        if competitor_1_result>competitor_2_result:
            self.append_resolved_games("main|Draw no bet|1","won")
            self.append_resolved_games("main|Draw no bet|2","lost")
        elif competitor_1_result<competitor_2_result:
            self.append_resolved_games("main|Draw no bet|1","lost")
            self.append_resolved_games("main|Draw no bet|2","won")
        else:
            self.append_resolved_games("main|Draw no bet|1","canceled")
            self.append_resolved_games("main|Draw no bet|2","canceled")

    def _game_total_even_odd(self):
        complete_results = self.competitor_1_result + self.competitor_2_result

        if complete_results % 2 == 0:
            self.append_resolved_games(
                "main|Total Goals - Even/Odd|even",
                "won"
            )
            self.append_resolved_games(
                "main|Total Goals - Even/Odd|odd",
                "lost"
            )
        else:
            self.append_resolved_games(
                "main|Total Goals - Even/Odd|even",
                "lost"
            )
            self.append_resolved_games(
                "main|Total Goals - Even/Odd|odd",
                "won"
            )

    def _game_corners_even_odd(self):
        if self.corners % 2 == 0:
            self.append_resolved_games(
                "main|Total Corners - Even/Odd|even",
                "won"
            )
            self.append_resolved_games(
                "main|Total Corners - Even/Odd|odd",
                "lost"
            )
        else:
            self.append_resolved_games(
                "main|Total Corners - Even/Odd|even",
                "lost"
            )
            self.append_resolved_games(
                "main|Total Corners - Even/Odd|odd",
                "won"
            )


    def _game_draw_no_bet_1_half(self):

        if self.competitor_1_period_1_result>self.competitor_2_period_1_result:
            self.append_resolved_games("main|Draw No Bet First Half|1","won")
            self.append_resolved_games("main|Draw No Bet First Half|2","lost")
        elif self.competitor_1_period_1_result<self.competitor_2_period_1_result:
            self.append_resolved_games("main|Draw No Bet First Half|1","lost")
            self.append_resolved_games("main|Draw No Bet First Half|2","won")
        else:
            self.append_resolved_games("main|Draw No Bet First Half|1","canceled")
            self.append_resolved_games("main|Draw No Bet First Half|2","canceled")

    def _game_draw_no_bet_2_half(self):

        if self.competitor_1_period_2_result>self.competitor_2_period_2_result:
            self.append_resolved_games("main|Draw No Bet Second Half|1","won")
            self.append_resolved_games("main|Draw No Bet Second Half|2","lost")
        elif self.competitor_1_period_2_result<self.competitor_2_period_2_result:
            self.append_resolved_games("main|Draw No Bet Second Half|1","lost")
            self.append_resolved_games("main|Draw No Bet Second Half|2","won")
        else:
            self.append_resolved_games("main|Draw No Bet Second Half|1","canceled")
            self.append_resolved_games("main|Draw No Bet Second Half|2","canceled")

    def _game_which_team_wins_rest(self):
        competitor_1_result = self.competitor_1_result
        competitor_2_result = self.competitor_2_result
        for i in range(0,competitor_1_result+1):
            for j in range(0,competitor_2_result+1):
                if competitor_1_result - i > competitor_2_result - j:
                    self.append_resolved_games(f"main|To Win the Rest of the Match ( {i}:{j} )|1","won")
                    self.append_resolved_games(f"main|To Win the Rest of the Match ( {i}:{j} )|draw","lost")
                    self.append_resolved_games(f"main|To Win the Rest of the Match ( {i}:{j} )|2","lost")
                elif competitor_1_result - i < competitor_2_result - j:
                    self.append_resolved_games(f"main|To Win the Rest of the Match ( {i}:{j} )|1","lost")
                    self.append_resolved_games(f"main|To Win the Rest of the Match ( {i}:{j} )|draw","lost")
                    self.append_resolved_games(f"main|To Win the Rest of the Match ( {i}:{j} )|2","won")
                else:
                    self.append_resolved_games(f"main|To Win the Rest of the Match ( {i}:{j} )|1","lost")
                    self.append_resolved_games(f"main|To Win the Rest of the Match ( {i}:{j} )|draw","won")
                    self.append_resolved_games(f"main|To Win the Rest of the Match ( {i}:{j} )|2","lost")

    def _game_which_team_wins_rest_of_1_half(self):
        for i in range(0,self.competitor_1_period_1_result+1):
            for j in range(0,self.competitor_2_period_1_result+1):
                if self.competitor_1_period_1_result - i > self.competitor_2_period_1_result - j:
                    self.append_resolved_games(f"main|To Win the Rest of the 1. Half ( {i}:{j} )|1","won")
                    self.append_resolved_games(f"main|To Win the Rest of the 1. Half ( {i}:{j} )|draw","lost")
                    self.append_resolved_games(f"main|To Win the Rest of the 1. Half ( {i}:{j} )|2","lost")
                elif self.competitor_1_period_1_result - i < self.competitor_2_period_1_result - j:
                    self.append_resolved_games(f"main|To Win the Rest of the 1. Half ( {i}:{j} )|1","lost")
                    self.append_resolved_games(f"main|To Win the Rest of the 1. Half ( {i}:{j} )|draw","lost")
                    self.append_resolved_games(f"main|To Win the Rest of the 1. Half ( {i}:{j} )|2","won")
                else:
                    self.append_resolved_games(f"main|To Win the Rest of the 1. Half ( {i}:{j} )|1","lost")
                    self.append_resolved_games(f"main|To Win the Rest of the 1. Half ( {i}:{j} )|draw","won")
                    self.append_resolved_games(f"main|To Win the Rest of the 1. Half ( {i}:{j} )|2","lost")

    def _game_gg_second_half(self):
        if self.competitor_1_period_2_result > 0 and self.competitor_2_period_2_result > 0:
            self.append_resolved_games("main|Second Half Both Teams to Score|yes", "won")
            self.append_resolved_games("main|Second Half Both Teams to Score|no", "won")
        else:
            self.append_resolved_games("main|Second Half Both Teams to Score|no", "won")
            self.append_resolved_games("main|Second Half Both Teams to Score|yes", "lost")

    def _game_team_1_more_goals_which_half(self):
        period_2_res = self.competitor_1_period_2_result + self.competitor_2_period_2_result
        period_1_res = self.competitor_1_period_1_result + self.competitor_2_period_1_result

        if period_1_res > period_2_res:
            self.append_resolved_games("main|Highest Scoring Half|1. half", "won")
        else:
            self.append_resolved_games("main|Highest Scoring Half|1. half", "lost")

        if period_1_res == period_2_res:
            self.append_resolved_games("main|Highest Scoring Half|equals", "won")
        else:
            self.append_resolved_games("main|Highest Scoring Half|equals", "lost")

        if period_1_res < period_2_res:
            self.append_resolved_games("main|Highest Scoring Half|2. half", "won")
        else:
            self.append_resolved_games("main|Highest Scoring Half|2. half", "lost")

    def _game_matchbet_2_half_yes(self):
        both_teams_to_score = self.competitor_1_period_2_result > 0 and self.competitor_2_period_2_result > 0
        if self.competitor_1_period_2_result > self.competitor_2_period_2_result:
            result = "home"
        elif self.competitor_1_period_2_result < self.competitor_2_period_2_result:
            result = "away"
        else:
            result = 'draw'
        possible_winners = ["home", "draw", "away"]
        for winner in possible_winners:
            if both_teams_to_score is True:
                if winner == result:
                    self.append_resolved_games(
                        f"main|2nd Half - Matchbet and both teams to score|{winner} and yes",
                        "won"
                    )
                else:
                    self.append_resolved_games(
                        f"main|2nd Half - Matchbet and both teams to score|{winner} and yes",
                        "lost"
                    )
                self.append_resolved_games(
                    f"main|2nd Half - Matchbet and both teams to score|{winner} and no",
                    "lost"
                )
            if both_teams_to_score is False:
                if winner == result:
                    self.append_resolved_games(
                        f"main|2nd Half - Matchbet and both teams to score|{winner} and no",
                        "won"
                    )
                else:
                    self.append_resolved_games(
                        f"main|2nd Half - Matchbet and both teams to score|{winner} and no",
                        "lost"
                    )
                self.append_resolved_games(
                    f"main|2nd Half - Matchbet and both teams to score|{winner} and yes",
                    "lost"
                )

    def _game_matchbet_2_half_totals(self):
        if self.competitor_1_period_2_result > self.competitor_2_period_2_result:
            result = "home"
        elif self.competitor_1_period_2_result < self.competitor_2_period_2_result:
            result = "away"
        else:
            result = 'draw'
        possible_winners = ["home", "draw", "away"]
        for total in range(0, 4, 1):
            over = (self.competitor_1_period_2_result + self.competitor_2_period_2_result) > total + 0.5
            under = (self.competitor_1_period_2_result + self.competitor_2_period_2_result) < total + 0.5
            for winner in possible_winners:
                if all([winner == result, over is True]):
                    self.append_resolved_games(
                        f"main|2nd Half - Matchbet and Totals ({total+0.5})|{winner} and over",
                        "won"
                    )
                else:
                    self.append_resolved_games(
                        f"main|2nd Half - Matchbet and Totals ({total+0.5})|{winner} and over",
                        "lost"
                    )
                if all([winner == result, under is True]):
                    self.append_resolved_games(
                        f"main|2nd Half - Matchbet and Totals ({total+0.5})|{winner} and under",
                        "won"
                    )
                else:
                    self.append_resolved_games(
                        f"main|2nd Half - Matchbet and Totals ({total+0.5})|{winner} and under",
                        "lost"
                    )

    def _game_matchbet_1_half(self):
        both_teams_to_score = self.competitor_1_period_1_result > 0 and self.competitor_2_period_1_result > 0
        if self.competitor_1_period_1_result > self.competitor_2_period_1_result:
            result = "1"
        elif self.competitor_1_period_1_result < self.competitor_2_period_1_result:
            result = "2"
        else:
            result = "X"
        possible_winners = ["1", "X", "away"]
        for winner in possible_winners:
            if both_teams_to_score is True:
                if winner == result:
                    self.append_resolved_games(
                        f"main|1. Half Result + 1. Half Both Teams To Score|{winner}fh & 1gg",
                        "won"
                    )
                else:
                    self.append_resolved_games(
                        f"main|1. Half Result + 1. Half Both Teams To Score|{winner}fh & 1gg",
                        "lost"
                    )
                self.append_resolved_games(
                    f"main|1. Half Result + 1. Half Both Teams To Score|{winner}fh & 1ng",
                    "lost"
                )
            if both_teams_to_score is False:
                if winner == result:
                    self.append_resolved_games(
                        f"main|1. Half Result + 1. Half Both Teams To Score|{winner}fh & 1ng",
                        "won"
                    )
                else:
                    self.append_resolved_games(
                        f"main|1. Half Result + 1. Half Both Teams To Score|{winner}fh & 1ng",
                        "lost"
                    )
                self.append_resolved_games(
                    f"main|1. Half Result + 1. Half Both Teams To Score|{winner}fh & 1gg",
                    "lost"
                )

    def _game_matchbet_1_half_totals_ou(self):
        if self.competitor_1_period_1_result > self.competitor_2_period_1_result:
            result = "1"
        elif self.competitor_1_period_1_result < self.competitor_2_period_1_result:
            result = "2"
        else:
            result = "X"
        possible_winners = ["1", "2", "X"]
        for total in range(0, 4, 1):
            over = (self.competitor_1_period_1_result + self.competitor_2_period_1_result) > total + 0.5
            under = (self.competitor_1_period_1_result + self.competitor_2_period_1_result) < total + 0.5
            for winner in possible_winners:
                if all([winner == result, over is True]):
                    self.append_resolved_games(
                        f"main|1. Half Result + 1. Half Total Goals ({total+0.5})|{winner}fh & over",
                        "won"
                    )
                else:
                    self.append_resolved_games(
                        f"main|1. Half Result + 1. Half Total Goals ({total+0.5})|{winner}fh & over",
                        "lost"
                    )
                if all([winner == result, under is True]):
                    self.append_resolved_games(
                        f"main|1. Half Result + 1. Half Total Goals ({total+0.5})|{winner}fh & under",
                        "won"
                    )
                else:
                    self.append_resolved_games(
                        f"main|1. Half Result + 1. Half Total Goals ({total+0.5})|{winner}fh & under",
                        "lost"
                    )
    def _game_1_half_totals(self):
        for total in range(0, 10, 1):
            if self.competitor_2_period_1_result > total:
                self.append_resolved_games(
                    f"main|1. Half Total Goals Team 2 ({total + 0.5})|over",
                    "won"
                    )
                self.append_resolved_games(
                    f"main|1. Half Total Goals Team 2 ({total + 0.5})|under",
                    "lost"
                )
            else:
                self.append_resolved_games(
                    f"main|1. Half Total Goals Team 2 ({total + 0.5})|over",
                    "lost"
                    )
                self.append_resolved_games(
                    f"main|1. Half Total Goals Team 2 ({total + 0.5})|under",
                    "won"
                )

            if self.competitor_1_period_1_result > total:
                self.append_resolved_games(
                    f"main|1. Half Total Goals Team 1 ({total + 0.5})|over",
                    "won"
                    )
                self.append_resolved_games(
                    f"main|1. Half Total Goals Team 1 ({total + 0.5})|under",
                    "lost"
                )
            else:
                self.append_resolved_games(
                    f"main|1. Half Total Goals Team 1 ({total + 0.5})|over",
                    "lost"
                    )
                self.append_resolved_games(
                    f"main|1. Half Total Goals Team 1 ({total + 0.5})|under",
                    "won"
                )

            if self.competitor_1_period_1_result + self.competitor_2_period_1_result > total:
                self.append_resolved_games(
                    f"main|1. Half Total Goals ({total + 0.5})|over",
                    "won"
                    )
                self.append_resolved_games(
                    f"main|1. Half Total Goals ({total + 0.5})|under",
                    "lost"
                )
            else:
                self.append_resolved_games(
                    f"main|1. Half Total Goals ({total + 0.5})|over",
                    "lost"
                    )
                self.append_resolved_games(
                    f"main|1. Half Total Goals ({total + 0.5})|under",
                    "won"
                )

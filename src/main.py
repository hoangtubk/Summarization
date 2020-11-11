import json
import re

def get_all_team():
    """
    Lay danh sach doi bong trong tap train
    :return:
    """
    team = []
    with open("../input/train.jsonl", "r", encoding="utf-8") as fr:
        lines = fr.readlines()
        for line in lines:
            data = json.loads(line, encoding="utf-8")
            team_1 = data["match_summary"]["players"]["team1"].strip()
            team_2 = data["match_summary"]["players"]["team2"].strip()
            if team_1 not in team:
                team.append(team_1)
            if team_2 not in team:
                team.append(team_2)

    return team

def get_all_line_score_board():
    """
    Lay danh sach cac ti so trong tap train
    :return:
    """
    line_score_board = []
    with open("../input/train.jsonl", "r", encoding="utf-8") as fr:
        lines = fr.readlines()
        for line in lines:
            data = str(json.loads(line, encoding="utf-8"))
            score_boards = re.findall("\\s\\d-\\d\\s", data)
            lst_score_boards = []
            for score_board in score_boards:
                if score_board.strip() not in lst_score_boards:
                    lst_score_boards.append(score_board.strip())
            line_score_board.append(lst_score_boards)

    return line_score_board

if __name__ == '__main__':
    team = get_all_team()
    line_score_board = get_all_line_score_board()
    print(len(line_score_board))
    print(line_score_board)
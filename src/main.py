import json
import re
from bs4 import BeautifulSoup
import copy

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

def get_list_pragraph_tag(tag):
    """
    lay list paragraph chứa tag
    :param tag:
    :return:
    """
    print("Tag: ", tag)
    list_paragraph = []
    with open("../input/train.jsonl", "r", encoding="utf-8") as fr:
        lines = fr.readlines()
        for line in lines:
            data = json.loads(line, encoding="utf-8")
            for html in data["html_annotation"]:
                soup = BeautifulSoup(html, "html.parser")
                events = soup.find_all("span", {"class": "tag"})
                for e in events:
                    if tag in e["data"]:
                        print(e.text)
                        list_paragraph.append(e.text)
                    # print("event_type:", e["data"])
                    # print("event_id:", e["event_id"])
                    # print("text:", e.text)
    return list_paragraph

def get_list_time_from_parag(text):
    """
    Lấy danh sách thời gian từ câu
    :param text:
    :return:
    """
    list_time = []
    time_pattern_1 = "((phút thứ)|phút)\s(\d{1,2})"
    temp_1 = re.findall(time_pattern_1, text.lower())
    for time in temp_1:
        list_time.append(time[2])
    time_pattern_2 = "(\d{1,2})('|\")"
    temp_2 = re.findall(time_pattern_2, text.lower())
    for time in temp_2:
        list_time.append(time[0])

    return list_time

def get_list_name_from_parag(text):
    """
    Lấy danh sách tên người trong câu
    :param text:
    :return:
    """
    # Loại bỏ ký tự đặc biệt
    text = re.sub('[^A-Za-z0-9\s]+', '', text)
    # Bổ sung dấu cách để bắt từ cuối cùng
    text = text + " ."
    text_word = text.split()
    temp = ""
    list_name = []
    for i in range(0, len(text_word)):
        last_text = text_word[i]
        if temp != "":
            list_name.append(temp.strip())
            temp = ""
        if len(list_name) != 0 and last_text in list_name[-1]:
            continue
        if text_word[i][0].isupper():
            temp = temp + " " + copy.deepcopy(text_word[i])
            for j in range(i + 1, len(text_word)):
                if text_word[j][0].isupper():
                    temp = temp + " " + copy.deepcopy(text_word[j])
                    i = j
                else:
                    break

    return list_name

def get_card_info():
    """
    # --------------------------------------
    # Bắt thẻ đỏ / thẻ vàng:
    # --------------------------------------
    :return:
    """
    with open("../input/train.jsonl", "r", encoding="utf-8") as fr:
        lines = fr.readlines()
        for line in lines:
            data = json.loads(line, encoding="utf-8")
            for body in data["original_doc"]["_source"]["body"]:
                text = body["text"]
                # Bắt pattern chứa thông tin thẻ
                if re.search("(thẻ đỏ)|(thẻ vàng)", text.lower()) == None:
                    continue
                # Bắt pattern chứa thông tin thời gian
                list_time = get_list_time_from_parag(text)
                print(list_time)
                print(text)
                # Lấy danh sách các từ bắt đầu bằng chữ in hoa
                list_name = get_list_name_from_parag(text)
                print(list_name)

if __name__ == '__main__':


    team = get_all_team()
    line_score_board = get_all_line_score_board()
    # lay list paragraph chứa tag:
    list_tag = get_list_pragraph_tag("card_info")
    # list_tag = get_list_pragraph_tag("substitution")
    print(len(list_tag))

    # for tag in list_tag:
    #     a = re.search("(thẻ đỏ)|(thẻ vàng)|(Thẻ vàng)|(Thẻ đỏ)", tag)
    #     if a == None:
    #         print(tag)
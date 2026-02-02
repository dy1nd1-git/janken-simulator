import sys
import random
from abc import ABC, abstractmethod
from collections import Counter

# 手の定義
GU = "グー"
CHOKI = "チョキ"
PA = "パー"
HANDS = [GU, CHOKI, PA]

def judge(h1, h2):
    """h1から見た勝敗を返す (1: 勝ち, -1: 負け, 0: アイコ)"""
    if h1 == h2:
        return 0
    if (h1 == GU and h2 == CHOKI) or \
       (h1 == CHOKI and h2 == PA) or \
       (h1 == PA and h2 == GU):
        return 1
    return -1

class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.history = []  # 自身の出した手と結果の記録

    @abstractmethod
    def next_hand(self):
        pass

    def record_result(self, my_hand, result):
        self.history.append({"hand": my_hand, "result": result})

class Nobita(Player):
    """均等にランダムに出す戦略"""
    def next_hand(self):
        return random.choice(HANDS)

class Suneo(Player):
    """勝率が最も良い手からランダムに選ぶ戦略"""
    def next_hand(self):
        # 履歴がない場合はランダム
        if not self.history:
            return random.choice(HANDS)

        win_counts = Counter()
        for h in HANDS:
            results = [record["result"] for record in self.history if record["hand"] == h]
            if not results:
                win_counts[h] = 0
                continue
            # 勝率 = 勝ち数 / その手を出した回数
            win_rate = results.count(1) / len(results)
            win_counts[h] = win_rate

        max_rate = max(win_counts.values())
        best_hands = [h for h, rate in win_counts.items() if rate == max_rate]
        return random.choice(best_hands)

def simulate(trials):
    n = Nobita("N")
    s = Suneo("S")
    
    n_wins = 0
    s_wins = 0

    for _ in range(trials):
        h_n = n.next_hand()
        h_s = s.next_hand()

        res_n = judge(h_n, h_s)
        res_s = -res_n

        n.record_result(h_n, res_n)
        s.record_result(h_s, res_s)

        if res_n == 1: n_wins += 1
        if res_s == 1: s_wins += 1

    print(f"N: {n_wins / trials * 100:.2f}%")
    print(f"S: {s_wins / trials * 100:.2f}%")

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    simulate(count)
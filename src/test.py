import sys
sys.dont_write_bytecode = True
from main import Nobita, HANDS

def test_nobita_randomness(trials=10000):
    n = Nobita("N")
    counts = {hand: 0 for hand in HANDS}
    
    for _ in range(trials):
        counts[n.next_hand()] += 1
    
    results = []
    is_all_valid = True
    
    expected_rate = 1/3
    for hand in HANDS:
        rate = counts[hand] / trials
        # 誤差1%以内か判定
        is_valid = abs(rate - expected_rate) < 0.01
        results.append(rate)
        if not is_valid:
            is_all_valid = False
            
    # 代表として1つの確率と全体の成否を出力
    print(f"{results[0]*100:.2f}% {is_all_valid}")

if __name__ == "__main__":
    test_nobita_randomness()
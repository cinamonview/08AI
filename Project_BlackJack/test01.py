import random
import platform
import matplotlib.pyplot as plt

# 1. 그래프 한글 깨짐 방지 설정
current_os = platform.system()
if current_os == 'Windows':
    plt.rc('font', family='Malgun Gothic')  # 윈도우
elif current_os == 'Darwin':
    plt.rc('font', family='AppleGothic')    # 맥
plt.rcParams['axes.unicode_minus'] = False

# 2. 덱 생성 함수
def create_deck(num_of_decks=6):
    single_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    full_deck = single_deck * num_of_decks
    random.shuffle(full_deck)
    return full_deck

# 3. 시뮬레이션 실행 함수
def run_simulation(total_games=100000):
    num_decks = 6
    deck = create_deck(num_decks)
    shuffle_threshold = len(deck) * 0.25 
    
    blackjack_count = 0
    history_list = []  # 기록을 담을 리스트
    
    for game_num in range(1, total_games + 1):
        if len(deck) < shuffle_threshold:
            deck = create_deck(num_decks)
            
        card1 = deck.pop()
        card2 = deck.pop()
        
        if (card1 == 11 and card2 == 10) or (card1 == 10 and card2 == 11):
            blackjack_count += 1
            
        # 1000판마다 누적 확률을 기록
        if game_num % 1000 == 0:
            current_prob = (blackjack_count / game_num) * 100
            history_list.append((game_num, current_prob))
            
    final_prob = (blackjack_count / total_games) * 100
    print(f"=== 시뮬레이션 결과 ===")
    print(f"총 실행 게임 수: {total_games:,}판")
    print(f"블랙잭 등장 횟수: {blackjack_count:,}번")
    print(f"실험적 블랙잭 확률: {final_prob:.4f}%")
    
    return history_list, final_prob

# ========================================================
# 4. 여기서 실제로 함수를 실행하여 데이터를 뽑아냅니다!
# ========================================================
game_history, final_probability = run_simulation(100000)

# ========================================================
# 5. 추출한 game_history 변수를 사용해 그래프를 그립니다.
# ========================================================
x_games, y_probs = zip(*game_history)  # 데이터를 x축(판수), y축(확률)으로 분리

plt.figure(figsize=(10, 5))
plt.plot(x_games, y_probs, label='시뮬레이션 확률', color='blue', linewidth=2)

# 6덱 기준 수학적 이론값 수평선 표시 (약 4.75%)
plt.axhline(y=4.749, color='red', linestyle='--', label='수학적 이론값 (~4.75%)')

plt.title('블랙잭 확률 수렴 과정 (몬테카를로 시뮬레이션)', fontsize=14, pad=15)
plt.xlabel('게임 판수 (Number of Games)', fontsize=12)
plt.ylabel('블랙잭 확률 (%)', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=11)
plt.ylim(4.0, 5.5)  # 변동을 자세히 보기 위해 y축 범위 제한

plt.show()
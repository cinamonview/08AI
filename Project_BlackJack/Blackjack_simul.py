import random
import matplotlib.pyplot as plt

def create_deck(num_of_decks=6):
    """지정된 개수의 덱(Deck)을 합친 카드 묶음을 생성하고 섞습니다."""
    # 2~10은 그대로 점수, J, Q, K는 10점(각 4장씩 총 16장), A는 11점(우선 11로 처리)
    single_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    full_deck = single_deck * num_of_decks
    random.shuffle(full_deck)
    return full_deck

def run_simulation(total_games=100000):
    """지정한 판수만큼 블랙잭 시뮬레이션을 실행합니다."""
    num_decks = 6
    deck = create_deck(num_decks)
    
    # 카드를 새로 섞는 기준 (전체 카드의 75%를 사용했을 때)
    shuffle_threshold = len(deck) * 0.25 
    
    blackjack_count = 0
    history = []  # 시각화를 위해 게임이 진행됨에 따라 변화하는 확률 기록
    
    for game_num in range(1, total_games + 1):
        # 남아있는 카드가 부족하면 새 덱을 가져와서 섞음
        if len(deck) < shuffle_threshold:
            deck = create_deck(num_decks)
            
        # 첫 두 장의 카드를 뽑음 (pop을 사용해 덱에서 제거)
        card1 = deck.pop()
        card2 = deck.pop()
        
        # 블랙잭 확인 (A(11)와 10점짜리 카드가 동시에 나온 경우)
        if (card1 == 11 and card2 == 10) or (card1 == 10 and card2 == 11):
            blackjack_count += 1
            
        # 1000판마다 누적 확률을 기록 (그래프 그리기용)
        if game_num % 1000 == 0:
            current_prob = (blackjack_count / game_num) * 100
            history.append((game_num, current_prob))
            
    final_prob = (blackjack_count / total_games) * 100
    print(f"=== 시뮬레이션 결과 ===")
    print(f"총 실행 게임 수: {total_games:,}판")
    print(f"블랙잭 등장 횟수: {blackjack_count:,}번")
    print(f"실험적 블랙잭 확률: {final_prob:.4f}%")
    
    return history, final_prob

# 시뮬레이션 실행 (10만 번)
game_history, final_probability = run_simulation(100000)
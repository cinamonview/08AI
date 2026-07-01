import matplotlib.pyplot as plt
import platform

# 그래프에서 한글 깨짐 방지 설정
current_os = platform.system()
if current_os == 'Windows':
    plt.rc('font', family='Malgun Gothic')  # 윈도우 (맑은 고딕)
elif current_os == 'Darwin':
    plt.rc('font', family='AppleGothic')    # 맥 (애플 고딕)

# 그래프에서 마이너스 기호(-) 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

# 그래프 시각화
games, probs = zip(*game_history)

plt.figure(figsize=(10, 5))
plt.plot(games, probs, label='Simulated Probability', color='blue', linewidth=2)

# 6덱 기준 수학적 이론값 수평선 표시 (약 4.74%)
plt.axhline(y=4.749, color='red', linestyle='--', label='Theoretical Value (6-Deck: ~4.75%)')

plt.title('Blackjack Probability Convergence (Monte Carlo)', fontsize=14, pad=15)
plt.xlabel('Number of Games', fontsize=12)
plt.ylabel('Probability (%)', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=11)
plt.ylim(4.0, 5.5)  # 변화를 잘 보기 위해 y축 범위 제한

plt.show()
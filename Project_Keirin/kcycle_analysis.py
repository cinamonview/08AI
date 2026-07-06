import oracledb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 한글 깨짐 방지 설정 (Windows 환경)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# 오라클 접속 설정
db_config = {
    "user": "education",
    "password": "1234",  # 👈 본인의 오라클 비밀번호로 변경해주세요!
    "dsn": "localhost:1521/xe"
}

def plot_cyclist_win_rate():
    try:
        # 1. 오라클 DB에서 승률 통계 데이터 쿼리해오기
        connection = oracledb.connect(**db_config)
        
        query = """
        SELECT 
            c.name AS PLAYER_NAME,
            COUNT(r.race_id) AS TOTAL_RACES,
            ROUND(COUNT(CASE WHEN r.rank_result = 1 THEN 1 END) / COUNT(r.race_id) * 100, 1) AS WIN_RATE
        FROM 
            cyclist_info c
        JOIN 
            race_result r ON c.cyclist_id = r.cyclist_id
        GROUP BY 
            c.name
        ORDER BY 
            WIN_RATE DESC
        """
        
        # 2. 쿼리 결과를 판다스 데이터프레임으로 깔끔하게 변환
        df = pd.read_sql(query, con=connection)
        connection.close()
        
        if df.empty:
            print("데이터가 없습니다.")
            return

        print("📊 DB에서 성공적으로 통계를 읽어왔습니다. 그래프를 그립니다...")

        # 3. Matplotlib을 이용한 막대그래프 시각화
        plt.figure(figsize=(10, 6))
        
        # 막대그래프 그리기 (x축: 선수명, y축: 승률)
        bars = plt.bar(df['PLAYER_NAME'], df['WIN_RATE'], color='skyblue', edgecolor='black')
        
        # 각 막대 위에 실제 승률 수치 적어주기
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{yval}%", ha='center', va='bottom', fontweight='bold')
            
        # 그래프 제목 및 축 레이블 설정
        plt.title('🏁 경륜 선수별 승률 분석 (2026년 4월 데이터 기반)', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('선수 이름', fontsize=12, labelpad=10)
        plt.ylabel('승률 (%)', fontsize=12, labelpad=10)
        plt.ylim(0, 115) # y축 범위 설정 (텍스트가 안 잘리게 115까지)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # 그래프 화면에 표시!
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"❌ 시각화 중 오류 발생: {e}")

if __name__ == "__main__":
    plot_cyclist_win_rate()
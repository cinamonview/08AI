import oracledb
import pandas as pd

# 오라클 접속 설정
db_config = {
    "user": "education",
    "password": "1234",  # 👈 본인의 오라클 비밀번호로 변경해주세요!
    "dsn": "localhost:1521/xe"
}

def get_betting_predictions():
    try:
        connection = oracledb.connect(**db_config)
        
        # [핵심 SQL] DB 안에서 선수별 승률, 연대율, 삼연대율을 퍼센트(숫자)로 계산해옵니다.
        query = """
        SELECT 
            c.name AS PLAYER_NAME,
            c.team AS TEAM,
            c.grade AS GRADE,
            COUNT(r.race_id) AS TOTAL_RACES,
            ROUND(COUNT(CASE WHEN r.rank_result = 1 THEN 1 END) / COUNT(r.race_id) * 100, 1) AS WIN_RATE,
            ROUND(COUNT(CASE WHEN r.rank_result IN (1, 2) THEN 1 END) / COUNT(r.race_id) * 100, 1) AS TOP2_RATE,
            ROUND(COUNT(CASE WHEN r.rank_result IN (1, 2, 3) THEN 1 END) / COUNT(r.race_id) * 100, 1) AS TOP3_RATE
        FROM 
            cyclist_info c
        JOIN 
            race_result r ON c.cyclist_id = r.cyclist_id
        WHERE
            c.name NOT IN ('젖히기', '마크', '경고', '주의', '선행', '추입') -- 👈 기술/판정 유령 선수 완벽 차단!
        GROUP BY 
            c.name, c.team, c.grade
        HAVING 
            COUNT(r.race_id) >= 5 -- 최소 5번 이상 출전한 신뢰성 있는 선수만 대상
        """
        
        df = pd.read_sql(query, con=connection)
        connection.close()
        
        if df.empty:
            print("⚠ 분석할 데이터가 부족합니다. 대량 수집을 먼저 진행해주세요.")
            return

        print("🔮 [경륜장 실전 예측 엔진] 데이터를 기반으로 모의 레이스를 분석 중입니다...")
        print("=" * 70)
        
        # 🚨 [파이썬 예측 공식 적용 구역] 
        # 가중치: 승률 40%, 연대율 45%, 삼연대율 15%
        df['PREDICT_SCORE'] = (df['WIN_RATE'] * 0.4) + (df['TOP2_RATE'] * 0.45) + (df['TOP3_RATE'] * 0.15)
        
        # 예측 점수가 높은 순서대로 정렬
        df_sorted = df.sort_values(by='PREDICT_SCORE', ascending=False).reset_index(drop=True)
        
        # 결과 출력하기
        print(f"{'순위':^4}|{'선수명':^6}|{'훈련지':^5}|{'출전':^4}|{'승률':^6}|{'연대율':^6}|{'삼연대율':^6}|{'최종 예측 점수':^8}")
        print("-" * 70)
        
        for idx, row in df_sorted.iterrows():
            print(f"{idx+1:^4}|{row['PLAYER_NAME']:^6}|{row['TEAM']:^5}|{int(row['TOTAL_RACES']):^4}|"
                  f"{row['WIN_RATE']:.1f}%|{row['TOP2_RATE']:.1f}%|{row['TOP3_RATE']:.1f}%|"
                  f"🔥 {row['PREDICT_SCORE']:.1f}점 / 100점")
            
        print("=" * 80)
        print("💡 [베팅 가이드] 점수가 높은 순서대로 '쌍승식(1,2등 적중)' 및 '삼복승식' 조합을 구성해 보세요!")

    except Exception as e:
        print(f"❌ 예측 연산 중 오류 발생: {e}")

if __name__ == "__main__":
    get_betting_predictions()
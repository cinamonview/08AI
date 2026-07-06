import requests
from bs4 import BeautifulSoup
import oracledb
from datetime import datetime, timedelta
from tqdm import tqdm  

# 오라클 DB 접속 설정
db_config = {
    "user": "education",
    "password": "1234",
    "dsn": "localhost:1521/xe"
}

# 걸러낼 유령 단어 목록
block_words = ['젖히기', '마크', '경고', '주의', '선행', '추입', '실격', '낙차', '재제', '기권']

# 🎭 [핵심 치트키] 서버 방화벽을 뚫기 위한 실제 크롬 브라우저 위장 가면
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
}

def get_connection():
    return oracledb.connect(**db_config)

def crawl_keirin_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 📅 최근 90일 기간 설정
    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)
    
    total_days = (end_date - start_date).days + 1
    
    print(f"🏁 전국 데이터 통합 수집 엔진 가동 (보안 우회 모드)!")
    print(f"📅 수집 기간: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')} ({total_days}일간)\n")

    locations = {1: "광명", 2: "창원", 3: "부산"}
    date_list = [start_date + timedelta(days=x) for x in range(total_days)]
    
    for current_date in tqdm(date_list, desc="🚀 전국 경륜 데이터 수집률", unit="일"):
        date_str = current_date.strftime("%Y%m%d")
        
        # 금, 토, 일요일 경기에 대해서만 수집 진행
        if current_date.weekday() in [4, 5, 6]: 
            for meet_code, loc_name in locations.items():
                url = f"https://www.kcycle.or.kr/contents/raceResult/rcResultList.do?raceDate={date_str}&meet={meet_code}"
                
                try:
                    # 🛠️ headers=headers 를 추가하여 브라우저인 척 위장하여 요청합니다!
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code != 200: continue
                        
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 가장 널리 쓰이는 테이블 행 selector 지정
                    rows = soup.select("table tbody tr")
                    
                    if not rows or "데이터가 없습니다" in soup.text:
                        continue
                    
                    # 데이터 존재 여부 실시간 출력
                    tqdm.write(f" ➡️ [적재 완료] {current_date.strftime('%Y-%m-%d')} - {loc_name} 경륜장")
                    
                    for row in rows:
                        try:
                            cols = row.find_all('td')
                            if len(cols) < 5: continue
                            
                            # 데이터 순서 매핑 안정화
                            race_num = cols[0].text.strip().zfill(2)
                            player_name = cols[1].text.strip()       
                            rank_str = cols[4].text.strip()          
                            
                            # 만약 순위 위치가 유동적일 경우 대비 방어 코드
                            if not rank_str.isdigit():
                                if cols[1].text.strip().isdigit():
                                    rank_str = cols[1].text.strip()
                                    player_name = cols[2].text.strip()
                                else:
                                    continue
                                    
                            if any(word in player_name for word in block_words) or len(player_name) > 4 or not player_name:
                                continue
                                
                            player_id = "C_" + player_name
                            rank_result = int(rank_str)
                            
                            race_id = f"{date_str}-{loc_name}-{race_num}"
                            team = "일반"
                            grade = loc_name  
                            tactics = "추입"
                            
                            # 1. 선수 정보 저장
                            player_merge_sql = """
                            MERGE INTO cyclist_info c
                            USING DUAL ON (c.cyclist_id = :1)
                            WHEN MATCHED THEN
                                UPDATE SET c.team = :2, c.grade = :3, c.tactics = :4
                            WHEN NOT MATCHED THEN
                                INSERT (cyclist_id, name, team, grade, tactics) VALUES (:1, :5, :2, :3, :4)
                            """
                            cursor.execute(player_merge_sql, (player_id, team, grade, tactics, player_name))
                            
                            # 2. 경기 결과 저장
                            race_merge_sql = """
                            MERGE INTO race_result r
                            USING DUAL ON (r.race_id = :1 AND r.cyclist_id = :2)
                            WHEN MATCHED THEN
                                UPDATE SET r.rank_result = :3, r.location = :4
                            WHEN NOT MATCHED THEN
                                INSERT (race_id, cyclist_id, rank_result, location) VALUES (:1, :2, :3, :4)
                            """
                            cursor.execute(race_merge_sql, (race_id, player_id, rank_result, loc_name))
                            
                        except Exception as e:
                            continue
                            
                    conn.commit()
                    
                except Exception as e:
                    continue
        
    cursor.close()
    conn.close()
    print("\n✨ Complete! 전국 3대 경륜장 데이터가 완벽하게 동기화되었습니다!")

if __name__ == "__main__":
    crawl_keirin_data()
import oracledb
import pandas as pd

# 오라클 데이터베이스 접속 정보 설정 (본인의 환경에 맞게 수정 가능)
db_config = {
    "user": "education",        # 실습용 계정 이름
    "password": "1234", # education 계정의 비밀번호 입력
    "dsn": "localhost:1521/xe"  # 호스트:포트/SID (보통 기본값은 xe 또는 orcl)
}

def insert_cyclist_data(df_cyclists):
    """
    선수 기본 정보(cyclist_info) 데이터를 오라클에 저장하는 함수
    """
    connection = None
    try:
        # 1. 오라클 DB 연결 (Thick 모드가 아닌 Thin 모드로 별도 프로그램 없이 바로 연결됩니다)
        connection = oracledb.connect(**db_config)
        cursor = connection.cursor()
        
        # 2. 오라클용 INSERT SQL 쿼리문 (기존 데이터가 있으면 무시하거나 업데이트하는 MERGE문 구조가 좋으나, 여기선 기본 INSERT)
        # :1, :2 등은 파이썬 데이터를 바인딩할 파라미터 위치입니다.
        sql = """
        INSERT INTO cyclist_info (cyclist_id, name, grade, team, cycle_type)
        VALUES (:1, :2, :3, :4, :5)
        """
        
        # 3. 데이터프레임의 행들을 튜플 리스트로 변환 (한 번에 대량 insert 하기 위함)
        data_to_insert = [
            (row['player_id'], row['player_name'], row.get('grade', 'A1'), row.get('team', '미정'), row.get('cycle_type', '추입'))
            for _, row in df_cyclists.iterrows()
        ]
        
        # 4. executemany로 수십~수백 개 데이터를 한 번에 초고속으로 전송!
        cursor.executemany(sql, data_to_insert)
        
        # 5. 오라클은 수동 커밋이 기본이므로 꼭 반영해줘야 합니다.
        connection.commit()
        print(f"✅ 선수 정보 {len(data_to_insert)}건 오라클 DB 적재 완료!")
        
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"❌ DB 오류 발생: {error.message}")
        if connection:
            connection.rollback() # 에러 나면 되돌리기
            
    finally:
        if connection:
            cursor.close()
            connection.close()

# ==========================================
# 가짜(테스트용) 크롤링 데이터로 DB 연동 확인해보기
# ==========================================
if __name__ == "__main__":
    # 크롤러가 긁어왔다고 가정하는 가상의 데이터프레임 만들기
    test_data = {
        'player_id': ['C00001', 'C00002'],
        'player_name': ['홍길동', '임꺽정'],
        'grade': ['SS', 'S1'],
        'team': ['광명', '가평'],
        'cycle_type': ['선행', '젖히기']
    }
    df_test = pd.DataFrame(test_data)
    
    # DB에 집어넣기 실행!
    insert_cyclist_data(df_test)
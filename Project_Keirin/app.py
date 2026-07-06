from flask import Flask, render_template_string, jsonify, request
import oracledb
import pandas as pd

app = Flask(__name__)

# 오라클 접속 설정
db_config = {
    "user": "education",
    "password": "1234",
    "dsn": "localhost:1521/xe"
}

# 🎨 전국구 확장 및 검색 창이 추가된 최신 HTML 템플릿
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔮 전국 경륜장 AI 통합 검색 & 예측 엔진</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background-color: #f8f9fa; font-family: 'Malgun Gothic', sans-serif; }
        .main-header { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 30px 0; border-radius: 0 0 20px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .card { border-radius: 15px; border: none; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        .table th { background-color: #e9ecef; }
        .chart-container { max-width: 500px; margin: 0 auto; }
    </style>
</head>
<body>

<div class="container text-center main-header mb-4">
    <h1 class="fw-bold">🏁 전국 경륜장 AI 통합 검색 시스템</h1>
    <p class="lead mb-0">광명·창원·부산 데이터를 아우르는 실시간 선수 분석 가이드</p>
</div>

<div class="container text-center mb-4">
    <div class="card p-3 shadow-sm d-inline-block">
        <div class="d-flex gap-3 justify-content-center align-items-center flex-wrap">
            <div>
                <label class="form-label fw-bold small text-muted mb-1 text-start d-block">🏢 경륜장 선택</label>
                <select id="select-location" class="form-select" style="width: 150px;">
                    <option value="ALL">전체 경륜장</option>
                    <option value="광명">광명 경륜장</option>
                    <option value="창원">창원 경륜장</option>
                    <option value="부산">부산 경륜장</option>
                </select>
            </div>
            <div>
                <label class="form-label fw-bold small text-muted mb-1 text-start d-block">👤 선수명 검색</label>
                <input type="text" id="search-name" class="form-control" placeholder="선수 이름 입력" style="width: 180px;">
            </div>
            <div class="pt-4">
                <button id="btn-predict" class="btn btn-success px-4 fw-bold shadow-sm">🔮 통합 분석 실행</button>
            </div>
        </div>
    </div>
</div>

<div class="container">
    <div class="row">
        <div class="col-lg-7 mb-4">
            <div class="card p-4 h-100">
                <h3 class="fw-bold mb-3 text-secondary">📋 AI 예측 순위표</h3>
                <div class="table-responsive">
                    <table class="table table-hover align-middle text-center">
                        <thead>
                            <tr>
                                <th>순위</th>
                                <th>선수명</th>
                                <th>훈련지</th>
                                <th>승률</th>
                                <th>최종 점수</th>
                            </tr>
                        </thead>
                        <tbody id="predict-result">
                            <tr>
                                <td colspan="5" class="text-muted py-5">조건 선택 후 분석 실행 버튼을 눌러주세요.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div class="col-lg-5 mb-4">
            <div class="card p-4 h-100 text-center">
                <h3 class="fw-bold mb-3 text-secondary">🕸️ 레이더 차트 분석</h3>
                <div class="chart-container py-3">
                    <canvas id="radarChart"></canvas>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
let myRadarChart = null;

document.getElementById('btn-predict').addEventListener('click', function() {
    const location = document.getElementById('select-location').value;
    const name = document.getElementById('search-name').value.trim();

    const tbody = document.getElementById('predict-result');
    tbody.innerHTML = `<tr><td colspan="5" class="text-success py-5"><div class="spinner-border" role="status"></div><br><br>전국 DB 분석 엔진 연산 중...</td></tr>`;

    // 💡 검색 조건을 URL 쿼리 스트링 파라미터로 붙여서 Flask로 보냅니다!
    fetch(`/api/predict?location=${location}&name=${name}`)
        .then(response => response.json())
        .then(res => {
            if(res.status === 'success') {
                let html = '';
                res.data.forEach(row => {
                    html += `
                        <tr class="${row.rank <= 3 ? 'table-light fw-bold' : ''}">
                            <td><span class="badge ${row.rank <= 3 ? 'bg-danger' : 'bg-secondary'}">${row.rank}위</span></td>
                            <td class="text-primary">${row.name}</td>
                            <td>${row.team}</td>
                            <td>${row.win}%</td>
                            <td class="text-danger fw-bold">🔥 ${row.score}점</td>
                        </tr>
                    `;
                });
                tbody.innerHTML = html;

                const topPlayers = res.data.slice(0, 3);
                if (myRadarChart) { myRadarChart.destroy(); }

                const colors = [
                    { fill: 'rgba(46, 204, 113, 0.2)', border: 'rgba(46, 204, 113, 1)' }, // 민트 계열
                    { fill: 'rgba(52, 152, 219, 0.2)', border: 'rgba(52, 152, 219, 1)' }, // 블루 계열
                    { fill: 'rgba(241, 196, 15, 0.2)', border: 'rgba(241, 196, 15, 1)' }  // 옐로우 계열
                ];

                const datasets = topPlayers.map((player, idx) => {
                    return {
                        label: player.name,
                        data: [player.win, player.top2, player.top3, player.score],
                        backgroundColor: colors[idx].fill,
                        borderColor: colors[idx].border,
                        borderWidth: 2,
                        pointBackgroundColor: colors[idx].border
                    }
                });

                const ctx = document.getElementById('radarChart').getContext('2d');
                myRadarChart = new Chart(ctx, {
                    type: 'radar',
                    data: {
                        labels: ['순수 승률', '연대율(2등이내)', '삼연대율(3등이내)', '최종 예측점수'],
                        datasets: datasets
                    },
                    options: {
                        responsive: true,
                        scales: { r: { suggestMin: 0, suggestMax: 100 } }
                    }
                });

            } else {
                tbody.innerHTML = `<tr><td colspan="5" class="text-danger py-5">❌ ${res.message}</td></tr>`;
                if (myRadarChart) { myRadarChart.destroy(); }
            }
        })
        .catch(err => {
            tbody.innerHTML = `<tr><td colspan="5" class="text-danger py-5">❌ 서버 통신 실패</td></tr>`;
        });
});
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/predict')
def get_predict_data():
    try:
        # 화면단에서 보낸 검색 파라미터 접수
        loc_param = request.args.get('location', 'ALL')
        name_param = request.args.get('name', '')

        connection = oracledb.connect(**db_config)
        
        # 기본 뼈대 쿼리문 작성 (Dynamic WHERE 절 구성을 위해 1=1 처리)
        query = """
        SELECT 
            c.name AS PLAYER_NAME, c.team AS TEAM, c.grade AS GRADE, COUNT(r.race_id) AS TOTAL_RACES,
            ROUND(COUNT(CASE WHEN r.rank_result = 1 THEN 1 END) / COUNT(r.race_id) * 100, 1) AS WIN_RATE,
            ROUND(COUNT(CASE WHEN r.rank_result IN (1, 2) THEN 1 END) / COUNT(r.race_id) * 100, 1) AS TOP2_RATE,
            ROUND(COUNT(CASE WHEN r.rank_result IN (1, 2, 3) THEN 1 END) / COUNT(r.race_id) * 100, 1) AS TOP3_RATE
        FROM cyclist_info c 
        JOIN race_result r ON c.cyclist_id = r.cyclist_id
        WHERE c.name NOT IN ('젖히기', '마크', '경고', '주의', '선행', '추입', '실격', '낙차')
        """
        
        # 💡 조건 1: 특정 경륜장을 선택한 경우
        if loc_param != 'ALL':
            query += f" AND r.location = '{loc_param}'"
            
        # 💡 조건 2: 선수 이름을 검색창에 넣은 경우 (LIKE 연산으로 부분 검색 허용)
        if name_param:
            query += f" AND c.name LIKE '%{name_param}%'"

        query += " GROUP BY c.name, c.team, c.grade"
        
        df = pd.read_sql(query, con=connection)
        connection.close()
        
        if df.empty:
            return jsonify({"status": "error", "message": "검색 결과와 일치하는 선수가 없거나 데이터가 부족합니다."})

        df['PREDICT_SCORE'] = (df['WIN_RATE'] * 0.4) + (df['TOP2_RATE'] * 0.45) + (df['TOP3_RATE'] * 0.15)
        df_sorted = df.sort_values(by='PREDICT_SCORE', ascending=False).reset_index(drop=True)
        
        result_data = []
        for idx, row in df_sorted.iterrows():
            result_data.append({
                "rank": idx + 1, "name": row['PLAYER_NAME'], "team": row['TEAM'], "grade": row['GRADE'],
                "total": int(row['TOTAL_RACES']), "win": row['WIN_RATE'], "top2": row['TOP2_RATE'],
                "top3": row['TOP3_RATE'], "score": round(row['PREDICT_SCORE'], 1)
            })
        return jsonify({"status": "success", "data": result_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # 5002번 포트 가동 유지
    app.run(debug=True, port=5002)
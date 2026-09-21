import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title='영화 데이터 그래프 도감 1 - 시간', layout='wide')

st.title('영화 데이터 그래프 도감 1 - 시간')

# 데이터 로드 및 전처리 (캐싱을 사용하여 로딩 속도 향상)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 날짜(8자리 숫자)를 datetime 형식으로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    # 관객수 데이터를 수치형으로 안전하게 변환
    df['일관객'] = pd.to_numeric(df['일관객'], errors='coerce').fillna(0)
    
    return df

df = load_data()

# -------------------------------------------------------------------
# [구역 1] 영화별 일일 관객수 변화
# -------------------------------------------------------------------
st.header('1. 영화별 일일 관객수 변화')

# 영화명 목록 추출 및 가나다순 정렬
movie_list = sorted(df['영화명'].unique())
selected_movie = st.selectbox('영화를 선택하세요:', movie_list)

# 선택된 영화 데이터 필터링 및 날짜순 정렬
filtered_df = df[df['영화명'] == selected_movie].sort_values('날짜')

# Plotly 선 그래프 생성
fig1 = px.line(
    filtered_df,
    x='날짜',
    y='일관객',
    title=f'[{selected_movie}] 일일 관객 추이'
)

# 마우스를 올렸을 때(hover) 표시될 툴팁 서식 지정
fig1.update_traces(
    hovertemplate='날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,.0f}명<extra></extra>'
)

# 그래프 화면 출력
st.plotly_chart(fig1, use_container_width=True)

# 그래프 해석 문구 자리
st.info('이 그래프로 알 수 있는 것: 개봉 직후 관객수 변화 양상과 특정 요일(주말 등)의 관객수 급증 패턴을 확인할 수 있습니다.')

st.divider()

# -------------------------------------------------------------------
# [구역 2] 총 관객수 상위 5개 영화의 일일 관객 추이 비교
# -------------------------------------------------------------------
st.header('2. 총 관객수 상위 5개 영화의 일일 관객 추이 비교')

# 기간 내 일관객 합계 기준 상위 5개 영화 추출
top5_movies = (
    df.groupby('영화명')['일관객']
    .sum()
    .nlargest(5)
    .index
    .tolist()
)

# 상위 5개 영화 데이터 필터링 및 날짜순 정렬
df_top5 = df[df['영화명'].isin(top5_movies)].sort_values('날짜')

# Plotly 다중 선 그래프 생성 (color 옵션으로 영화별 구분)
fig2 = px.line(
    df_top5,
    x='날짜',
    y='일관객',
    color='영화명',
    title='기간 내 총 관객수 상위 5개 영화 비교'
)

# 마우스 툴팁 서식 지정
fig2.update_traces(
    hovertemplate='날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,.0f}명<extra></extra>'
)

# 그래프 화면 출력 (오른쪽 범례를 클릭하여 특정 영화 선을 켜고 끌 수 있음)
st.plotly_chart(fig2, use_container_width=True)

# 그래프 해석 문구 자리
st.info('이 그래프로 알 수 있는 것: 기간 내 최고 흥행작 Top 5간의 개봉 시기 차이, 흥행 유지 기간, 정점(피크) 관객수를 서로 비교할 수 있습니다.')

st.divider()

# -------------------------------------------------------------------
# [구역 3] 향후 추가될 그래프를 위한 공간
# -------------------------------------------------------------------
st.header('3. (추가할 그래프 제목을 입력하세요)')
st.write('이곳에 새로운 시간 관련 데이터 그래프가 추가될 예정입니다.')

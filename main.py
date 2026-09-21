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

# Plotly 다중 선 그래프 생성
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

# 그래프 화면 출력
st.plotly_chart(fig2, use_container_width=True)

# 그래프 해석 문구 자리
st.info('이 그래프로 알 수 있는 것: 기간 내 최고 흥행작 Top 5간의 개봉 시기 차이, 흥행 유지 기간, 정점(피크) 관객수를 서로 비교할 수 있습니다.')

st.divider()

# -------------------------------------------------------------------
# [구역 3] 날짜별 박스오피스 TOP 10 일관객 합계 변화
# -------------------------------------------------------------------
st.header('3. 날짜별 박스오피스 TOP 10 일관객 합계 (영역 그래프)')

# 날짜별 TOP 10 영화의 일관객 합계 계산 및 정렬
df_daily_sum = df.groupby('날짜', as_index=False)['일관객'].sum().sort_values('날짜')

# Plotly 영역 그래프(Area Chart) 생성
fig3 = px.area(
    df_daily_sum,
    x='날짜',
    y='일관객',
    title='날짜별 박스오피스 TOP 10 전체 관객수 합계 추이'
)

# 마우스 툴팁 서식 지정
fig3.update_traces(
    hovertemplate='날짜: %{x|%Y-%m-%d}<br>TOP 10 총 관객수: %{y:,.0f}명<extra></extra>'
)

# 일관객 합계 상위 3개 날짜 추출
top3_dates = df_daily_sum.nlargest(3, '일관객')

# 그래프 상단에 상위 3일 날짜 및 관객수 주석(Annotation) 표시
for _, row in top3_dates.iterrows():
    date_str = row['날짜'].strftime('%Y-%m-%d')
    audience_val = row['일관객']
    
    fig3.add_annotation(
        x=row['날짜'],
        y=audience_val,
        text=f"<b>{date_str}</b><br>({audience_val:,.0f}명)",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1.5,
        arrowcolor="red",
        ax=0,
        ay=-45,
        bordercolor="red",
        borderwidth=1,
        borderpad=4,
        bgcolor="rgba(255, 255, 255, 0.9)"
    )

# 그래프 화면 출력
st.plotly_chart(fig3, use_container_width=True)

# 그래프 해석 문구 자리
st.info('이 그래프로 알 수 있는 것: 영화 시장 전체의 연중 성수기(명절, 연휴, 여름/겨울 방학 등)와 비수기 흐름을 한눈에 파악할 수 있으며, 일년 중 관객 수가 가장 많이 몰린 상위 3일을 확인할 수 있습니다.')

st.divider()

# -------------------------------------------------------------------
# [구역 4] 기간 내 관객수 TOP 10 영화 (가로 막대그래프)
# -------------------------------------------------------------------
st.header('4. 기간 내 관객수 TOP 10 영화 및 10위권 진입 일수')

# 영화별 총 관객수 및 10위권 진입 일수 집계
df_top10_bar = (
    df.groupby('영화명')
    .agg(
        총관객수=('일관객', 'sum'),
        진입일수=('날짜', 'count')
    )
    .reset_index()
    .nlargest(10, '총관객수')
    .sort_values('총관객수', ascending=True)
)

# Plotly 가로 막대그래프 생성
fig4 = px.bar(
    df_top10_bar,
    x='총관객수',
    y='영화명',
    orientation='h',
    title='기간 내 총 관객수 TOP 10 영화'
)

# 마우스 툴팁 서식 및 커스텀 데이터 지정
fig4.update_traces(
    customdata=df_top10_bar[['진입일수']],
    hovertemplate='<b>%{y}</b><br>총 관객수: %{x:,.0f}명<br>10위권 진입 일수: %{customdata[0]}일<extra></extra>'
)

# 축 레이블 설정
fig4.update_layout(
    xaxis_title='총 관객수 (명)',
    yaxis_title='영화명'
)

# 그래프 화면 출력
st.plotly_chart(fig4, use_container_width=True)

# 그래프 해석 문구 자리
st.info('이 그래프로 알 수 있는 것: 기간 내 가장 많은 선택을 받은 상위 10개 영화의 전체 관객 동원력과, 박스오피스 TOP 10 차트에 얼마나 오랫동안 머물렀는지(흥행 지속력)를 비교할 수 있습니다.')

st.divider()

# -------------------------------------------------------------------
# [구역 5] 월×요일별 관객수 합계 (히트맵)
# -------------------------------------------------------------------
st.header('5. 월×요일별 관객수 합계 (히트맵)')

# 월 및 요일 데이터 추출
df_heatmap = df.copy()
df_heatmap['월'] = df_heatmap['날짜'].dt.month.astype(str) + '월'

day_map = {0: '월요일', 1: '화요일', 2: '수요일', 3: '목요일', 4: '금요일', 5: '토요일', 6: '일요일'}
df_heatmap['요일'] = df_heatmap['날짜'].dt.dayofweek.map(day_map)

# 월×요일 피벗 테이블 생성 (관객수 합계 집계)
pivot_df = df_heatmap.pivot_table(
    index='요일',
    columns='월',
    values='일관객',
    aggfunc='sum'
).fillna(0)

# 요일 및 월 순서 정렬
days_order = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
months_order = [f'{i}월' for i in range(1, 13)]
existing_months = [m for m in months_order if m in pivot_df.columns]

pivot_df = pivot_df.reindex(index=days_order, columns=existing_months)

# Plotly 히트맵 생성 (Blues 컬러스케일 사용: 값이 크고 진할수록 관객수가 많음)
fig5 = px.imshow(
    pivot_df,
    labels=dict(x="월", y="요일", color="관객수 합계"),
    color_continuous_scale="Blues",
    title="월 및 요일별 관객수 합계 히트맵"
)

# 마우스 툴팁 서식 지정
fig5.update_traces(
    hovertemplate='%{x} %{y}<br>총 관객수: %{z:,.0f}명<extra></extra>'
)

# 축 레이블 설정
fig5.update_layout(
    xaxis_title="월",
    yaxis_title="요일"
)

# 그래프 화면 출력
st.plotly_chart(fig5, use_container_width=True)

# 그래프 해석 문구 자리
st.info('이 그래프로 알 수 있는 것: 각 월별로 어떤 요일에 관객이 집중되는지 파악할 수 있으며, 여름/겨울 방학이나 명절이 포함된 달의 평일 관객수 증가 양상을 한눈에 비교할 수 있습니다.')

st.divider()

# -------------------------------------------------------------------
# [구역 6] 향후 추가될 그래프를 위한 공간
# -------------------------------------------------------------------
st.header('6. (추가할 그래프 제목을 입력하세요)')
st.write('이곳에 새로운 시간 관련 데이터 그래프가 추가될 예정입니다.')

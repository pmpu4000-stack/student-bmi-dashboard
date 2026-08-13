import io
import os
import dash
from dash import dcc, html, Input, Output
import dash_mantine_components as dmc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ============================================================================
# 1. 資料與常數定義
# ============================================================================
csv_data = """體位類別,性別,年度,百分比
適中,男,96,53.4
適中,女,96,58.1
過輕,男,96,17.6
過輕,女,96,20.4
過重,男,96,14.4
過重,女,96,11.9
肥胖,男,96,14.7
肥胖,女,96,9.6
適中,男,97,53.2
適中,女,97,57.9
過輕,男,97,18.2
過輕,女,97,21.2
過重,男,97,14.3
過重,女,97,11.7
肥胖,男,97,14.3
肥胖,女,97,9.3
適中,男,98,52.3
適中,女,98,57.1
過輕,男,98,18.9
過輕,女,98,21.9
過重,男,98,14.3
過重,女,98,11.6
肥胖,男,98,14.5
肥胖,女,98,9.3
適中,男,99,59.5
適中,女,99,66.7
過輕,男,99,6.6
過輕,女,99,7.7
過重,男,99,15.7
過重,女,99,12.9
肥胖,男,99,18.2
肥胖,女,99,12.6
適中,男,100,60.1
適中,女,100,67.2
過輕,男,100,6.6
過輕,女,100,7.7
過重,男,100,15.4
過重,女,100,12.7
肥胖,男,100,17.8
肥胖,女,100,12.4
適中,男,101,59.7
適中,女,101,66.8
過輕,男,101,6.6
過輕,女,101,7.7
過重,男,101,15.5
過重,女,101,12.9
肥胖,男,101,18.2
肥胖,女,101,12.7
適中,男,102,59.5
適中,女,102,66.3
過輕,男,102,6.4
過輕,女,102,7.4
過重,男,102,15.5
過重,女,102,13
肥胖,男,102,18.7
肥胖,女,102,13.2
適中,男,103,60.3
適中,女,103,67.2
過輕,男,103,6.8
過輕,女,103,7.8
過重,男,103,15
過重,女,103,12.3
肥胖,男,103,17.8
肥胖,女,103,12.6
適中,男,104,60.6
適中,女,104,67.4
過輕,男,104,7
過輕,女,104,7.9
過重,男,104,14.7
過重,女,104,12.2
肥胖,男,104,17.7
肥胖,女,104,12.5
適中,男,105,60.7
適中,女,105,67.5
過輕,男,105,7.5
過輕,女,105,8.4
過重,男,105,14.5
過重,女,105,11.9
肥胖,男,105,17.4
肥胖,女,105,12.2
適中,男,106,60.9
適中,女,106,67.8
過輕,男,106,7.8
過輕,女,106,8.6
過重,男,106,14.3
過重,女,106,11.6
肥胖,男,106,17,106
肥胖,女,106,12
適中,男,107,61.2
適中,女,107,68.3
過輕,男,107,7.5
過輕,女,107,8.3
過重,男,107,14.2
過重,女,107,11.6
肥胖,男,107,17.1
肥胖,女,107,11.9
適中,男,108,61.6
適中,女,108,68.3
過輕,男,108,7.7
過輕,女,108,8.4
過重,男,108,14
過重,女,108,11.5
肥胖,男,108,16.7
肥胖,女,108,11.8
適中,男,109,62.6
適中,女,109,68.9
過輕,男,109,8.5
過輕,女,109,9.3
過重,男,109,13.6
過重,女,109,11
肥胖,男,109,15.3
肥胖,女,109,10.8
適中,男,110,60.7
適中,女,110,68.2
過輕,男,110,8
過輕,女,110,9.2
過重,男,110,14.4
過重,女,110,11.3
肥胖,男,110,16.8
肥胖,女,110,11.4
適中,男,111,60.9
適中,女,111,68.3
過輕,男,111,8.7
過輕,女,111,9.7
過重,男,111,13.8
過重,女,111,10.8
肥胖,男,111,16.6
肥胖,女,111,11.1
適中,男,112,62.8
適中,女,112,69.1
過輕,男,112,10
過輕,女,112,10.7
過重,男,112,12.6
過重,女,112,10.1
肥胖,男,112,14.6
肥胖,女,112,10.1
適中,男,113,63.5
適中,女,113,69.6
過輕,男,113,9.8
過輕,女,113,10.2
過重,男,113,12.5
過重,女,113,10.2
肥胖,男,113,14.2
肥胖,女,113,10.1"""

# 修正讀取資料的小錯誤（原始 CSV 裡 106 年那行有多餘 "106"，在這裡修掉）
csv_data = csv_data.replace('\n肥胖,男,106,17,106\n', '\n肥胖,男,106,17\n')

df = pd.read_csv(io.StringIO(csv_data))
df["年度"] = df["年度"].astype(int)
df["百分比"] = df["百分比"].astype(float)

MIN_YEAR, MAX_YEAR = 95, int(df["年度"].max())
ALL_YEARS = list(range(MIN_YEAR, MAX_YEAR + 1))
PRED_YEARS = [114, 115, 116]

# ============================================================================
# 2. 事件與顏色常數
# ============================================================================
# 統一事件資料（取代原本的 EVENT_MAP + ALL_EVENTS）
ALL_EVENTS = [
    {"year": 95, "type": "positive", "text": "校園飲品及點心販售範圍"},
    {"year": 97, "type": "positive", "text": "健康促進學校計畫全面推動"},
    {"year": 98, "type": "positive", "text": "體適能檢測全面實施"},
    {"year": 99, "type": "negative", "text": "智慧型手機與行動網路普及"},
    {"year": 103, "type": "positive", "text": "推行健康成長密碼85210"},
    {"year": 106, "type": "positive", "text": "三章一Q政策與午餐食材登錄"},
    {"year": 107, "type": "negative", "text": "外送平台快速崛起"},
    {"year": 108, "type": "positive", "text": "108 課綱正式上路"},
    {"year": 109, "type": "negative", "text": "COVID-19 疫情衝擊"},
    {"year": 111, "type": "positive", "text": "生生用平板方案 / 食農教育法實施"}
]

# 輔助索引：year -> [events]
EVENT_BY_YEAR = {}
for e in ALL_EVENTS:
    EVENT_BY_YEAR.setdefault(e["year"], []).append(e)

# UI 常數
DARK_BG = "#1e1e1e"
CARD_BG = "#2d2d2d"
TEXT_COLOR = "#ffffff"
MALE_COLOR = "#29b6f6"
FEMALE_COLOR = "#ff4081"

# 明亮顏色（使用使用者要求的亮綠與亮紫）
POLICY_COLOR = "#00FF00"      # 亮綠色（政府政策）
EVENT_COLOR = "#BF00FF"       # 亮紫色（社會事件）

# 性別分類選項
GENDER_OPTIONS = {
    "male": [
        {
            "label": html.Span(cat, style={"color": GENDER_COLORS["male"][cat], "fontWeight": "bold"}),
            "value": f"男_{cat}"
        } 
        for cat in ["過輕", "適中", "過重", "肥胖"]
    ],
    "female": [
        {
            "label": html.Span(cat, style={"color": GENDER_COLORS["female"][cat], "fontWeight": "bold"}),
            "value": f"女_{cat}"
        } 
        for cat in ["過輕", "適中", "過重", "肥胖"]
    ],
}

# 顏色映射
COLOR_MAP = {
    "男生 - 過輕": "#81d4fa", "男生 - 適中": "#29b6f6", "男生 - 過重": "#0288d1", "男生 - 肥胖": "#01579b",
    "女生 - 過輕": "#ff80ab", "女生 - 適中": "#ff4081", "女生 - 過重": "#f50057", "女生 - 肥胖": "#c51162",
}

GENDER_COLORS = {
    "male": {
        "過輕": "#2196f3",  # 男生過輕改成標準藍
        "適中": "#2ca02c",  # 男生適中 (標準綠)
        "過重": "#ff9800",  # 男生過重 (橘色)
        "肥胖": "#d32f2f"   # 男生肥胖 (深紅)
    },
    "female": {
        "過輕": "#b3e5fc",  # 女生過輕 (極淺藍)
        "適中": "#81c784",  # 女生適中 (柔和綠)
        "過重": "#ffb74d",  # 女生過重 (柔和橘)
        "肥胖": "#f06292"   # 女生肥胖 (粉桃紅)
    }
}

# ============================================================================
# 3. 樣式常數
# ============================================================================
INPUT_STYLE = {
    "width": "70px", "padding": "6px", "borderRadius": "4px", "border": "1px solid #555555",
    "backgroundColor": CARD_BG, "color": TEXT_COLOR, "textAlign": "center",
    "fontSize": "14px", "fontWeight": "bold",
}

CARD_STYLE = {
    "backgroundColor": CARD_BG, "padding": "20px", "borderRadius": "8px", "border": "1px solid #444",
}

LABEL_STYLE = {
    "fontWeight": "bold", "marginBottom": "10px", "display": "block",
}

# ============================================================================
# 4. 工具函數
# ============================================================================
def create_event_block(year_label, event_type, event_text):
    """生成統一的事件卡片（消除重複代碼）"""
    bg_color = POLICY_COLOR if event_type == "positive" else EVENT_COLOR
    return html.Div([
        html.Div(year_label, style={
            "backgroundColor": bg_color, "color": "#ffffff", "padding": "4px 12px",
            "borderRadius": "4px", "fontWeight": "bold", "fontSize": "13px",
            "display": "inline-block", "marginBottom": "6px",
        }),
        html.Div(event_text, style={"color": "#e0e0e0", "fontSize": "14px"}),
    ], style={
        "padding": "12px 15px", "backgroundColor": "#252525", "borderRadius": "6px",
        "borderLeft": f"4px solid {bg_color}", "marginBottom": "10px",
    })


def create_gender_checklist(gender_key, color):
    """生成性別選擇列表"""
    return html.Div([
        html.Span(f"{'男生' if gender_key == 'male' else '女生'}：",
                 style={"fontWeight": "bold", "color": color, "marginBottom": "4px", "display": "block"}),
        dcc.Checklist(
            id=f"{'male' if gender_key == 'male' else 'female'}-checklist",
            options=GENDER_OPTIONS[gender_key],
            value=["男_適中" if gender_key == "male" else "女_適中"],
            labelStyle={"display": "block", "marginBottom": "4px", "color": color},
        ),
    ], style={"flex": 1, "marginRight": "10px" if gender_key == "male" else 0})


def get_common_bar_layout(start_y, end_y):
    """返回堆疊長條圖的通用 layout 配置"""
    return {
        "barmode": "stack",
        "paper_bgcolor": DARK_BG,
        "plot_bgcolor": CARD_BG,
        "font": dict(color=TEXT_COLOR, size=14),
        "margin": dict(l=40, r=40, t=20, b=40),
        "xaxis": dict(
            title=dict(text="年度 (民國)", font=dict(size=16)),
            showgrid=True, gridcolor="#333333", tickmode="array",
            tickvals=ALL_YEARS, ticktext=[str(y) for y in ALL_YEARS],
            range=[start_y - 0.5, end_y + 0.5], tickfont=dict(size=14)
        ),
        "yaxis": dict(
            title=dict(text="百分比 (%)", font=dict(size=16)),
            showgrid=True, gridcolor="#333333", range=[0, 105], tickfont=dict(size=14)
        ),
        "legend": dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=14))
    }


def create_stacked_bar_chart(gender, year_range):
    """統一生成堆疊長條圖（消除兩個 callback 重複代碼）"""
    start_y, end_y = year_range
    gender_char = "男" if gender == "male" else "女"
    df_filtered = df[(df["年度"] >= start_y) & (df["年度"] <= end_y) & (df["性別"] == gender_char)]

    fig = go.Figure()
    for cat in ["過輕", "適中", "過重", "肥胖"]:
        df_sub = df_filtered[df_filtered["體位類別"] == cat]
        fig.add_trace(go.Bar(
            x=df_sub["年度"], y=df_sub["百分比"], name=cat,
            marker_color=GENDER_COLORS[gender][cat]
        ))

    fig.update_layout(get_common_bar_layout(start_y, end_y))
    return fig


def create_heatmap(gender, year_range):
    """生成性別的熱力圖（修正欄列對齊與資料型態問題）"""
    # 安全處理 year_range
    if not year_range:
        start_y, end_y = MIN_YEAR, MAX_YEAR
    else:
        start_y, end_y = int(min(year_range)), int(max(year_range))

    gender_char = "男" if gender == "male" else "女"

    # 篩選資料
    df_filtered = df[(df["年度"] >= start_y) & (df["年度"] <= end_y) & (df["性別"] == gender_char)]

    # 建立完整的年度索引
    years = list(range(start_y, end_y + 1))

    # pivot 並確保欄位為完整的年度序列（強制轉為字串以防萬一）
    pivot_data = df_filtered.pivot(index="體位類別", columns="年度", values="百分比")
    pivot_data = pivot_data.reindex(index=["過輕", "適中", "過重", "肥胖"], columns=years)

    # 若完全沒有資料，回傳帶提示的空圖
    if pivot_data.isnull().all().all():
        fig = go.Figure()
        fig.add_annotation(
            text="沒有符合條件的資料可呈現",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=TEXT_COLOR)
        )
        fig.update_layout(
            paper_bgcolor=DARK_BG, plot_bgcolor=CARD_BG,
            margin=dict(l=80, r=40, t=40, b=40),
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
            font=dict(color=TEXT_COLOR)
        )
        return fig

    x_vals = [str(y) for y in pivot_data.columns]
    y_vals = pivot_data.index.tolist()

    # 確保 z 值為 float 矩陣，保留 NaN
    z_vals = pivot_data.values.astype(float)

    colorscale = "Viridis"
    gender_display = "男生" if gender == "male" else "女生"

    customdata = np.full(z_vals.shape, gender_display, dtype=object)

    fig = go.Figure(data=go.Heatmap(
        z=z_vals,
        x=x_vals,
        y=y_vals,
        colorscale=colorscale,
        customdata=customdata,
        hovertemplate="<b>%{customdata}</b><br>年度：民國 %{x} 年<br>體位：%{y}<br>百分比：%{z:.1f}%<extra></extra>"
    ))

    fig.update_layout(
        paper_bgcolor=DARK_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_COLOR, size=14),
        margin=dict(l=80, r=40, t=40, b=40),
        xaxis=dict(title=dict(text="年度 (民國)", font=dict(size=16)), showgrid=False),
        yaxis=dict(title=dict(text="體位類別", font=dict(size=16)), showgrid=False)
    )

    return fig

    # 將 x 軸轉為字串，並把 NaN 保留（Plotly 能處理 NaN，不會顯示格子）
    x_vals = [str(y) for y in pivot_data.columns]
    y_vals = pivot_data.index.tolist()

    # 轉換 z 資料，讓 NaN 保持為 np.nan（或 None），以避免不一致導致 Plotly 錯誤
    raw_z = pivot_data.values
    # 使用 float 並保留 np.nan
    z_vals = np.array(raw_z, dtype=float)

    colorscale = "Blues" if gender == "male" else "Reds"

    # 讓 hover 顯示為 橫向：性別 - 體位 - 百分比
    gender_display = "男生" if gender == "male" else "女生"
    # customdata 必須與 z 形狀一致，填入性別字串
    customdata = np.full(z_vals.shape, gender_display, dtype=object)

    fig = go.Figure(data=go.Heatmap(
        z=z_vals,
        x=x_vals,
        y=y_vals,
        customdata=customdata,
        colorscale=colorscale,
        hovertemplate="%{customdata} - %{y} - %{z:.1f}%<extra></extra>",
        colorbar=dict(title="百分比 (%)", titleside="right", ticksuffix="%")
    ))

    fig.update_layout(
        xaxis_title="年度 (民國)",
        yaxis_title="體位類別",
        paper_bgcolor=DARK_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_COLOR, size=14),
        margin=dict(l=80, r=40, t=40, b=40),
        xaxis=dict(showgrid=False, tickmode="array", tickvals=x_vals, ticktext=x_vals),
        yaxis=dict(showgrid=False),
    )

    return fig


# ============================================================================
# 5. Dash App 初始化
# ============================================================================
app = dash.Dash(__name__)
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>國民小學學生歷年體位趨勢報告</title>
        {%metas%}
        {%css%}
        <style>
            /* 隱藏左上角的 Loading 提示 */
            ._dash-loading {
                display: none !important;
            }
            input[type=number]::-webkit-inner-spin-button,
            input[type=number]::-webkit-outer-spin-button {
                -webkit-appearance: none;
                margin: 0;
            }
            input[type=number] {
                -moz-appearance: textfield;
            }
        </style>
    </head>
    <body style="background-color: #1e1e1e; color: #ffffff;">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# ============================================================================
# 6. Layout 設定
# ============================================================================
# 先建立 timeline blocks（改為從 ALL_EVENTS 生成，避免手動重複）
timeline_children = []
for e in ALL_EVENTS:
    year_label = f"民國 {e['year']} 年起"
    timeline_children.append(create_event_block(year_label, e["type"], e["text"]))

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    children=[
        html.Div([
            # 標題區
            html.Div([
                html.H1("國民小學學生歷年體位趨勢報告",
                       style={"textAlign": "center", "fontWeight": "bold", "marginBottom": "10px"}),
                html.P("專題研究：探討民國 95 年至 113 年國民體位統計數據之變遷、性別差異與未來預測",
                      style={"textAlign": "center", "color": "#aaaaaa", "marginBottom": "30px"}),
            ]),

            # 控制面板
            html.Div([
                # 左側：性別選擇
                html.Div([
                    html.Label("選擇比較組合：", style=LABEL_STYLE),
                    html.Div([
                        create_gender_checklist("male", MALE_COLOR),
                        create_gender_checklist("female", FEMALE_COLOR),
                    ], style={"display": "flex", "flexDirection": "row", "flex": 1}),
                ], style={**CARD_STYLE, "flex": "0 0 200px", "padding": "15px 20px",
                         "display": "flex", "flexDirection": "column"}),

                # 中間：相關資訊選擇
                html.Div([
                    html.Label("選擇相關資訊：", style=LABEL_STYLE),
                    html.Div([
                        dcc.Checklist(
                            id="impact-checklist",
                            options=[{"label": "政府政策", "value": "positive"},
                                    {"label": "社會事件", "value": "negative"}],
                            value=["positive", "negative"],
                            labelStyle={"display": "block", "marginBottom": "12px", "color": "#e0e0e0",
                                      "fontSize": "15px", "fontWeight": "bold"},
                        ),
                        # 新增：顯示預測資料勾選
                        dcc.Checklist(
                            id="show-prediction",
                            options=[{"label": "顯示預測資料 (114~116 年)", "value": "show"}],
                            value=[],
                            labelStyle={"display": "block", "marginTop": "8px", "color": "#e0e0e0",
                                      "fontSize": "14px"}
                        ),
                    ], style={"display": "flex", "flexDirection": "column", "flex": 1, "justifyContent": "center"}),
                ], style={**CARD_STYLE, "flex": "0 0 160px", "padding": "15px 20px",
                         "display": "flex", "flexDirection": "column"}),

                # 右側：年份範圍選擇
                html.Div([
                    html.Label("選擇年份範圍：", style={**LABEL_STYLE, "marginBottom": "12px"}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Span("民國 ", style={"marginRight": "4px"}),
                                dcc.Input(id="start-year-input", type="number", step=1, value=MIN_YEAR, style=INPUT_STYLE),
                                html.Span(" 年 至 民國 ", style={"margin": "0 6px"}),
                                dcc.Input(id="end-year-input", type="number", step=1, value=MAX_YEAR, style=INPUT_STYLE),
                                html.Span(" 年", style={"marginLeft": "4px"}),
                            ], style={"display": "flex", "alignItems": "center", "justifyContent": "center"}),
                            html.Div(id="year-error-message", style={"minHeight": "20px", "marginTop": "5px", "textAlign": "center"}),
                        ], style={"marginBottom": "15px"}),
                        html.Div([
                            dmc.RangeSlider(
                                id="year-range-slider", min=MIN_YEAR, max=MAX_YEAR, step=1,
                                value=[MIN_YEAR, MAX_YEAR], minRange=0, pushOnOverlap=False,
                                color="violet", size="sm",
                                marks=[{"value": y, "label": str(y), "style": {
                                    "transform": "translateY(-22px) translateX(-50%)", "fontSize": "11px", "color": "#C1C2C5"
                                }} for y in ALL_YEARS],
                                styles={
                                    "root": {"padding": "0 10px", "marginTop": "0px", "marginBottom": "10px"},
                                    "track": {"backgroundColor": "#424242"},
                                    "thumb": {"backgroundColor": "#ffffff", "borderColor": "#7950F2", "borderWidth": "2px"},
                                    "mark": {"backgroundColor": "#2D2D2D", "borderColor": "#666666"},
                                },
                            ),
                        ], style={"flex": 1, "display": "flex", "flexDirection": "column", "justifyContent": "center"}),
                    ], style={"display": "flex", "flexDirection": "column", "flex": 1, "justifyContent": "space-between"}),
                ], style={**CARD_STYLE, "flex": 1, "padding": "20px 25px", "display": "flex", "flexDirection": "column"}),
            ], style={"display": "flex", "gap": "20px", "alignItems": "stretch", "marginBottom": "20px"}),

            # 趨勢折線圖
            dcc.Graph(id="trend-line-chart"),

            # 堆疊長條圖
            html.Div([
                html.Div([
                    html.H3("男生體位比例堆疊圖",
                           style={"textAlign": "center", "marginBottom": "20px", "color": MALE_COLOR, "fontSize": "22px"}),
                    dcc.Graph(id="stacked-bar-chart-male", config={"displayModeBar": False})
                ], style={**CARD_STYLE, "flex": "1", "minWidth": "450px"}),
                html.Div([
                    html.H3("女生體位比例堆疊圖",
                           style={"textAlign": "center", "marginBottom": "20px", "color": FEMALE_COLOR, "fontSize": "22px"}),
                    dcc.Graph(id="stacked-bar-chart-female", config={"displayModeBar": False})
                ], style={**CARD_STYLE, "flex": "1", "minWidth": "450px"}),
            ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap", "marginBottom": "20px"}),

            # 熱力圖（加入與堆疊圖相同位置與風格的標題）
            html.Div([
                html.Div([
                    html.H3("男生體位比例熱力圖",
                           style={"textAlign": "center", "marginBottom": "20px", "color": MALE_COLOR, "fontSize": "22px"}),
                    dcc.Graph(id="heatmap-male", config={"displayModeBar": False})
                ], style={**CARD_STYLE, "flex": "1", "minWidth": "450px"}),
                html.Div([
                    html.H3("女生體位比例熱力圖",
                           style={"textAlign": "center", "marginBottom": "20px", "color": FEMALE_COLOR, "fontSize": "22px"}),
                    dcc.Graph(id="heatmap-female", config={"displayModeBar": False})
                ], style={**CARD_STYLE, "flex": "1", "minWidth": "450px"}),
            ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap", "marginBottom": "20px"}),

        ], style={"padding": "20px 40px", "backgroundColor": DARK_BG, "minHeight": "100vh"}),
    ],
)

# ============================================================================
# 7. Callbacks
# ============================================================================

@app.callback(
    [Output("start-year-input", "value"), Output("end-year-input", "value"),
     Output("year-range-slider", "value"), Output("year-error-message", "children")],
    [Input("start-year-input", "value"), Input("end-year-input", "value"),
     Input("year-range-slider", "value")],
)
def sync_and_validate_years(start_in, end_in, slider_val):
    """同步和驗證年份輸入"""
    triggered_id = dash.ctx.triggered_id

    if triggered_id == "year-range-slider" and slider_val:
        return min(slider_val), max(slider_val), slider_val, ""

    if start_in is None or end_in is None:
        return start_in, end_in, dash.no_update, html.Span(
            "⚠️ 請填入完整的年份數字",
            style={"color": "#ff5252", "fontSize": "13px", "fontWeight": "bold"},
        )

    actual_start, actual_end = min(start_in, end_in), max(start_in, end_in)

    if not (MIN_YEAR <= actual_start <= MAX_YEAR and MIN_YEAR <= actual_end <= MAX_YEAR):
        return start_in, end_in, dash.no_update, html.Span(
            f"⚠️ 輸入超出範圍！請輸入民國 {MIN_YEAR} 年至 {MAX_YEAR} 年之間的數字",
            style={"color": "#ff5252", "fontSize": "13px", "fontWeight": "bold"},
        )

    return actual_start, actual_end, [actual_start, actual_end], ""


@app.callback(
    Output("trend-line-chart", "figure"),
    [Input("male-checklist", "value"), Input("female-checklist", "value"),
     Input("impact-checklist", "value"), Input("year-range-slider", "value"), Input("show-prediction", "value")],
)
def update_trend_chart(male_selected, female_selected, impact_selected, year_range, show_prediction_val):
    """更新趨勢折線圖，並可顯示事件標籤與線性回歸預測"""
    selected_groups = (male_selected or []) + (female_selected or [])
    show_positive = "positive" in (impact_selected or [])
    show_negative = "negative" in (impact_selected or [])
    show_prediction = "show" in (show_prediction_val or [])

    if not year_range:
        year_range = [MIN_YEAR, MAX_YEAR]

    filtered_df = df[(df["年度"] >= min(year_range)) & (df["年度"] <= max(year_range))]
    fig = go.Figure()

    # 無選擇時顯示提示
    if not selected_groups:
        fig.add_annotation(text="請至少勾選一種比較組合...", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=18, color="#ffffff"))
        fig.update_layout(paper_bgcolor=DARK_BG, plot_bgcolor=CARD_BG,
                         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showline=False),
                         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showline=False),
                         margin=dict(l=40, r=40, t=60, b=40))
        return fig

    # 為每個選中的組合準備資料
    for group in selected_groups:
        gender, category = group.split("_")
        sub_df = filtered_df[(filtered_df["性別"] == gender) & (filtered_df["體位類別"] == category)].copy()
        label_name = f"{'男生' if gender == '男' else '女生'} - {category}"
        color = COLOR_MAP.get(label_name, "#ffffff")

        # 建立 hover 資訊，包含性別、體位、比例（橫向呈現）
        gender_display = "男生" if gender == "男" else "女生"
        # customdata 為 2D list，每列為 [性別, 體位, 百分比]
        customdata = [[gender_display, category, float(pct)] for pct in sub_df["百分比"].values]

        fig.add_trace(go.Scatter(
            x=sub_df["年度"],
            y=sub_df["百分比"],
            mode="lines+markers",
            name=label_name,
            line=dict(color=color, width=3),
            marker=dict(size=8),
            customdata=customdata,
            hovertemplate="%{customdata[0]} - %{customdata[1]} - %{customdata[2]:.1f}%<extra></extra>"
        ))

    # 動態添加政策/事件標記（使用 ALL_EVENTS，並配合使用者勾選）
    display_min, display_max = min(year_range), max(year_range)
    for e in ALL_EVENTS:
        yr = e["year"]
        if not (display_min <= yr <= display_max):
            continue
        if e["type"] == "positive" and not show_positive:
            continue
        if e["type"] == "negative" and not show_negative:
            continue
        color = POLICY_COLOR if e["type"] == "positive" else EVENT_COLOR
        # 短的區域標記
        fig.add_vrect(x0=yr - 0.2, x1=yr + 0.2, fillcolor=color, opacity=0.35,
                      line_width=1, line_dash="dot", line_color=color)

    # 在對應年分上方以垂直文字顯示事件說明（使用 paper 座標，使文字不會被資料點遮蔽）
    # 多個同年事件時，向上堆疊
    for yr in sorted(EVENT_BY_YEAR.keys()):
        if not (display_min <= yr <= display_max):
            continue
        events = EVENT_BY_YEAR.get(yr, [])
        # 根據使用者選擇篩選事件類型
        events = [ev for ev in events if ((ev["type"] == "positive" and show_positive) or (ev["type"] == "negative" and show_negative))]
        for idx, ev in enumerate(events):
            ann_color = POLICY_COLOR if ev["type"] == "positive" else EVENT_COLOR
            # yref='paper' 並用 1.02 起始，堆疊間距 0.06
            fig.add_annotation(x=yr, y=1 + idx * 0.06, xref='x', yref='paper',
                   text="<br>".join(list(ev['text'])), showarrow=False, textangle=0,
                   font=dict(color=ann_color, size=12), align='center')

    # 若使用者要求預測，對每個選中組合做線性回歸並加入預測線（114~116 年）
    if show_prediction:
        for group in selected_groups:
            gender, category = group.split("_")
            sub_df_all = df[(df["性別"] == gender) & (df["體位類別"] == category) & (df["年度"] >= 99)].copy()
            years = sub_df_all["年度"].values
            vals = sub_df_all["百分比"].values
            if len(years) < 2:
                continue
            # 線性回歸（numpy polyfit）
            m, b = np.polyfit(years, vals, 1)
            x_pred = np.array(PRED_YEARS)
            y_pred = m * x_pred + b
            label_name = f"{'男生' if gender == '男' else '女生'} - {category} (預測)"
            color = COLOR_MAP.get(f"{'男生' if gender == '男' else '女生'} - {category}", "#ffffff")

            fig.add_trace(go.Scatter(
                x=x_pred, y=y_pred, mode='lines+markers', name=label_name,
                line=dict(color=color, dash='dash', width=2), marker=dict(symbol='x', size=8, color=color),
                hovertemplate=f"{label_name} - %{{x}} - %{{y:.1f}}%<extra></extra>"
            ))

    # 設定 x 軸刻度：若有預測則合併顯示預測年份
    if show_prediction:
        tickvals = sorted(list(set(ALL_YEARS + PRED_YEARS)))
    else:
        tickvals = ALL_YEARS

    x_min = min(display_min, min(PRED_YEARS) if show_prediction else display_min)
    x_max = max(display_max, max(PRED_YEARS) if show_prediction else display_max)

    fig.update_layout(
        title="歷年體位變遷趨勢", xaxis_title="年度 (民國)", yaxis_title="百分比 (%)",
        paper_bgcolor=DARK_BG, plot_bgcolor=CARD_BG, font=dict(color=TEXT_COLOR),
        hovermode="x unified", hoverlabel=dict(bgcolor="#2d2d2d", font_color="#ffffff", font_size=13),
        xaxis=dict(showgrid=True, gridcolor="#333333", tickmode="array", tickvals=tickvals,
               ticktext=[str(y) for y in tickvals], range=[x_min - 0.5, x_max + 0.5],
               showspikes=False),
        yaxis=dict(showgrid=True, gridcolor="#333333"),
        legend=dict(title="比較族群", bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=40, r=40, t=60, b=40),
    )
    return fig


@app.callback(Output("stacked-bar-chart-male", "figure"), [Input("year-range-slider", "value")])
def update_stacked_bar_male(year_range):
    """更新男生堆疊長條圖"""
    return create_stacked_bar_chart("male", year_range)


@app.callback(Output("stacked-bar-chart-female", "figure"), [Input("year-range-slider", "value")])
def update_stacked_bar_female(year_range):
    """更新女生堆疊長條圖"""
    return create_stacked_bar_chart("female", year_range)


@app.callback(Output("heatmap-male", "figure"), [Input("year-range-slider", "value")])
def update_heatmap_male(year_range):
    """更新男生熱力圖"""
    return create_heatmap("male", year_range)


@app.callback(Output("heatmap-female", "figure"), [Input("year-range-slider", "value")])
def update_heatmap_female(year_range):
    """更新女生熱力圖"""
    return create_heatmap("female", year_range)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)

import io
import os
import dash
from dash import dcc, html, Input, Output
import dash_mantine_components as dmc
import plotly.graph_objects as go
import pandas as pd

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
肥胖,男,106,17
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

df = pd.read_csv(io.StringIO(csv_data))
df["年度"] = df["年度"].astype(int)
df["百分比"] = df["百分比"].astype(float)

MIN_YEAR = 95
MAX_YEAR = int(df["年度"].max())
ALL_YEARS = list(range(MIN_YEAR, MAX_YEAR + 1))

# ============================================================================
# 2. 常數與配置
# ============================================================================

# 常數定義
BMI_CATEGORIES = ["過輕", "適中", "過重", "肥胖"]
COLORS = {
    "dark_bg": "#1e1e1e",
    "card_bg": "#2d2d2d",
    "text": "#ffffff",
    "male": "#29b6f6",
    "female": "#ff4081",
    "positive": "#4caf50",
    "negative": "#8A2BE2",
}

# 性別顏色映射
GENDER_COLORS = {
    "male": {"過輕": "#81d4fa", "適中": "#29b6f6", "過重": "#0288d1", "肥胖": "#01579b"},
    "female": {"過輕": "#ff80ab", "適中": "#ff4081", "過重": "#f50057", "肥胖": "#c51162"},
}

# 合併事件與標籤（單一數據來源）
EVENTS_DATA = [
    (95, "positive", "民國95年發布校園飲品及點心販售範圍規定"),
    (97, "positive", "民國97年推動健康促進學校計畫全面"),
    (98, "positive", "民國98年體適能檢測全面實施"),
    (99, "negative", "民國99年智慧型手機與行動網路普及"),
    (103, "positive", "民國103年推行健康成長密碼85210"),
    (106, "positive", "民國106年三章一Q政策與午餐食材登錄"),
    (107, "negative", "民國107年外送平台快速崛起"),
    (108, "positive", "民國108年108課綱正式上路"),
    (109, "negative", "民國109-112年COVID-19疫情衝擊"),
    (111, "positive", "民國111年生生用平板數位學習方案"),
    (111, "positive", "民國111年食農教育法三讀通過實施"),
]

# 預編譯事件查詢表
EVENT_MAP = {year: text for year, _, text in EVENTS_DATA}
POSITIVE_EVENT_YEARS = [year for year, event_type, _ in EVENTS_DATA if event_type == "positive"]
NEGATIVE_EVENT_YEARS = [(99, 99), (107, 107), (109, 112)]

# 性別選項
GENDER_OPTIONS = {
    "male": [{"label": cat, "value": f"男_{cat}"} for cat in BMI_CATEGORIES],
    "female": [{"label": cat, "value": f"女_{cat}"} for cat in BMI_CATEGORIES],
}

# ============================================================================
# 3. 樣式常數
# ============================================================================
INPUT_STYLE = {
    "width": "70px", "padding": "6px", "borderRadius": "4px",
    "border": "1px solid #555555", "backgroundColor": COLORS["card_bg"],
    "color": COLORS["text"], "textAlign": "center",
    "fontSize": "14px", "fontWeight": "bold",
}

CARD_STYLE = {
    "backgroundColor": COLORS["card_bg"], "padding": "20px",
    "borderRadius": "8px", "border": "1px solid #444",
}

LABEL_STYLE = {
    "fontWeight": "bold", "marginBottom": "10px", "display": "block",
}

# ============================================================================
# 4. 工具函數
# ============================================================================

def get_label_name(gender_char, category):
    """生成標籤名稱"""
    gender_label = "男生" if gender_char == "男" else "女生"
    return f"{gender_label} - {category}"


def get_color(label_name):
    """根據標籤獲取顏色"""
    for gender_key, categories in GENDER_COLORS.items():
        for cat, color in categories.items():
            if get_label_name("男" if gender_key == "male" else "女", cat) == label_name:
                return color
    return COLORS["text"]


def create_event_block(year_label, event_type, event_text):
    """生成統一的事件卡片"""
    bg_color = COLORS["positive"] if event_type == "positive" else COLORS["negative"]
    
    return html.Div([
        html.Div(year_label, style={
            "backgroundColor": bg_color, "color": COLORS["text"],
            "padding": "4px 12px", "borderRadius": "4px",
            "fontWeight": "bold", "fontSize": "13px",
            "display": "inline-block", "marginBottom": "6px",
        }),
        html.Div(event_text, style={"color": "#e0e0e0", "fontSize": "14px"}),
    ], style={
        "padding": "12px 15px", "backgroundColor": "#252525",
        "borderRadius": "6px", "borderLeft": f"4px solid {bg_color}",
        "marginBottom": "10px",
    })


def create_gender_checklist(gender_key, color):
    """生成性別選擇列表"""
    gender_label = "男生" if gender_key == "male" else "女生"
    
    return html.Div([
        html.Span(
            f"{gender_label}：",
            style={"fontWeight": "bold", "color": color, "marginBottom": "4px", "display": "block"}
        ),
        dcc.Checklist(
            id=f"{gender_key}-checklist",
            options=GENDER_OPTIONS[gender_key],
            value=[f"{gender_key[0]}_{gender_key}適中"],
            labelStyle={"display": "block", "marginBottom": "4px", "color": color},
        ),
    ], style={"flex": 1, "marginRight": "10px" if gender_key == "male" else 0})


def get_chart_layout(start_year, end_year):
    """返回圖表通用 layout 配置"""
    return {
        "barmode": "stack",
        "paper_bgcolor": COLORS["dark_bg"],
        "plot_bgcolor": COLORS["card_bg"],
        "font": dict(color=COLORS["text"], size=14),
        "margin": dict(l=40, r=40, t=20, b=40),
        "xaxis": dict(
            title=dict(text="年度 (民國)", font=dict(size=16)),
            showgrid=True, gridcolor="#333333",
            tickmode="array", tickvals=ALL_YEARS,
            ticktext=[str(y) for y in ALL_YEARS],
            range=[start_year - 0.5, end_year + 0.5],
            tickfont=dict(size=14)
        ),
        "yaxis": dict(
            title=dict(text="百分比 (%)", font=dict(size=16)),
            showgrid=True, gridcolor="#333333",
            range=[0, 105], tickfont=dict(size=14)
        ),
        "legend": dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1, font=dict(size=14)
        )
    }


def create_stacked_bar_chart(gender, year_range):
    """統一生成堆疊長條圖"""
    start_year, end_year = year_range
    gender_char = "男" if gender == "male" else "女"
    
    # 高效過濾
    filtered_df = df[(df["年度"].between(start_year, end_year)) & (df["性別"] == gender_char)]
    
    fig = go.Figure()
    for category in BMI_CATEGORIES:
        subset = filtered_df[filtered_df["體位類別"] == category]
        fig.add_trace(go.Bar(
            x=subset["年度"], y=subset["百分比"],
            name=category, marker_color=GENDER_COLORS[gender][category]
        ))
    
    fig.update_layout(get_chart_layout(start_year, end_year))
    return fig


def build_tooltip_data(year, selected_groups, filtered_df, show_positive, show_negative):
    """構建單年份的 tooltip 內容"""
    # 收集該年各組合的數據
    group_lines = []
    for group in selected_groups:
        gender, category = group.split("_")
        gender_label = "男生" if gender == "男" else "女生"
        match_row = filtered_df[
            (filtered_df["年度"] == year) &
            (filtered_df["性別"] == gender) &
            (filtered_df["體位類別"] == category)
        ]
        if not match_row.empty:
            group_lines.append(
                f"資       料：{gender_label}-{category}-{match_row['百分比'].values[0]:.1f}%"
            )
    
    # 獲取該年的事件
    hist_items = [
        text for y, t, text in EVENTS_DATA 
        if y <= year and ((t == "positive" and show_positive) or (t == "negative" and show_negative))
    ]
    hist_str = "<br>".join(hist_items) if hist_items else "無"
    
    return (
        f"<b>年       度：民國 {year} 年</b><br>"
        f"{'<br>'.join(group_lines)}<br>"
        f"<b>關鍵事件：</b>民國 {year} 年{EVENT_MAP.get(year, '無重大記事')}<br>"
        f"<b>歷史事件：</b>{hist_str}"
    )


# ============================================================================
# 5. Dash App 初始化
# ============================================================================
app = dash.Dash(__name__)
app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>
            input[type=number]::-webkit-inner-spin-button,
            input[type=number]::-webkit-outer-spin-button {{
                -webkit-appearance: none;
                margin: 0;
            }}
            input[type=number] {{
                -moz-appearance: textfield;
            }}
            .mantine-Slider-thumb:hover,
            .mantine-Slider-thumb:focus,
            .mantine-Slider-thumb:active {{
                z-index: 10 !important;
            }}
        </style>
    </head>
    <body style="background-color: {COLORS['dark_bg']}; color: {COLORS['text']}; font-family: sans-serif;">
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

# ============================================================================
# 6. Layout 設定
# ============================================================================
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    children=[
        html.Div([
            # 標題區
            html.Div([
                html.H1(
                    "國民小學學生歷年體位趨勢報告",
                    style={"textAlign": "center", "fontWeight": "bold", "marginBottom": "10px"}
                ),
                html.P(
                    "專題研究：探討民國 95 年至 113 年國民體位統計數據之變遷、性別差異與未來預測",
                    style={"textAlign": "center", "color": "#aaaaaa", "marginBottom": "30px"}
                ),
            ]),
            
            # 控制面板
            html.Div([
                # 左側：性別選擇
                html.Div([
                    html.Label("選擇比較組合：", style=LABEL_STYLE),
                    html.Div([
                        create_gender_checklist("male", COLORS["male"]),
                        create_gender_checklist("female", COLORS["female"]),
                    ], style={"display": "flex", "flexDirection": "row", "flex": 1}),
                ], style={
                    **CARD_STYLE, "flex": "0 0 200px",
                    "padding": "15px 20px", "display": "flex", "flexDirection": "column"
                }),
                
                # 中間：影響因素選擇
                html.Div([
                    html.Label("選擇影響因素：", style=LABEL_STYLE),
                    html.Div([
                        dcc.Checklist(
                            id="impact-checklist",
                            options=[
                                {"label": "政府政策", "value": "positive"},
                                {"label": "社會事件", "value": "negative"}
                            ],
                            value=["positive", "negative"],
                            labelStyle={
                                "display": "block", "marginBottom": "12px",
                                "color": "#e0e0e0", "fontSize": "15px", "fontWeight": "bold"
                            },
                        ),
                    ], style={
                        "display": "flex", "flexDirection": "column",
                        "flex": 1, "justifyContent": "center"
                    }),
                ], style={
                    **CARD_STYLE, "flex": "0 0 160px",
                    "padding": "15px 20px", "display": "flex", "flexDirection": "column"
                }),
                
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
                            html.Div(id="year-error-message", style={
                                "minHeight": "20px", "marginTop": "5px", "textAlign": "center"
                            }),
                        ], style={"marginBottom": "15px"}),
                        html.Div([
                            dmc.RangeSlider(
                                id="year-range-slider",
                                min=MIN_YEAR, max=MAX_YEAR, step=1,
                                value=[MIN_YEAR, MAX_YEAR],
                                minRange=0, pushOnOverlap=False,
                                color="violet", size="sm",
                                marks=[{
                                    "value": y, "label": str(y),
                                    "style": {
                                        "transform": "translateY(-22px) translateX(-50%)",
                                        "fontSize": "11px", "color": "#C1C2C5"
                                    }
                                } for y in ALL_YEARS],
                                styles={
                                    "root": {"padding": "0 10px", "marginTop": "0px", "marginBottom": "10px"},
                                    "track": {"backgroundColor": "#424242"},
                                    "thumb": {"backgroundColor": "#ffffff", "borderColor": "#7950F2", "borderWidth": "2px"},
                                    "mark": {"backgroundColor": "#2D2D2D", "borderColor": "#666666"},
                                },
                            ),
                        ], style={"flex": 1, "display": "flex", "flexDirection": "column", "justifyContent": "center"}),
                    ], style={"display": "flex", "flexDirection": "column", "flex": 1, "justifyContent": "space-between"}),
                ], style={
                    **CARD_STYLE, "flex": 1, "padding": "20px 25px",
                    "display": "flex", "flexDirection": "column"
                }),
            ], style={"display": "flex", "gap": "20px", "alignItems": "stretch", "marginBottom": "20px"}),
            
            # 趨勢折線圖
            dcc.Graph(id="trend-line-chart"),
            
            # 堆疊長條圖
            html.Div([
                html.Div([
                    html.H3(
                        "國民小學 - 男生體位比例堆疊圖",
                        style={
                            "textAlign": "center", "marginBottom": "20px",
                            "color": COLORS["male"], "fontSize": "22px"
                        }
                    ),
                    dcc.Graph(id="stacked-bar-chart-male", config={"displayModeBar": False})
                ], style={**CARD_STYLE, "flex": "1", "minWidth": "450px"}),
                html.Div([
                    html.H3(
                        "國民小學 - 女生體位比例堆疊圖",
                        style={
                            "textAlign": "center", "marginBottom": "20px",
                            "color": COLORS["female"], "fontSize": "22px"
                        }
                    ),
                    dcc.Graph(id="stacked-bar-chart-female", config={"displayModeBar": False})
                ], style={**CARD_STYLE, "flex": "1", "minWidth": "450px"}),
            ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap", "marginBottom": "20px"}),
            
            # 時間軸區塊
            html.Div([
                html.H3(
                    "政府政策與社會事件時間軸",
                    style={
                        "fontSize": "18px", "fontWeight": "bold",
                        "marginBottom": "15px", "marginTop": "25px",
                        "color": COLORS["text"]
                    }
                ),
                html.Div([
                    create_event_block("民國 95 年起", "positive", 
                                     "校園飲品及點心販售範圍：教育部正式訂定並嚴格規範校園內合作社及自動販賣機販售食品之營養成分、脂肪熱量比例..."),
                    create_event_block("民國 97 年起", "positive",
                                     "健康促進學校計畫全面推動：教育部全面推動健康促進學校計畫，輔導各級學校從組織運作、教學環境到社區結合..."),
                    create_event_block("民國 98 年起", "positive",
                                     "體適能檢測全面實施：教育部全面實施規範全國中小學學生體適能檢測，透過系統化資料追蹤與體位回饋..."),
                    create_event_block("民國 99 年起", "negative",
                                     "智慧型手機與行動網路普及：隨著智慧型手機與行動網路快速普及，學童接觸 3C 螢幕時間大幅增加..."),
                    create_event_block("民國 103 年起", "positive",
                                     "推行健康成長密碼85210：國民健康署強力推行「85210」健康口訣..."),
                    create_event_block("民國 106 年起", "positive",
                                     "三章一Q政策與午餐食材登錄：行政院全面推動「三章一Q」國產溯源食材政策..."),
                    create_event_block("民國 107 年起", "negative",
                                     "外送平台快速崛起：各類美食外送平台全面快速崛起，高熱量、高鈉之手搖飲與速食取得便利性大增..."),
                    create_event_block("民國 108 年起", "positive",
                                     "108 課綱正式上路：108課綱正式上路，強調素養導向與健康與體育領域的多元選修..."),
                    create_event_block("民國 109 - 112 年", "negative",
                                     "COVID-19 疫情衝擊：疫情爆發導致學校實施遠距教學與居家防疫，學童長期缺乏戶外運動..."),
                    create_event_block("民國 111 年起", "positive",
                                     "生生用平板方案 / 食農教育法實施：教育部推動「生生用平板」數位學習方案..."),
                ], style={**CARD_STYLE, "padding": "20px 25px", "marginTop": "15px"}),
            ], style={"marginTop": "15px"}),
        ], style={"padding": "20px 40px", "backgroundColor": COLORS["dark_bg"], "minHeight": "100vh"}),
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
     Input("impact-checklist", "value"), Input("year-range-slider", "value")],
)
def update_trend_chart(male_selected, female_selected, impact_selected, year_range):
    """更新趨勢折線圖"""
    selected_groups = (male_selected or []) + (female_selected or [])
    show_positive = "positive" in (impact_selected or [])
    show_negative = "negative" in (impact_selected or [])
    
    year_range = year_range or [MIN_YEAR, MAX_YEAR]
    start_year, end_year = min(year_range), max(year_range)
    
    fig = go.Figure()
    
    # 無選擇時顯示提示
    if not selected_groups:
        fig.add_annotation(
            text="請至少勾選一種比較組合...",
            xref="paper", yref="paper", x=0.5, y=0.5,
            showarrow=False, font=dict(size=18, color=COLORS["text"])
        )
        fig.update_layout(
            paper_bgcolor=COLORS["dark_bg"], plot_bgcolor=COLORS["card_bg"],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showline=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showline=False),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        return fig
    
    # 高效過濾數據
    filtered_df = df[df["年度"].between(start_year, end_year)]
    
    # 添加數據線
    for i, group in enumerate(selected_groups):
        gender, category = group.split("_")
        sub_df = filtered_df[
            (filtered_df["性別"] == gender) &
            (filtered_df["體位類別"] == category)
        ].copy()
        
        label_name = get_label_name(gender, category)
        color = get_color(label_name)
        
        # 第一個 trace 包含詳細 tooltip
        if i == 0:
            customdata = [
                build_tooltip_data(int(row["年度"]), selected_groups, filtered_df, show_positive, show_negative)
                for _, row in sub_df.iterrows()
            ]
            fig.add_trace(go.Scatter(
                x=sub_df["年度"], y=sub_df["百分比"],
                mode="lines+markers", name=label_name,
                line=dict(color=color, width=3), marker=dict(size=8),
                customdata=customdata,
                hovertemplate="<b>%{fullData.name} - %{y:.1f}%</b><extra></extra>"
            ))
        else:
            fig.add_trace(go.Scatter(
                x=sub_df["年度"], y=sub_df["百分比"],
                mode="lines+markers", name=label_name,
                line=dict(color=color, width=3), marker=dict(size=8),
                hoverinfo="skip"
            ))
    
    # 添加正面政策標記
    if show_positive:
        for yr in POSITIVE_EVENT_YEARS:
            if start_year <= yr <= end_year:
                fig.add_vrect(
                    x0=yr - 0.2, x1=yr + 0.2,
                    fillcolor=COLORS["positive"], opacity=0.35,
                    line_width=1, line_dash="dot", line_color=COLORS["positive"]
                )
    
    # 添加負面事件標記
    if show_negative:
        for y_start, y_end in NEGATIVE_EVENT_YEARS:
            if start_year <= y_end and end_year >= y_start:
                opacity = 0.4 if y_start == y_end else 0.25
                line_width = 1 if y_start == y_end else 0
                fig.add_vrect(
                    x0=y_start - 0.2, x1=y_end + 0.2,
                    fillcolor=COLORS["negative"], opacity=opacity,
                    line_width=line_width, line_dash="dot", line_color=COLORS["negative"]
                )
    
    # 更新圖表配置
    layout_config = get_chart_layout(start_year, end_year)
    layout_config.update({
        "title": "歷年體位變遷趨勢",
        "xaxis_title": "年度 (民國)",
        "yaxis_title": "百分比 (%)",
        "paper_bgcolor": COLORS["dark_bg"],
        "plot_bgcolor": COLORS["card_bg"],
        "font": dict(color=COLORS["text"]),
        "hovermode": "x unified",
        "hoverlabel": dict(bgcolor=COLORS["card_bg"], font_color=COLORS["text"], font_size=13),
        "xaxis": dict(
            showgrid=True, gridcolor="#333333",
            tickmode="array", tickvals=ALL_YEARS,
            ticktext=[str(y) for y in ALL_YEARS],
            range=[start_year - 0.5, end_year + 0.5]
        ),
        "yaxis": dict(showgrid=True, gridcolor="#333333"),
        "legend": dict(title="比較族群", bgcolor="rgba(0,0,0,0)"),
        "barmode": "group",
    })
    fig.update_layout(layout_config)
    return fig


@app.callback(
    Output("stacked-bar-chart-male", "figure"),
    [Input("year-range-slider", "value")]
)
def update_stacked_bar_male(year_range):
    """更新男生堆疊長條圖"""
    return create_stacked_bar_chart("male", year_range or [MIN_YEAR, MAX_YEAR])


@app.callback(
    Output("stacked-bar-chart-female", "figure"),
    [Input("year-range-slider", "value")]
)
def update_stacked_bar_female(year_range):
    """更新女生堆疊長條圖"""
    return create_stacked_bar_chart("female", year_range or [MIN_YEAR, MAX_YEAR])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)

import io
import os
import dash
from dash import dcc, html, Input, Output
import dash_mantine_components as dmc
import plotly.graph_objects as go
import pandas as pd

# ------------------------------------------------------------------------------
# 1. 原始資料與預處理解析（已排除全國、調整欄位名稱為「體位類別」）
# ------------------------------------------------------------------------------
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
df["性別體位組合Key"] = df["性別"] + "_" + df["體位類別"]

MIN_YEAR, MAX_YEAR = 95, int(df["年度"].max())

# 當年度關鍵事件對應字典
EVENT_MAP = {
    95: "發布校園飲品及點心販售範圍規定",
    97: "推動健康促進學校計畫全面",
    98: "全面實施體適能檢測",
    99: "智慧型手機與行動網路普及",
    103: "推行健康成長密碼85210",
    106: "三章一Q政策與午餐食材登錄",
    107: "外送平台快速崛起",
    108: "108 課綱正式上路",
    109: "COVID-19 疫情衝擊開始",
    110: "COVID-19 疫情期間生活型態改變",
    111: "生生用平板方案 / 食農教育法實施",
    112: "COVID-19 疫情解封與作息調整",
}

# 歷史事件完整列表
ALL_EVENTS = [
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

# UI 常數定義
DARK_BG, CARD_BG, TEXT_COLOR = "#1e1e1e", "#2d2d2d", "#ffffff"
MALE_COLOR, FEMALE_COLOR = "#29b6f6", "#ff4081"
MALE_OPTIONS = [
    {"label": cat, "value": f"男_{cat}"} for cat in ["過輕", "適中", "過重", "肥胖"]
]
FEMALE_OPTIONS = [
    {"label": cat, "value": f"女_{cat}"} for cat in ["過輕", "適中", "過重", "肥胖"]
]

COLOR_MAP = {
    "男生 - 過輕": "#81d4fa",
    "男生 - 適中": "#29b6f6",
    "男生 - 過重": "#0288d1",
    "男生 - 肥胖": "#01579b",
    "女生 - 過輕": "#ff80ab",
    "女生 - 適中": "#ff4081",
    "女生 - 過重": "#f50057",
    "女生 - 肥胖": "#c51162",
}

# ------------------------------------------------------------------------------
# 2. Dash App 設定
# ------------------------------------------------------------------------------
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
    <body style="background-color: {DARK_BG}; color: {TEXT_COLOR}; font-family: sans-serif;">
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

# ------------------------------------------------------------------------------
# 3. Layout 設定
# ------------------------------------------------------------------------------
input_style = {
    "width": "70px",
    "padding": "6px",
    "borderRadius": "4px",
    "border": "1px solid #555555",
    "backgroundColor": CARD_BG,
    "color": TEXT_COLOR,
    "textAlign": "center",
    "fontSize": "14px",
    "fontWeight": "bold",
}

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    children=[
        html.Div(
            [
                html.Div(
                    [
                        html.H1(
                            "國民小學學生歷年體位趨勢報告",
                            style={
                                "textAlign": "center",
                                "fontWeight": "bold",
                                "marginBottom": "10px",
                            },
                        ),
                        html.P(
                            "專題研究：探討民國 95 年至 113 年國民體位統計數據之變遷、性別差異與未來預測",
                            style={
                                "textAlign": "center",
                                "color": "#aaaaaa",
                                "marginBottom": "30px",
                            },
                        ),
                    ]
                ),
                # 上方控制面板外層容器
                html.Div(
                    [
                        # 左側：選擇比較組合
                        html.Div(
                            [
                                html.Label(
                                    "選擇比較組合：",
                                    style={
                                        "fontWeight": "bold",
                                        "marginBottom": "10px",
                                        "display": "block",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Span(
                                                    "男生：",
                                                    style={
                                                        "fontWeight": "bold",
                                                        "color": MALE_COLOR,
                                                        "marginBottom": "4px",
                                                        "display": "block",
                                                    },
                                                ),
                                                dcc.Checklist(
                                                    id="male-checklist",
                                                    options=MALE_OPTIONS,
                                                    value=["男_適中"],
                                                    labelStyle={
                                                        "display": "block",
                                                        "marginBottom": "4px",
                                                        "color": MALE_COLOR,
                                                    },
                                                ),
                                            ],
                                            style={"flex": 1, "marginRight": "10px"},
                                        ),
                                        html.Div(
                                            [
                                                html.Span(
                                                    "女生：",
                                                    style={
                                                        "fontWeight": "bold",
                                                        "color": FEMALE_COLOR,
                                                        "marginBottom": "4px",
                                                        "display": "block",
                                                    },
                                                ),
                                                dcc.Checklist(
                                                    id="female-checklist",
                                                    options=FEMALE_OPTIONS,
                                                    value=["女_適中"],
                                                    labelStyle={
                                                        "display": "block",
                                                        "marginBottom": "4px",
                                                        "color": FEMALE_COLOR,
                                                    },
                                                ),
                                            ],
                                            style={"flex": 1},
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "flexDirection": "row",
                                        "flex": 1,
                                    },
                                ),
                            ],
                            style={
                                "flex": "0 0 200px",
                                "backgroundColor": CARD_BG,
                                "padding": "15px 20px",
                                "borderRadius": "8px",
                                "border": "1px solid #444",
                                "display": "flex",
                                "flexDirection": "column",
                            },
                        ),
                        # 中間：選擇影響因素
                        html.Div(
                            [
                                html.Label(
                                    "選擇影響因素：",
                                    style={
                                        "fontWeight": "bold",
                                        "marginBottom": "10px",
                                        "display": "block",
                                    },
                                ),
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id="impact-checklist",
                                            options=[
                                                {"label": "政府政策", "value": "positive"},
                                                {"label": "社會事件", "value": "negative"},
                                            ],
                                            value=["positive", "negative"],
                                            labelStyle={
                                                "display": "block",
                                                "marginBottom": "12px",
                                                "color": "#e0e0e0",
                                                "fontSize": "15px",
                                                "fontWeight": "bold",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "flexDirection": "column",
                                        "flex": 1,
                                        "justifyContent": "center",
                                    },
                                ),
                            ],
                            style={
                                "flex": "0 0 160px",
                                "backgroundColor": CARD_BG,
                                "padding": "15px 20px",
                                "borderRadius": "8px",
                                "border": "1px solid #444",
                                "display": "flex",
                                "flexDirection": "column",
                            },
                        ),
                        # 右側：選擇年份範圍
                        html.Div(
                            [
                                html.Label(
                                    "選擇年份範圍：",
                                    style={
                                        "fontWeight": "bold",
                                        "marginBottom": "12px",
                                        "display": "block",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.Span(
                                                            "民國 ",
                                                            style={
                                                                "marginRight": "4px"
                                                            },
                                                        ),
                                                        dcc.Input(
                                                            id="start-year-input",
                                                            type="number",
                                                            step=1,
                                                            value=MIN_YEAR,
                                                            style=input_style,
                                                        ),
                                                        html.Span(
                                                            " 年 至 民國 ",
                                                            style={
                                                                "margin": "0 6px"
                                                            },
                                                        ),
                                                        dcc.Input(
                                                            id="end-year-input",
                                                            type="number",
                                                            step=1,
                                                            value=MAX_YEAR,
                                                            style=input_style,
                                                        ),
                                                        html.Span(
                                                            " 年",
                                                            style={
                                                                "marginLeft": "4px"
                                                            },
                                                        ),
                                                    ],
                                                    style={
                                                        "display": "flex",
                                                        "alignItems": "center",
                                                        "justifyContent": "center",
                                                    },
                                                ),
                                                html.Div(
                                                    id="year-error-message",
                                                    style={
                                                        "minHeight": "20px",
                                                        "marginTop": "5px",
                                                        "textAlign": "center",
                                                    },
                                                ),
                                            ],
                                            style={"marginBottom": "15px"},
                                        ),
                                        html.Div(
                                            [
                                                dmc.RangeSlider(
                                                    id="year-range-slider",
                                                    min=MIN_YEAR,
                                                    max=MAX_YEAR,
                                                    step=1,
                                                    value=[MIN_YEAR, MAX_YEAR],
                                                    minRange=0,
                                                    pushOnOverlap=False,
                                                    color="violet",
                                                    size="sm",
                                                    marks=[
                                                        {
                                                            "value": y,
                                                            "label": str(y),
                                                            "style": {
                                                                "transform": "translateY(-22px) translateX(-50%)",
                                                                "fontSize": "11px",
                                                                "color": "#C1C2C5",
                                                            },
                                                        }
                                                        for y in range(
                                                            MIN_YEAR,
                                                            MAX_YEAR + 1,
                                                        )
                                                    ],
                                                    styles={
                                                        "root": {
                                                            "padding": "0 10px",
                                                            "marginTop": "0px",
                                                            "marginBottom": "10px",
                                                        },
                                                        "track": {
                                                            "backgroundColor": "#424242"
                                                        },
                                                        "thumb": {
                                                            "backgroundColor": "#ffffff",
                                                            "borderColor": "#7950F2",
                                                            "borderWidth": "2px",
                                                        },
                                                        "mark": {
                                                            "backgroundColor": "#2D2D2D",
                                                            "borderColor": "#666666",
                                                        },
                                                    },
                                                ),
                                            ],
                                            style={
                                                "flex": 1,
                                                "display": "flex",
                                                "flexDirection": "column",
                                                "justifyContent": "center",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "flexDirection": "column",
                                        "flex": 1,
                                        "justifyContent": "space-between",
                                    },
                                ),
                            ],
                            style={
                                "flex": 1,
                                "backgroundColor": CARD_BG,
                                "padding": "20px 25px",
                                "borderRadius": "8px",
                                "border": "1px solid #444",
                                "display": "flex",
                                "flexDirection": "column",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "gap": "20px",
                        "alignItems": "stretch",
                        "marginBottom": "20px",
                    },
                ),
                # 折線圖輸出
                dcc.Graph(id="trend-line-chart"),
                # ★ 男生與女生堆疊長條圖（左：男生，右：女生）
                html.Div(
                    style={
                        "display": "flex",
                        "gap": "20px",
                        "flexWrap": "wrap",
                        "marginBottom": "20px",
                    },
                    children=[
                        # 左側：男生堆疊長條圖
                        html.Div(
                            style={
                                "flex": "1",
                                "minWidth": "450px",
                                "backgroundColor": CARD_BG,
                                "padding": "20px",
                                "borderRadius": "8px",
                                "border": "1px solid #444",
                            },
                            children=[
                                html.H3("國民小學 - 男生體位比例堆疊圖", style={"textAlign": "center", "marginBottom": "20px", "color": MALE_COLOR, "fontSize": "22px"}),
                                dcc.Graph(id="stacked-bar-chart-male", config={"displayModeBar": False})
                            ]
                        ),
                        # 右側：女生堆疊長條圖
                        html.Div(
                            style={
                                "flex": "1",
                                "minWidth": "450px",
                                "backgroundColor": CARD_BG,
                                "padding": "20px",
                                "borderRadius": "8px",
                                "border": "1px solid #444",
                            },
                            children=[
                                html.H3("國民小學 - 女生體位比例堆疊圖", style={"textAlign": "center", "marginBottom": "20px", "color": FEMALE_COLOR, "fontSize": "22px"}),
                                dcc.Graph(id="stacked-bar-chart-female", config={"displayModeBar": False})
                            ]
                        ),
                    ]
                ),
                # 政府政策與社會事件時間軸專區
                html.Div(
                    [
                        html.H3(
                            "政府政策與社會事件時間軸",
                            style={
                                "fontSize": "18px",
                                "fontWeight": "bold",
                                "marginBottom": "15px",
                                "marginTop": "25px",
                                "color": "#ffffff",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            "民國 95 年起",
                                            style={
                                                "backgroundColor": "#4caf50",
                                                "color": "#ffffff",
                                                "padding": "4px 12px",
                                                "borderRadius": "4px",
                                                "fontWeight": "bold",
                                                "fontSize": "13px",
                                                "display": "inline-block",
                                                "marginBottom": "6px",
                                            },
                                        ),
                                        html.Div(
                                            "校園飲品及點心販售範圍：教育部正式訂定並發布校園飲品及點心販售範圍規定，嚴格規範校園內合作社及自動販賣機販售食品之營養成分、脂肪熱量比例與糖分上限。",
                                            style={
                                                "color": "#e0e0e0",
                                                "fontSize": "14px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "padding": "12px 15px",
                                        "backgroundColor": "#252525",
                                        "borderRadius": "6px",
                                        "borderLeft": "4px solid #4caf50",
                                        "marginBottom": "10px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            "民國 97 年起",
                                            style={
                                                "backgroundColor": "#4caf50",
                                                "color": "#ffffff",
                                                "padding": "4px 12px",
                                                "borderRadius": "4px",
                                                "fontWeight": "bold",
                                                "fontSize": "13px",
                                                "display": "inline-block",
                                                "marginBottom": "6px",
                                            },
                                        ),
                                        html.Div(
                                            "健康促進學校計畫全面推動：教育部全面推動健康促進學校計畫，輔導各級學校從組織運作、教學環境到社區結合，全面深化校園健康自主管理與均衡飲食教育。",
                                            style={
                                                "color": "#e0e0e0",
                                                "fontSize": "14px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "padding": "12px 15px",
                                        "backgroundColor": "#252525",
                                        "borderRadius": "6px",
                                        "borderLeft": "4px solid #4caf50",
                                        "marginBottom": "10px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            "民國 98 年起",
                                            style={
                                                "backgroundColor": "#4caf50",
                                                "color": "#ffffff",
                                                "padding": "4px 12px",
                                                "borderRadius": "4px",
                                                "fontWeight": "bold",
                                                "fontSize": "13px",
                                                "display": "inline-block",
                                                "marginBottom": "6px",
                                            },
                                        ),
                                        html.Div(
                                            "體適能檢測全面實施：教育部全面實施並規範全國中小學學生體適能檢測，透過系統化資料追蹤與體位回饋，促使各校更加重視體育授課品質。",
                                            style={
                                                "color": "#e0e0e0",
                                                "fontSize": "14px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "padding": "12px 15px",
                                        "backgroundColor": "#252525",
                                        "borderRadius": "6px",
                                        "borderLeft": "4px solid #4caf50",
                                        "marginBottom": "10px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            "民國 99 年起",
                                            style={
                                                "backgroundColor": "#8A2BE2",
                                                "color": "#ffffff",
                                                "padding": "4px 12px",
                                                "borderRadius": "4px",
                                                "fontWeight": "bold",
                                                "fontSize": "13px",
                                                "display": "inline-block",
                                                "marginBottom": "6px",
                                            },
                                        ),
                                        html.Div(
                                            "智慧型手機與行動網路普及：學童接觸 3C 螢幕時間大幅增加，戶外活動逐漸減少。",
                                            style={
                                                "color": "#e0e0e0",
                                                "fontSize": "14px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "padding": "12px 15px",
                                        "backgroundColor": "#252525",
                                        "borderRadius": "6px",
                                        "borderLeft": "4px solid #8A2BE2",
                                        "marginBottom": "10px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            "民國 103 年起",
                                            style={
                                                "backgroundColor": "#4caf50",
                                                "color": "#ffffff",
                                                "padding": "4px 12px",
                                                "borderRadius": "4px",
                                                "fontWeight": "bold",
                                                "fontSize": "13px",
                                                "display": "inline-block",
                                                "marginBottom": "6px",
                                            },
                                        ),
                                        html.Div(
                                            "推行健康成長密碼85210：衛福部國健署推行健康口訣與減重計畫（85210），有效引導建立健康生活習慣。",
                                            style={
                                                "color": "#e0e0e0",
                                                "fontSize": "14px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "padding": "12px 15px",
                                        "backgroundColor": "#252525",
                                        "borderRadius": "6px",
                                        "borderLeft": "4px solid #4caf50",
                                        "marginBottom": "10px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            "民國 106 年起",
                                            style={
                                                "backgroundColor": "#4caf50",
                                                "color": "#ffffff",
                                                "padding": "4px 12px",
                                                "borderRadius": "4px",
                                                "fontWeight": "bold",
                                                "fontSize": "13px",
                                                "display": "inline-block",
                                                "marginBottom": "6px",
                                            },
                                        ),
                                        html.Div(
                                            "三章一Q政策與午餐食材登錄：全面推動校園午餐使用三章一Q國產農產品溯源標章。",
                                            style={
                                                "color": "#e0e0e0",
                                                "fontSize": "14px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "padding": "12px 15px",
                                        "backgroundColor": "#252525",
                                        "borderRadius": "6px",
                                        "borderLeft": "4px solid #4caf50",
                                        "marginBottom": "10px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            "民國 107 年起",
                                            style={
                                                "backgroundColor": "#8A2BE2",
                                                "color": "#ffffff",
                                                "padding": "4px 12px",
                                                "borderRadius": "4px",
                                                "fontWeight": "bold",
                                                "fontSize": "13px",
                                                "display": "inline-block",
                                                "marginBottom": "6px",
                                            },
                                        ),
                                        html.Div(
                                            "外送平台快速崛起：改變家庭飲食習慣，高熱量外食與加工食品取得更為便利。",
                                            style={
                                                "color": "#e0e0e0",
                                                "fontSize": "14px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "padding": "12px 15px",
                                        "backgroundColor": "#252525",
                                        "borderRadius": "6px",
                                        "borderLeft": "4px solid #8A2BE2",
                                        "marginBottom": "10px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            "民國 108 年起",
                                            style={
                                                "backgroundColor": "#4caf50",
                                                "color": "#ffffff",
                                                "padding": "4px 12px",
                                                "borderRadius": "4px",
                                                "fontWeight": "bold",
                                                "fontSize": "13px",
                                                "display": "inline-block",
                                                "marginBottom": "6px",
                                            },
                                        ),
                                        html.Div(
                                            "108 課綱正式上路：強調核心素養導向，提供學校多元規劃戶外探索與體育課程空間。",
                                            style={
                                                "color": "#e0e0e0",
                                                "fontSize": "14px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "padding": "12px 15px",
                                        "backgroundColor": "#252525",
                                        "borderRadius": "6px",
                                        "borderLeft": "4px solid #4caf50",
                                        "marginBottom": "10px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            "民國 109 - 112 年",
                                            style={
                                                "backgroundColor": "#8A2BE2",
                                                "color": "#ffffff",
                                                "padding": "4px 12px",
                                                "borderRadius": "4px",
                                                "fontWeight": "bold",
                                                "fontSize": "13px",
                                                "display": "inline-block",
                                                "marginBottom": "6px",
                                            },
                                        ),
                                        html.Div(
                                            "COVID-19 疫情衝擊：遠距教學與室內外活動受限，運動量驟降導致肥胖率波動。",
                                            style={
                                                "color": "#e0e0e0",
                                                "fontSize": "14px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "padding": "12px 15px",
                                        "backgroundColor": "#252525",
                                        "borderRadius": "6px",
                                        "borderLeft": "4px solid #8A2BE2",
                                        "marginBottom": "10px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            "民國 111 年起",
                                            style={
                                                "backgroundColor": "#4caf50",
                                                "color": "#ffffff",
                                                "padding": "4px 12px",
                                                "borderRadius": "4px",
                                                "fontWeight": "bold",
                                                "fontSize": "13px",
                                                "display": "inline-block",
                                                "marginBottom": "6px",
                                            },
                                        ),
                                        html.Div(
                                            "生生用平板方案 / 食農教育法實施：推動數位學習與均衡飲食教育。",
                                            style={
                                                "color": "#e0e0e0",
                                                "fontSize": "14px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "padding": "12px 15px",
                                        "backgroundColor": "#252525",
                                        "borderRadius": "6px",
                                        "borderLeft": "4px solid #4caf50",
                                    },
                                ),
                            ],
                            style={
                                "backgroundColor": CARD_BG,
                                "padding": "20px 25px",
                                "borderRadius": "8px",
                                "border": "1px solid #444",
                            },
                        ),
                    ],
                    style={"marginTop": "15px"},
                ),
            ],
            style={
                "padding": "20px 40px",
                "backgroundColor": DARK_BG,
                "minHeight": "100vh",
            },
        )
    ],
)

# ------------------------------------------------------------------------------
# 4. Callbacks
# ------------------------------------------------------------------------------


@app.callback(
    [
        Output("start-year-input", "value"),
        Output("end-year-input", "value"),
        Output("year-range-slider", "value"),
        Output("year-error-message", "children"),
    ],
    [
        Input("start-year-input", "value"),
        Input("end-year-input", "value"),
        Input("year-range-slider", "value"),
    ],
)
def sync_and_validate_years(start_in, end_in, slider_val):
    triggered_id = dash.ctx.triggered_id

    if triggered_id == "year-range-slider" and slider_val:
        real_start = min(slider_val)
        real_end = max(slider_val)
        return real_start, real_end, slider_val, ""

    if start_in is None or end_in is None:
        return (
            start_in,
            end_in,
            dash.no_update,
            html.Span(
                "⚠️ 請填入完整的年份數字",
                style={"color": "#ff5252", "fontSize": "13px", "fontWeight": "bold"},
            ),
        )

    actual_start = min(start_in, end_in)
    actual_end = max(start_in, end_in)

    if not (
        MIN_YEAR <= actual_start <= MAX_YEAR
        and MIN_YEAR <= actual_end <= MAX_YEAR
    ):
        err = f"⚠️ 輸入超出範圍！請輸入民國 {MIN_YEAR} 年至 {MAX_YEAR} 年之間的數字"
        return (
            start_in,
            end_in,
            dash.no_update,
            html.Span(
                err,
                style={"color": "#ff5252", "fontSize": "13px", "fontWeight": "bold"},
            ),
        )

    return actual_start, actual_end, [actual_start, actual_end], ""


@app.callback(
    Output("trend-line-chart", "figure"),
    [
        Input("male-checklist", "value"),
        Input("female-checklist", "value"),
        Input("impact-checklist", "value"),
        Input("year-range-slider", "value"),
    ],
)
def update_trend_chart(male_selected, female_selected, impact_selected, year_range):
    selected_groups = (male_selected or []) + (female_selected or [])
    selected_impacts = impact_selected or []
    show_positive = "positive" in selected_impacts
    show_negative = "negative" in selected_impacts
    
    fig = go.Figure()

    if not year_range:
        year_range = [MIN_YEAR, MAX_YEAR]

    filtered_df = df[
        (df["年度"] >= min(year_range)) & (df["年度"] <= max(year_range))
    ]

    if not selected_groups:
        fig.add_annotation(
            text="請至少勾選一種比較組合...",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=18, color="#ffffff"),
        )
        fig.update_layout(
            paper_bgcolor=DARK_BG,
            plot_bgcolor=CARD_BG,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                showline=False,
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                showline=False,
            ),
            margin=dict(l=40, r=40, t=60, b=40),
        )
        return fig

    for i, group in enumerate(selected_groups):
        parts = group.split("_")
        gender_prefix = parts[0]
        category = parts[1]
        
        sub_df = filtered_df[
            (filtered_df["性別"] == gender_prefix)
            & (filtered_df["體位類別"] == category)
        ].copy()
        
        label_name = f"{'男生' if gender_prefix == '男' else '女生'} - {category}"
        color = COLOR_MAP.get(label_name, "#ffffff")

        if i == 0:
            customdata_rows = []
            for _, row in sub_df.iterrows():
                yr = int(row["年度"])
                ev = EVENT_MAP.get(yr, "無重大記事")
                
                # 收集所有目前勾選群組的百分比資料
                group_lines = []
                for g in selected_groups:
                    gp = g.split("_")
                    gp_gender = "男生" if gp[0] == "男" else "女生"
                    gp_cat = gp[1]
                    match_row = filtered_df[
                        (filtered_df["年度"] == yr)
                        & (filtered_df["性別"] == gp[0])
                        & (filtered_df["體位類別"] == gp_cat)
                    ]
                    if not match_row.empty:
                        val = match_row["百分比"].values[0]
                        group_lines.append(f"資       料：{gp_gender}-{gp_cat}-{val:.1f}%")
                
                # 篩選該年度之前（含當年度）的歷史事件
                hist_items = []
                for ey, et, etxt in ALL_EVENTS:
                    if ey <= yr:
                        if et == "positive" and show_positive:
                            hist_items.append(etxt)
                        elif et == "negative" and show_negative:
                            hist_items.append(etxt)
                
                if hist_items:
                    formatted_hist = []
                    for idx, h_text in enumerate(hist_items):
                        if idx == 0:
                            formatted_hist.append(h_text)
                        else:
                            # 進行文字對齊排版
                            formatted_hist.append("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + h_text)
                    hist_str = "<br>".join(formatted_hist)
                else:
                    hist_str = "無"
                
                group_lines_str = "<br>".join(group_lines)
                
                # 依照使用者指定的格式與順序組合
                tooltip_block = (
                    f"<b>年       度：民國 {yr} 年</b><br>"
                    f"{group_lines_str}<br>"
                    f"<b>關鍵事件：</b>民國 {yr} 年{ev}<br>"
                    f"<b>歷史事件：</b>{hist_str}"
                )
                customdata_rows.append(tooltip_block)

            fig.add_trace(
                go.Scatter(
                    x=sub_df["年度"],
                    y=sub_df["百分比"],
                    mode="lines+markers",
                    name=label_name,
                    line=dict(color=color, width=3),
                    marker=dict(size=8),
                    customdata=customdata_rows,
                    hovertemplate="%{customdata}<extra></extra>",
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=sub_df["年度"],
                    y=sub_df["百分比"],
                    mode="lines+markers",
                    name=label_name,
                    line=dict(color=color, width=3),
                    marker=dict(size=8),
                    hoverinfo="skip",
                )
            )

    # --- 政府政策影響因素標記 ---
    if show_positive:
        for yr_pos in [95, 97, 98, 103, 106, 108, 111]:
            if min(year_range) <= yr_pos <= max(year_range):
                fig.add_vrect(
                    x0=yr_pos - 0.2, x1=yr_pos + 0.2,
                    fillcolor="#4caf50", opacity=0.35,
                    line_width=1, line_dash="dot", line_color="#4caf50",
                )

    # --- 社會事件影響因素標記 ---
    if show_negative:
        if min(year_range) <= 99 <= max(year_range):
            fig.add_vrect(
                x0=98.8, x1=99.2,
                fillcolor="#8A2BE2", opacity=0.4,
                line_width=1, line_dash="dot", line_color="#8A2BE2",
            )
        if min(year_range) <= 107 <= max(year_range):
            fig.add_vrect(
                x0=106.8, x1=107.2,
                fillcolor="#8A2BE2", opacity=0.4,
                line_width=1, line_dash="dot", line_color="#8A2BE2",
            )
        if max(year_range) >= 109 and min(year_range) <= 112:
            fig.add_vrect(
                x0=108.8, x1=112.2,
                fillcolor="#8A2BE2", opacity=0.25,
                line_width=0,
            )

    all_years = list(range(95, 114))
    fig.update_layout(
        title="歷年體位變遷趨勢",
        xaxis_title="年度 (民國)",
        yaxis_title="百分比 (%)",
        paper_bgcolor=DARK_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_COLOR),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#2d2d2d", font_color="#ffffff", font_size=13),
        xaxis=dict(
            showgrid=True,
            gridcolor="#333333",
            tickmode="array",
            tickvals=all_years,
            ticktext=[str(y) for y in all_years],
            range=[min(year_range) - 0.5, max(year_range) + 0.5],
        ),
        yaxis=dict(showgrid=True, gridcolor="#333333"),
        legend=dict(title="比較族群", bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=40, r=40, t=60, b=40),
    )

    return fig
# ------------------------------------------------------------------------------
# 左側：男生專用堆疊長條圖 Callback
# ------------------------------------------------------------------------------
@app.callback(
    Output("stacked-bar-chart-male", "figure"),
    [Input("year-range-slider", "value")]
)
def update_stacked_bar_male(year_range):
    start_y, end_y = year_range
    df_filtered = df[(df["年度"] >= start_y) & (df["年度"] <= end_y) & (df["性別"] == "男")]
    
    categories = ["過輕", "適中", "過重", "肥胖"]
    male_colors = {"過輕": "#81d4fa", "適中": "#29b6f6", "過重": "#0288d1", "肥胖": "#01579b"}
    
    fig = go.Figure()
    for cat in categories:
        df_sub = df_filtered[df_filtered["體位類別"] == cat]
        fig.add_trace(go.Bar(
            x=df_sub["年度"],
            y=df_sub["百分比"],
            name=cat,
            marker_color=male_colors[cat]
        ))
        
    all_years = list(range(96, 114))
    fig.update_layout(
        barmode='stack',
        paper_bgcolor=DARK_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_COLOR, size=14),
        margin=dict(l=40, r=40, t=20, b=40),
        xaxis=dict(
            title=dict(text="年度 (民國)", font=dict(size=16)),
            showgrid=True,
            gridcolor="#333333",
            tickmode="array",
            tickvals=all_years,
            ticktext=[str(y) for y in all_years],
            range=[start_y - 0.5, end_y + 0.5],
            tickfont=dict(size=14)
        ),
        yaxis=dict(title=dict(text="百分比 (%)", font=dict(size=16)), showgrid=True, gridcolor="#333333", range=[0, 105], tickfont=dict(size=14)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=14))
    )
    return fig

# ------------------------------------------------------------------------------
# 右側：女生專用堆疊長條圖 Callback
# ------------------------------------------------------------------------------
@app.callback(
    Output("stacked-bar-chart-female", "figure"),
    [Input("year-range-slider", "value")]
)
def update_stacked_bar_female(year_range):
    start_y, end_y = year_range
    df_filtered = df[(df["年度"] >= start_y) & (df["年度"] <= end_y) & (df["性別"] == "女")]
    
    categories = ["過輕", "適中", "過重", "肥胖"]
    female_colors = {"過輕": "#ff80ab", "適中": "#ff4081", "過重": "#f50057", "肥胖": "#c51162"}
    
    fig = go.Figure()
    for cat in categories:
        df_sub = df_filtered[df_filtered["體位類別"] == cat]
        fig.add_trace(go.Bar(
            x=df_sub["年度"],
            y=df_sub["百分比"],
            name=cat,
            marker_color=female_colors[cat]
        ))
        
    all_years = list(range(96, 114))
    fig.update_layout(
        barmode='stack',
        paper_bgcolor=DARK_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_COLOR, size=14),
        margin=dict(l=40, r=40, t=20, b=40),
        xaxis=dict(
            title=dict(text="年度 (民國)", font=dict(size=16)),
            showgrid=True,
            gridcolor="#333333",
            tickmode="array",
            tickvals=all_years,
            ticktext=[str(y) for y in all_years],
            range=[start_y - 0.5, end_y + 0.5],
            tickfont=dict(size=14)
        ),
        yaxis=dict(title=dict(text="百分比 (%)", font=dict(size=16)), showgrid=True, gridcolor="#333333", range=[0, 105], tickfont=dict(size=14)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=14))
    )
    return fig

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)

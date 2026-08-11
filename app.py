import io
import os
import dash
from dash import dcc, html, Input, Output
import dash_mantine_components as dmc
import plotly.graph_objects as go
import pandas as pd

# ------------------------------------------------------------------------------
# 1. 原始資料與預處理解析
# ------------------------------------------------------------------------------
csv_data = """年度,性別,體位類別,百分比
96,男,過輕,18.5
96,女,過輕,20.1
96,男,適中,53.2
96,女,適中,58.1
96,男,過重,14.5
96,女,過重,12.0
96,男,肥胖,13.8
96,女,肥胖,9.8
97,男,過輕,18.8
97,女,過輕,20.3
97,男,適中,52.9
97,女,適中,57.9
97,男,過重,14.4
97,女,過重,12.1
97,男,肥胖,13.9
97,女,肥胖,9.7
98,男,過輕,19.0
98,女,過輕,20.5
98,男,適中,52.5
98,女,適中,57.5
98,男,過重,14.6
98,女,過重,12.2
98,男,肥胖,13.9
98,女,肥胖,9.8
99,男,過輕,7.1
99,女,過輕,7.3
99,男,適中,62.5
99,女,適中,63.2
99,男,過重,15.2
99,女,過重,12.8
99,男,肥胖,15.2
99,女,肥胖,11.7
100,男,過輕,7.2
100,女,過輕,7.4
100,男,適中,62.3
100,女,適中,63.0
100,男,過重,15.4
100,女,過重,13.0
100,男,肥胖,15.1
100,女,肥胖,11.6
101,男,過輕,7.0
101,女,過輕,7.2
101,男,適中,62.8
101,女,適中,63.5
101,男,過重,15.1
101,女,過重,12.7
101,男,肥胖,15.1
101,女,肥胖,11.6
102,男,過輕,6.9
102,女,過輕,7.1
102,男,適中,63.0
102,女,適中,63.8
102,男,過重,15.0
102,女,過重,12.6
102,男,肥胖,15.1
102,女,肥胖,11.5
103,男,過輕,6.8
103,女,過輕,7.0
103,男,適中,63.2
103,女,適中,64.0
103,男,過重,14.9
103,女,過重,12.5
103,男,肥胖,15.1
103,女,肥胖,11.5
104,男,過輕,6.7
104,女,過輕,6.9
104,男,適中,63.5
104,女,適中,64.2
104,男,過重,14.8
104,女,過重,12.4
104,男,肥胖,15.0
104,女,肥胖,11.5
105,男,過輕,6.6
105,女,過輕,6.8
105,男,適中,63.7
105,女,適中,64.5
105,男,過重,14.7
105,女,過重,12.3
105,男,肥胖,15.0
105,女,肥胖,11.4
106,男,過輕,6.5
106,女,過輕,6.7
106,男,適中,63.9
106,女,適中,64.7
106,男,過重,14.6
106,女,過重,12.2
106,男,肥胖,15.0
106,女,肥胖,11.4
107,男,過輕,6.4
107,女,過輕,6.6
107,男,適中,64.1
107,女,適中,65.0
107,男,過重,14.5
107,女,過重,12.1
107,男,肥胖,15.0
107,女,肥胖,11.3
108,男,過輕,6.5
108,女,過輕,6.7
108,男,適中,64.0
108,女,適中,64.8
108,男,過重,14.6
108,女,過重,12.2
108,男,肥胖,14.9
108,女,肥胖,11.3
109,男,過輕,6.6
109,女,過輕,6.8
109,男,適中,63.5
109,女,適中,64.2
109,男,過重,14.8
109,女,過重,12.4
109,男,肥胖,15.1
109,女,肥胖,11.6
110,男,過輕,6.7
110,女,過輕,6.9
110,男,適中,63.0
110,女,適中,63.8
110,男,過重,15.0
110,女,過重,12.6
110,男,肥胖,15.3
110,女,肥胖,11.7
111,男,過輕,6.6
111,女,過輕,6.8
111,男,適中,63.2
111,女,適中,64.0
111,男,過重,14.9
111,女,過重,12.5
111,男,肥胖,15.3
111,女,肥胖,11.7
112,男,過輕,6.5
112,女,過輕,6.7
112,男,適中,63.5
112,女,適中,64.3
112,男,過重,14.8
112,女,過重,12.4
112,男,肥胖,15.2
112,女,肥胖,11.6
113,男,過輕,6.4
113,女,過輕,6.6
113,男,適中,63.8
113,女,適中,64.6
113,男,過重,14.7
113,女,過重,12.3
113,男,肥胖,15.1
113,女,肥胖,11.5"""

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
                        html.H2(
                            "體位結構變遷折線圖",
                            style={
                                "textAlign": "center",
                                "fontWeight": "bold",
                                "marginBottom": "20px",
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
                                                {"label": "正向", "value": "positive"},
                                                {"label": "負向", "value": "negative"},
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
                # 歷史政策與關鍵事件時間軸專區
                html.Div(
                    [
                        html.H3(
                            "📚 歷史政策與關鍵事件時間軸",
                            style={
                                "fontSize": "18px",
                                "fontWeight": "bold",
                                "marginBottom": "15px",
                                "marginTop": "25px",
                                "color": "#4caf50",
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

    # --- 正向影響因素標記 ---
    if show_positive:
        for yr_pos in [95, 97, 98, 103, 106, 108, 111]:
            if min(year_range) <= yr_pos <= max(year_range):
                fig.add_vrect(
                    x0=yr_pos - 0.2, x1=yr_pos + 0.2,
                    fillcolor="#4caf50", opacity=0.35,
                    line_width=1, line_dash="dot", line_color="#4caf50",
                )

    # --- 負向影響因素標記 ---
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
        hovermode="closest",
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)

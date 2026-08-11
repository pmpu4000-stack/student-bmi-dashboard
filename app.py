import dash
from dash import dcc, html, Input, Output
import dash_mantine_components as dmc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import io

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
df["標示類別"] = df["性別"] + "生 - " + df["體位類別"]

MIN_YEAR, MAX_YEAR = int(df["年度"].min()), int(df["年度"].max())

# UI 常數定義
DARK_BG, CARD_BG, TEXT_COLOR = "#1e1e1e", "#2d2d2d", "#ffffff"
MALE_COLOR, FEMALE_COLOR = "#29b6f6", "#ff4081"

MALE_OPTIONS = [{"label": cat, "value": f"男_{cat}"} for cat in ["過輕", "適中", "過重", "肥胖"]]
FEMALE_OPTIONS = [{"label": cat, "value": f"女_{cat}"} for cat in ["過輕", "適中", "過重", "肥胖"]]

COLOR_MAP = {
    "男生 - 過輕": "#81d4fa", "男生 - 適中": "#29b6f6", "男生 - 過重": "#0288d1", "男生 - 肥胖": "#01579b",
    "女生 - 過輕": "#ff80ab", "女生 - 適中": "#ff4081", "女生 - 過重": "#f50057", "女生 - 肥胖": "#c51162",
}

# ------------------------------------------------------------------------------
# 2. Dash App 設定
# ------------------------------------------------------------------------------
app = dash.Dash(__name__)

app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>
            /* 隱藏輸入框微調按鈕 */
            input[type=number]::-webkit-inner-spin-button, 
            input[type=number]::-webkit-outer-spin-button {{ 
                -webkit-appearance: none; 
                margin: 0; 
            }}
            input[type=number] {{
                -moz-appearance: textfield;
            }}
            
            /* 重疊時讓滑鼠懸停或聚焦的白點提升至最上層，方便抓取拉開 */
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
'''

# ------------------------------------------------------------------------------
# 3. Layout 設定
# ------------------------------------------------------------------------------
input_style = {
    "width": "75px", "padding": "6px", "borderRadius": "4px",
    "border": "1px solid #555555", "backgroundColor": CARD_BG,
    "color": TEXT_COLOR, "textAlign": "center", "fontSize": "14px", "fontWeight": "bold"
}

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    children=[
        html.Div([
            # 主標題區塊
            html.Div([
                html.H1("國民小學學生歷年體位趨勢報告", style={"textAlign": "center", "fontWeight": "bold", "marginBottom": "10px"}),
                html.P("專題研究：探討民國 96 年至 113 年國民體位統計數據之變遷、性別差異與未來預測", style={"textAlign": "center", "color": "#aaaaaa", "marginBottom": "30px"}),
                html.H2("體位結構變遷折線圖", style={"textAlign": "center", "fontWeight": "bold", "marginBottom": "20px"}),
            ]),

            # 控制面板區塊
            html.Div([
                # 1. 選擇比較組合
                html.Div([
                    html.Label("選擇比較組合：", style={"fontWeight": "bold", "marginBottom": "10px", "display": "block"}),
                    html.Div([
                        html.Div([
                            html.Span("男生：", style={"fontWeight": "bold", "color": MALE_COLOR, "marginRight": "10px"}),
                            dcc.Checklist(id="male-checklist", options=MALE_OPTIONS, value=["男_適中"],
                                          labelStyle={'display': 'inline-block', 'marginRight': '12px', 'color': MALE_COLOR})
                        ], style={"display": "flex", "alignItems": "center", "marginRight": "20px"}),
                        
                        html.Div([
                            html.Span("女生：", style={"fontWeight": "bold", "color": FEMALE_COLOR, "marginRight": "10px"}),
                            dcc.Checklist(id="female-checklist", options=FEMALE_OPTIONS, value=["女_適中"],
                                          labelStyle={'display': 'inline-block', 'marginRight': '12px', 'color': FEMALE_COLOR})
                        ], style={"display": "flex", "alignItems": "center"}),
                    ], style={"display": "flex", "alignItems": "center", "marginTop": "5px"}),
                ], style={"flexShrink": 0, "marginRight": "40px"}),
                
                # 2. 選擇年份範圍
                html.Div([
                    html.Label("選擇年份範圍：", style={"fontWeight": "bold", "marginBottom": "10px", "display": "block"}),
                    html.Div([
                        html.Span("民國 ", style={"marginRight": "4px"}),
                        dcc.Input(id="start-year-input", type="number", step=1, value=MIN_YEAR, style=input_style),
                        html.Span(" 年  至 民國 ", style={"margin": "0 8px"}),
                        dcc.Input(id="end-year-input", type="number", step=1, value=MAX_YEAR, style=input_style),
                        html.Span(" 年", style={"marginLeft": "4px"})
                    ], style={"display": "flex", "alignItems": "center", "height": "32px", "marginBottom": "10px"}),
                    
                    # 錯誤警示訊息
                    html.Div(id="year-error-message", style={"minHeight": "20px"}),

                    # 紫色滑條（年度數字在上方、支援交叉與重疊抓取）
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
                                    "color": "#C1C2C5"
                                }
                            } 
                            for y in range(MIN_YEAR, MAX_YEAR + 1)
                        ],
                        styles={
                            "root": {"padding": "0 10px", "marginTop": "25px", "marginBottom": "10px"},
                            "track": {"backgroundColor": "#424242"},
                            "thumb": {"backgroundColor": "#ffffff", "borderColor": "#7950F2", "borderWidth": "2px"},
                            "mark": {"backgroundColor": "#2D2D2D", "borderColor": "#666666"}
                        }
                    )
                ], style={"flex": 1, "minWidth": "450px"}), 
            ], style={
                "display": "flex", "alignItems": "flex-start", "marginBottom": "20px", 
                "padding": "20px 25px", "backgroundColor": CARD_BG, "borderRadius": "8px", "border": "1px solid #444"
            }),

            # 圖表輸出
            dcc.Graph(id="trend-line-chart")
        ], style={"padding": "20px 40px", "backgroundColor": DARK_BG, "minHeight": "100vh"})
    ]
)

# ------------------------------------------------------------------------------
# 4. Callbacks
# ------------------------------------------------------------------------------

# 1. 雙向同步與輸入欄位驗證
@app.callback(
    [Output("start-year-input", "value"),
     Output("end-year-input", "value"),
     Output("year-range-slider", "value"),
     Output("year-error-message", "children")],
    [Input("start-year-input", "value"),
     Input("end-year-input", "value"),
     Input("year-range-slider", "value")]
)
def sync_and_validate_years(start_in, end_in, slider_val):
    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0] if dash.callback_context.triggered else None

    if triggered_id == "year-range-slider":
        real_start = min(slider_val)
        real_end = max(slider_val)
        return real_start, real_end, slider_val, ""
    
    if start_in is None or end_in is None:
        return start_in, end_in, dash.no_update, html.Span("⚠️ 請填入完整的年份數字", style={"color": "#ff5252", "fontSize": "13px", "fontWeight": "bold"})

    if not (MIN_YEAR <= start_in <= MAX_YEAR and MIN_YEAR <= end_in <= MAX_YEAR):
        err = f"⚠️ 輸入超出範圍！請輸入民國 {MIN_YEAR} 年至 {MAX_YEAR} 年之間的數字"
        return start_in, end_in, dash.no_update, html.Span(err, style={"color": "#ff5252", "fontSize": "13px", "fontWeight": "bold"})

    return start_in, end_in, [start_in, end_in], ""

# 2. 折線圖渲染（男女生分別對應獨立的邊框色）
@app.callback(
    Output("trend-line-chart", "figure"),
    [Input("male-checklist", "value"),
     Input("female-checklist", "value"),
     Input("year-range-slider", "value")]
)
def update_trend_chart(male_selected, female_selected, year_range):
    selected_groups = (male_selected or []) + (female_selected or [])
    
    if not selected_groups:
        fig = go.Figure()
        fig.add_annotation(
            text="請至少勾選一種比較組合（例如：男生 - 適中）",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color=TEXT_COLOR)
        )
        fig.update_layout(
            template="plotly_dark", paper_bgcolor=DARK_BG, plot_bgcolor=CARD_BG,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        return fig

    s_year, e_year = min(year_range), max(year_range)
    filtered_df = df[
        (df["性別體位組合Key"].isin(selected_groups)) &
        (df["年度"].between(s_year, e_year))
    ]
    
    fig = px.line(
        filtered_df, x="年度", y="百分比", color="標示類別",
        color_discrete_map=COLOR_MAP, markers=True,
        title="歷年體位變遷比較",
        labels={"百分比": "百分比 (%)", "標示類別": "比較族群"}
    )
    
    for trace in fig.data:
        group_name = trace.name
        border_color = "#29b6f6" if "男" in group_name else "#ff4081"
        
        trace.hovertemplate = (
            f"<div style='background-color: #242424; padding: 10px 14px; border-radius: 6px; "
            f"border: 2px solid {border_color}; box-shadow: 0px 4px 12px rgba(0,0,0,0.6); text-align: left;'>"
            f"<b style='color: {border_color}; font-size: 14px;'>%{{fullData.name}}</b><br>"
            f"<span style='color: #e0e0e0; font-size: 12px;'>民國 %{{x}} 年</span><br>"
            f"<span style='color: #ffffff; font-size: 13px;'>百分比：<b>%{{y:.1f}}%</b></span>"
            f"</div><extra></extra>"
        )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=DARK_BG,
        plot_bgcolor=CARD_BG,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(tickmode='linear', dtick=1, tickfont=dict(color=TEXT_COLOR)),
        yaxis=dict(tickfont=dict(color=TEXT_COLOR)),
        legend=dict(font=dict(color=TEXT_COLOR)),
        hovermode="closest"
    )
    
    return fig

# ------------------------------------------------------------------------------
# 5. 啟動服務
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)import dash
from dash import dcc, html, Input, Output
import dash_mantine_components as dmc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import io

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
df["標示類別"] = df["性別"] + "生 - " + df["體位類別"]

MIN_YEAR, MAX_YEAR = int(df["年度"].min()), int(df["年度"].max())

# UI 常數定義
DARK_BG, CARD_BG, TEXT_COLOR = "#1e1e1e", "#2d2d2d", "#ffffff"
MALE_COLOR, FEMALE_COLOR = "#29b6f6", "#ff4081"

MALE_OPTIONS = [{"label": cat, "value": f"男_{cat}"} for cat in ["過輕", "適中", "過重", "肥胖"]]
FEMALE_OPTIONS = [{"label": cat, "value": f"女_{cat}"} for cat in ["過輕", "適中", "過重", "肥胖"]]

COLOR_MAP = {
    "男生 - 過輕": "#81d4fa", "男生 - 適中": "#29b6f6", "男生 - 過重": "#0288d1", "男生 - 肥胖": "#01579b",
    "女生 - 過輕": "#ff80ab", "女生 - 適中": "#ff4081", "女生 - 過重": "#f50057", "女生 - 肥胖": "#c51162",
}

# ------------------------------------------------------------------------------
# 2. Dash App 設定
# ------------------------------------------------------------------------------
app = dash.Dash(__name__)

app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>
            /* 隱藏輸入框微調按鈕 */
            input[type=number]::-webkit-inner-spin-button, 
            input[type=number]::-webkit-outer-spin-button {{ 
                -webkit-appearance: none; 
                margin: 0; 
            }}
            input[type=number] {{
                -moz-appearance: textfield;
            }}
            
            /* 重疊時讓滑鼠懸停或聚焦的白點提升至最上層，方便抓取拉開 */
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
'''

# ------------------------------------------------------------------------------
# 3. Layout 設定
# ------------------------------------------------------------------------------
input_style = {
    "width": "75px", "padding": "6px", "borderRadius": "4px",
    "border": "1px solid #555555", "backgroundColor": CARD_BG,
    "color": TEXT_COLOR, "textAlign": "center", "fontSize": "14px", "fontWeight": "bold"
}

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    children=[
        html.Div([
            # 主標題區塊
            html.Div([
                html.H1("國民小學學生歷年體位趨勢報告", style={"textAlign": "center", "fontWeight": "bold", "marginBottom": "10px"}),
                html.P("專題研究：探討民國 96 年至 113 年國民體位統計數據之變遷、性別差異與未來預測", style={"textAlign": "center", "color": "#aaaaaa", "marginBottom": "30px"}),
                html.H2("體位結構變遷折線圖", style={"textAlign": "center", "fontWeight": "bold", "marginBottom": "20px"}),
            ]),

            # 控制面板區塊
            html.Div([
                # 1. 選擇比較組合
                html.Div([
                    html.Label("選擇比較組合：", style={"fontWeight": "bold", "marginBottom": "10px", "display": "block"}),
                    html.Div([
                        html.Div([
                            html.Span("男生：", style={"fontWeight": "bold", "color": MALE_COLOR, "marginRight": "10px"}),
                            dcc.Checklist(id="male-checklist", options=MALE_OPTIONS, value=["男_適中"],
                                          labelStyle={'display': 'inline-block', 'marginRight': '12px', 'color': MALE_COLOR})
                        ], style={"display": "flex", "alignItems": "center", "marginRight": "20px"}),
                        
                        html.Div([
                            html.Span("女生：", style={"fontWeight": "bold", "color": FEMALE_COLOR, "marginRight": "10px"}),
                            dcc.Checklist(id="female-checklist", options=FEMALE_OPTIONS, value=["女_適中"],
                                          labelStyle={'display': 'inline-block', 'marginRight': '12px', 'color': FEMALE_COLOR})
                        ], style={"display": "flex", "alignItems": "center"}),
                    ], style={"display": "flex", "alignItems": "center", "marginTop": "5px"}),
                ], style={"flexShrink": 0, "marginRight": "40px"}),
                
                # 2. 選擇年份範圍
                html.Div([
                    html.Label("選擇年份範圍：", style={"fontWeight": "bold", "marginBottom": "10px", "display": "block"}),
                    html.Div([
                        html.Span("民國 ", style={"marginRight": "4px"}),
                        dcc.Input(id="start-year-input", type="number", step=1, value=MIN_YEAR, style=input_style),
                        html.Span(" 年  至 民國 ", style={"margin": "0 8px"}),
                        dcc.Input(id="end-year-input", type="number", step=1, value=MAX_YEAR, style=input_style),
                        html.Span(" 年", style={"marginLeft": "4px"})
                    ], style={"display": "flex", "alignItems": "center", "height": "32px", "marginBottom": "10px"}),
                    
                    # 錯誤警示訊息
                    html.Div(id="year-error-message", style={"minHeight": "20px"}),

                    # 紫色滑條（年度數字在上方、支援交叉與重疊抓取）
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
                                    "color": "#C1C2C5"
                                }
                            } 
                            for y in range(MIN_YEAR, MAX_YEAR + 1)
                        ],
                        styles={
                            "root": {"padding": "0 10px", "marginTop": "25px", "marginBottom": "10px"},
                            "track": {"backgroundColor": "#424242"},
                            "thumb": {"backgroundColor": "#ffffff", "borderColor": "#7950F2", "borderWidth": "2px"},
                            "mark": {"backgroundColor": "#2D2D2D", "borderColor": "#666666"}
                        }
                    )
                ], style={"flex": 1, "minWidth": "450px"}), 
            ], style={
                "display": "flex", "alignItems": "flex-start", "marginBottom": "20px", 
                "padding": "20px 25px", "backgroundColor": CARD_BG, "borderRadius": "8px", "border": "1px solid #444"
            }),

            # 圖表輸出
            dcc.Graph(id="trend-line-chart")
        ], style={"padding": "20px 40px", "backgroundColor": DARK_BG, "minHeight": "100vh"})
    ]
)

# ------------------------------------------------------------------------------
# 4. Callbacks
# ------------------------------------------------------------------------------

# 1. 雙向同步與輸入欄位驗證
@app.callback(
    [Output("start-year-input", "value"),
     Output("end-year-input", "value"),
     Output("year-range-slider", "value"),
     Output("year-error-message", "children")],
    [Input("start-year-input", "value"),
     Input("end-year-input", "value"),
     Input("year-range-slider", "value")]
)
def sync_and_validate_years(start_in, end_in, slider_val):
    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0] if dash.callback_context.triggered else None

    if triggered_id == "year-range-slider":
        real_start = min(slider_val)
        real_end = max(slider_val)
        return real_start, real_end, slider_val, ""
    
    if start_in is None or end_in is None:
        return start_in, end_in, dash.no_update, html.Span("⚠️ 請填入完整的年份數字", style={"color": "#ff5252", "fontSize": "13px", "fontWeight": "bold"})

    if not (MIN_YEAR <= start_in <= MAX_YEAR and MIN_YEAR <= end_in <= MAX_YEAR):
        err = f"⚠️ 輸入超出範圍！請輸入民國 {MIN_YEAR} 年至 {MAX_YEAR} 年之間的數字"
        return start_in, end_in, dash.no_update, html.Span(err, style={"color": "#ff5252", "fontSize": "13px", "fontWeight": "bold"})

    return start_in, end_in, [start_in, end_in], ""

# 2. 折線圖渲染（男女生分別對應獨立的邊框色）
@app.callback(
    Output("trend-line-chart", "figure"),
    [Input("male-checklist", "value"),
     Input("female-checklist", "value"),
     Input("year-range-slider", "value")]
)
def update_trend_chart(male_selected, female_selected, year_range):
    selected_groups = (male_selected or []) + (female_selected or [])
    
    if not selected_groups:
        fig = go.Figure()
        fig.add_annotation(
            text="請至少勾選一種比較組合（例如：男生 - 適中）",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color=TEXT_COLOR)
        )
        fig.update_layout(
            template="plotly_dark", paper_bgcolor=DARK_BG, plot_bgcolor=CARD_BG,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        return fig

    s_year, e_year = min(year_range), max(year_range)
    filtered_df = df[
        (df["性別體位組合Key"].isin(selected_groups)) &
        (df["年度"].between(s_year, e_year))
    ]
    
    fig = px.line(
        filtered_df, x="年度", y="百分比", color="標示類別",
        color_discrete_map=COLOR_MAP, markers=True,
        title="歷年體位變遷比較",
        labels={"百分比": "百分比 (%)", "標示類別": "比較族群"}
    )
    
    for trace in fig.data:
        group_name = trace.name
        border_color = "#29b6f6" if "男" in group_name else "#ff4081"
        
        trace.hovertemplate = (
            f"<div style='background-color: #242424; padding: 10px 14px; border-radius: 6px; "
            f"border: 2px solid {border_color}; box-shadow: 0px 4px 12px rgba(0,0,0,0.6); text-align: left;'>"
            f"<b style='color: {border_color}; font-size: 14px;'>%{{fullData.name}}</b><br>"
            f"<span style='color: #e0e0e0; font-size: 12px;'>民國 %{{x}} 年</span><br>"
            f"<span style='color: #ffffff; font-size: 13px;'>百分比：<b>%{{y:.1f}}%</b></span>"
            f"</div><extra></extra>"
        )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=DARK_BG,
        plot_bgcolor=CARD_BG,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(tickmode='linear', dtick=1, tickfont=dict(color=TEXT_COLOR)),
        yaxis=dict(tickfont=dict(color=TEXT_COLOR)),
        legend=dict(font=dict(color=TEXT_COLOR)),
        hovermode="closest"
    )
    
    return fig

# ------------------------------------------------------------------------------
# 5. 啟動服務
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
import io
import os

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
df["指標類型"] = "BMI 體位"
df = df.rename(columns={"體位類別": "類別"})
df["年度"] = pd.to_numeric(df["年度"], errors="coerce")
df["百分比"] = pd.to_numeric(df["百分比"], errors="coerce")
df["性別"] = df["性別"].astype(str).str.strip()
df["類別"] = df["類別"].astype(str).str.strip()
df = df.dropna(subset=["年度", "百分比"])
df = df.sort_values(by=["指標類型", "類別", "性別", "年度"])

app = dash.Dash(__name__)
server = app.server

unique_genders = df["性別"].dropna().unique()
gender_options = [{"label": g, "value": g} for g in sorted(list(set(unique_genders)))]
gender_options.append({"label": "男與女共同顯示", "value": "男與女共同顯示"})

category_options = [
    { "label": "📊 全部指標總覽 (過輕/適中/過重/肥胖)", "value": "全部類別" }
] + [
    { "label": f"  •  {c}", "value": c }
    for c in df[df["指標類型"] == "BMI 體位"]["類別"].unique()
]

min_yr = int(df["年度"].min())
max_yr = int(df["年度"].max())
year_options = [{"label": f"民國 {yr} 年", "value": yr} for yr in sorted(df["年度"].unique())]
table_category_options = [{"label": c, "value": c} for c in df["類別"].unique()]

app.layout = html.Div(
    style={
        "fontFamily": "Microsoft JhengHei, sans-serif",
        "padding": "30px",
        "backgroundColor": "#FDFEFE"
    },
    children=[
        html.H1(
            "國民小學學生歷年體位趨勢報告",
            style={"textAlign": "center", "color": "#2C3E50", "marginBottom": "10px"},
        ),
        html.P(
            "專題研究：探討民國 96 年至 113 年國民體位統計數據之變遷、性別差異與未來預測",
            style={"textAlign": "center", "color": "#7F8C8D", "marginBottom": "40px", "fontSize": "16px"},
        ),
        html.Div(
            [
                html.H3("📈 歷年體位結構變遷趨勢", style={"color": "#34495E"}),
                html.P("透過下拉選單與年度滑桿，自由組合您想要觀察的體位類別、性別與年份範圍：", style={"color": "#7F8C8D"}),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("選擇體位類別：", style={"fontWeight": "bold"}),
                                dcc.Dropdown(
                                    id="category-dropdown",
                                    options=category_options,
                                    value="全部類別",
                                    clearable=False,
                                ),
                            ],
                            style={"width": "48%", "display": "inline-block"},
                        ),
                        html.Div(
                            [
                                html.Label("選擇統計族群：", style={"fontWeight": "bold"}),
                                dcc.Dropdown(
                                    id="gender-dropdown",
                                    options=gender_options,
                                    value="男與女共同顯示",
                                    clearable=False,
                                ),
                            ],
                            style={"width": "48%", "display": "inline-block", "float": "right"},
                        ),
                    ],
                    style={"marginBottom": "20px"},
                ),
                html.Div(
                    [
                        html.Label("指定觀察的民國年度範圍：", style={"fontWeight": "bold", "marginBottom": "10px", "display": "block"}),
                        dcc.RangeSlider(
                            id="year-slider",
                            min=min_yr,
                            max=max_yr,
                            step=1,
                            value=[min_yr, max_yr],
                            marks={str(yr): str(yr) for yr in range(min_yr, max_yr + 1, 2)}
                        ),
                    ],
                    style={"marginBottom": "30px", "padding": "0 10px"}
                ),
                dcc.Graph(id="trend-line-chart"),
            ],
            style={"backgroundColor": "#F8F9F9", "padding": "20px", "borderRadius": "8px", "marginBottom": "40px", "boxShadow": "0 2px 4px rgba(0,0,0,0.05)"},
        ),
        html.Div(
            [
                html.H3("🔮 體位指標未來趨勢預測（延伸推估）", style={"color": "#34495E"}),
                html.P("運用線性趨勢模型向外推估未來三年（114-116年）的可能走向（虛線部分為預測值）：", style={"color": "#7F8C8D"}),
                dcc.Graph(id="prediction-line-chart"),
            ],
            style={"backgroundColor": "#F8F9F9", "padding": "20px", "borderRadius": "8px", "marginBottom": "40px", "boxShadow": "0 2px 4px rgba(0,0,0,0.05)"},
        ),
        html.Div(
            [
                html.H3("📋 男女比例差異比較表", style={"color": "#34495E", "marginBottom": "10px"}),
                html.P("可自由選定年度與體位類別，系統將自動比對男生與女生的數值並計算差額：", style={"color": "#7F8C8D"}),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("選擇比較年度：", style={"fontWeight": "bold"}),
                                dcc.Dropdown(
                                    id="table-year-dropdown",
                                    options=year_options,
                                    value=max_yr,
                                    clearable=False,
                                ),
                            ],
                            style={"width": "48%", "display": "inline-block"},
                        ),
                        html.Div(
                            [
                                html.Label("選擇比較體位類別：", style={"fontWeight": "bold"}),
                                dcc.Dropdown(
                                    id="table-category-dropdown",
                                    options=table_category_options,
                                    value="適中",
                                    clearable=False,
                                ),
                            ],
                            style={"width": "48%", "display": "inline-block", "float": "right"},
                        ),
                    ],
                    style={"marginBottom": "20px"}
                ),
                html.Div(id="table-container")
            ],
            style={"backgroundColor": "#F8F9F9", "padding": "20px", "borderRadius": "8px", "marginBottom": "40px", "boxShadow": "0 2px 4px rgba(0,0,0,0.05)"},
        ),
    ],
)

@app.callback(
    Output("trend-line-chart", "figure"),
    [
        Input("category-dropdown", "value"),
        Input("gender-dropdown", "value"),
        Input("year-slider", "value")
    ],
)
def update_line_chart(selected_category, selected_gender, year_range):
    start_year, end_year = year_range
    dff = df[(df["年度"] >= start_year) & (df["年度"] <= end_year)]
    color_map = {"男": "#1F77B4", "女": "#D62728", "男性": "#1F77B4", "女性": "#D62728"}
    
    if selected_gender == "男與女共同顯示":
        filtered_df = dff[dff["性別"].isin(["男", "女", "男性", "女性"])].sort_values("年度")
        if selected_category == "全部類別":
            fig = px.line(
                filtered_df, x="年度", y="百分比", color="類別", line_dash="性別",
                title=f"【男與女共同顯示】- 所有體位類別歷年變化趨勢 ({start_year}-{end_year}年)",
                markers=True, labels={"百分比": "比例 (%)", "年度": "民國年度"},
            )
        else:
            sub_df = filtered_df[filtered_df["類別"] == selected_category]
            fig = px.line(
                sub_df, x="年度", y="百分比", color="性別",
                title=f"【男與女共同顯示】- {selected_category} 歷年變化趨勢 ({start_year}-{end_year}年)",
                markers=True, labels={"百分比": "比例 (%)", "年度": "民國年度"},
                color_discrete_map=color_map,
            )
    else:
        if selected_category == "全部類別":
            filtered_df = dff[dff["性別"] == selected_gender].sort_values("年度")
            fig = px.line(
                filtered_df, x="年度", y="百分比", color="類別",
                title=f"【{selected_gender}】- 所有體位類別歷年變化趨勢 ({start_year}-{end_year}年)",
                markers=True, labels={"百分比": "比例 (%)", "年度": "民國年度"},
            )
        else:
            sub_df = dff[(dff["性別"] == selected_gender) & (dff["類別"] == selected_category)]
            fig = px.line(
                sub_df, x="年度", y="百分比", color="類別",
                title=f"【{selected_gender}】- {selected_category} 歷年變化趨勢 ({start_year}-{end_year}年)",
                markers=True, labels={"百分比": "比例 (%)", "年度": "民國年度"},
            )
    
    fig.update_layout(
        plot_bgcolor="#FFFFFF", paper_bgcolor="#F8F9F9", font={"color": "#2C3E50"},
        xaxis=dict(showgrid=True, gridcolor="#EAECEE"), yaxis=dict(showgrid=True, gridcolor="#EAECEE"),
    )
    return fig

@app.callback(
    Output("prediction-line-chart", "figure"),
    [
        Input("category-dropdown", "value"),
        Input("gender-dropdown", "value")
    ],
)
def update_prediction_chart(selected_category, selected_gender):
    cat = "過重" if selected_category == "全部類別" else selected_category
    gen = "男" if selected_gender == "男與女共同顯示" else selected_gender

    sub = df[(df["類別"] == cat) & (df["性別"] == gen)].sort_values("年度")
    
    if len(sub) > 1:
        x = sub["年度"].values
        y = sub["百分比"].values
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        
        future_years = np.array([114, 115, 116])
        future_preds = p(future_years)
        
        hist_df = pd.DataFrame({"年度": x, "百分比": y, "類型": "歷史實際值"})
        pred_df = pd.DataFrame({"年度": future_years, "百分比": future_preds, "類型": "未來預測值 (線性推估)"})
        combined = pd.concat([hist_df, pred_df])
        
        fig = px.line(
            combined, x="年度", y="百分比", color="類型", markers=True,
            title=f"【{gen} - {cat}】未來三年趨勢預測模型 (114-116年)",
            labels={"百分比": "比例 (%)", "年度": "民國年度"},
            color_discrete_map={"歷史實際值": "#1F77B4", "未來預測值 (線性推估)": "#FF7F0E"}
        )
        fig.update_traces(selector=dict(name="未來預測值 (線性推估)"), line=dict(dash="dash"))
    else:
        fig = px.line(title="資料不足無法預測")

    fig.update_layout(
        plot_bgcolor="#FFFFFF", paper_bgcolor="#F8F9F9", font={"color": "#2C3E50"},
        xaxis=dict(showgrid=True, gridcolor="#EAECEE"), yaxis=dict(showgrid=True, gridcolor="#EAECEE"),
    )
    return fig

@app.callback(
    Output("table-container", "children"),
    [
        Input("table-year-dropdown", "value"),
        Input("table-category-dropdown", "value")
    ]
)
def update_table(table_year, table_category):
    sub = df[(df["年度"] == table_year) & (df["類別"] == table_category)]
    
    male_row = sub[sub["性別"].isin(["男", "男性"])]
    female_row = sub[sub["性別"].isin(["女", "女性"])]
    
    m_val = male_row["百分比"].values[0] if not male_row.empty else None
    f_val = female_row["百分比"].values[0] if not female_row.empty else None
    
    diff = round(m_val - f_val, 2) if (m_val is not None and f_val is not None) else "N/A"
    
    table_data = [
        {"年度": table_year, "體位類別": table_category, "男生比例 (%)": m_val, "女生比例 (%)": f_val, "男女差額 (男-女)": diff}
    ]
    
    return dash_table.DataTable(
        data=table_data,
        columns=[{"name": i, "id": i} for i in ["年度", "體位類別", "男生比例 (%)", "女生比例 (%)", "男女差額 (男-女)"]],
        style_table={"overflowX": "auto"},
        style_header={"backgroundColor": "#34495E", "color": "white", "fontWeight": "bold", "textAlign": "center"},
        style_cell={"textAlign": "center", "padding": "12px", "fontFamily": "Microsoft JhengHei, sans-serif"},
        style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#F2F4F4"}]
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)

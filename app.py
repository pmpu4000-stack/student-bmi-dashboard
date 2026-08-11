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

    # 當滑軌拖動時
    if triggered_id == "year-range-slider":
        real_start = min(slider_val)
        real_end = max(slider_val)
        return real_start, real_end, slider_val, ""
    
    # 檢查輸入格式
    if start_in is None or end_in is None:
        return start_in, end_in, dash.no_update, html.Span("⚠️ 請填入完整的年份數字", style={"color": "#ff5252", "fontSize": "13px", "fontWeight": "bold"})

    # 檢查數據範圍
    if not (MIN_YEAR <= start_in <= MAX_YEAR and MIN_YEAR <= end_in <= MAX_YEAR):
        err = f"⚠️ 輸入超出範圍！請輸入民國 {MIN_YEAR} 年至 {MAX_YEAR} 年之間的數字"
        return start_in, end_in, dash.no_update, html.Span(err, style={"color": "#ff5252", "fontSize": "13px", "fontWeight": "bold"})

    return start_in, end_in, [start_in, end_in], ""

# 2. 折線圖渲染
@app.callback(
    Output("trend-line-chart", "figure"),
    [Input("male-checklist", "value"),
     Input("female-checklist", "value"),
     Input("year-range-slider", "value")]
)
def update_trend_chart(male_selected, female_selected, year_range):
    selected_groups = (male_selected or []) + (female_selected or [])
    
    # 未選擇項目時顯示提示
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
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=DARK_BG,
        plot_bgcolor=CARD_BG,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(tickmode='linear', dtick=1, tickfont=dict(color=TEXT_COLOR)),
        yaxis=dict(tickfont=dict(color=TEXT_COLOR)),
        legend=dict(font=dict(color=TEXT_COLOR)),
        hoverlabel=dict(bgcolor="#333333", font_color="#FFFFFF", font_size=14)
    )
    
    return fig

# ------------------------------------------------------------------------------
# 5. 啟動服務
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

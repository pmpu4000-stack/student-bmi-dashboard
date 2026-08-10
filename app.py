import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
import io

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
113,女,肥胖,11.5
"""

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

unique_genders = df["性別"].dropna().unique()
gender_options = [{"label": g, "value": g} for g in sorted(list(set(unique_genders)))]
gender_options.append({"label": "男與女共同顯示", "value": "男與女共同顯示"})

category_options = [
    {"label": "📊 全部指標總覽 (過輕/適中/過重/肥胖)", "value": "全部類別"}
] + [
    {"label": f"  • {c}", "value": c} 
    for c in df[df["指標類型"] == "BMI 體位"]["類別"].unique()
]

min_yr = int(df["年度"].min())
max_yr = int(df["年度"].max())

app.layout = html.Div(
    style={
        "fontFamily": "Microsoft JhengHei, sans-serif",
        "padding": "30px",
        "backgroundColor": "#FDFEFE"
    },
    children=[
        html.H1(
            "台灣學生歷年體位趨勢大數據互動報告",
            style={
                "textAlign": "center",
                "color": "#2C3E50",
                "marginBottom": "10px"
            },
        ),
        html.P(
            "專題研究：探討民國 96 年至 113 年國民體位統計數據之變遷、性別差異與未來預測",
            style={
                "textAlign": "center",
                "color": "#7F8C8D",
                "marginBottom": "40px",
                "fontSize": "16px"
            },
        ),
        html.Div(
            [
                html.H3("📈 歷年體位結構變遷趨勢（支援自訂篩選）", style={
                    "color": "#34495E"
                }),
                html.P(
                    "透過下拉選單與年度滑桿，自由組合您想要觀察的體位類別、性別與年份範圍：",
                    style={
                        "color": "#7F8C8D"
                    },
                ),
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
            style={
                "backgroundColor": "#F8F9F9",
                "padding": "20px",
                "borderRadius": "8px",
                "marginBottom": "40px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)"
            },
        ),
        html.Div(
            [
                html.H3("🔮 體位指標未來趨勢預測（延伸推估）", style={
                    "color": "#34495E"
                }),
                html.P(
                    "運用線性趨勢模型向外推估未來三年（114-116年）的可能走向（虛線部分為預測值）：",
                    style={
                        "color": "#7F8C8D"
                    },
                ),
                dcc.Graph(id="prediction-line-chart"),
            ],
            style={
                "backgroundColor": "#F8F9F9",
                "padding": "20px",
                "borderRadius": "8px",
                "marginBottom": "40px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)"
            },
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
    
    if selected_gender == "男與女共同顯示":
        filtered_df = dff[dff["性別"].isin(["男", "女", "男性", "女性"])].sort_values("年度")
        if selected_category == "全部類別":
            fig = px.line(
                filtered_df,
                x="年度",
                y="百分比",
                color="類別",
                line_dash="性別",
                title=f"【男與女共同顯示】- 所有體位類別歷年變化趨勢 ({start_year}-{end_year}年)",
                markers=True,
                labels={"百分比": "比例 (%)", "年度": "民國年度"},
            )
        else:
            sub_df = filtered_df[filtered_df["類別"] == selected_category]
            fig = px.line(
                sub_df,
                x="年度",
                y="百分比",
                color="性別",
                title=f"【男與女共同顯示】- {selected_category} 歷年變化趨勢 ({start_year}-{end_year}年)",
                markers=True,
                labels={"百分比": "比例 (%)", "年度": "民國年度"},
            )
    else:
        if selected_category == "全部類別":
            filtered_df = dff[dff["性別"] == selected_gender].sort_values("年度")
            fig = px.line(
                filtered_df,
                x="年度",
                y="百分比",
                color="類別",
                title=f"【{selected_gender}】- 所有體位類別歷年變化趨勢 ({start_year}-{end_year}年)",
                markers=True,
                labels={"百分比": "比例 (%)", "年度": "民國年度"},
            )
        else:
            filtered_df = dff[
                (dff["類別"] == selected_category) & (dff["性別"] == selected_gender)
            ].sort_values("年度")
            fig = px.line(
                filtered_df,
                x="年度",
                y="百分比",
                title=f"【{selected_gender}】- {selected_category} 歷年變化趨勢 ({start_year}-{end_year}年)",
                markers=True,
                labels={"百分比": "比例 (%)", "年度": "民國年度"},
            )
            
    fig.update_traces(connectgaps=True)
    fig.update_layout(
        hovermode="x unified",
        title_font_size=18,
        height=600,
        xaxis=dict(tickmode="linear", dtick=1, range=[start_year - 0.5, end_year + 0.5]),
        yaxis=dict(autorange=True),
    )
    return fig

@app.callback(
    Output("prediction-line-chart", "figure"),
    [Input("category-dropdown", "value"), Input("gender-dropdown", "value")]
)
def update_prediction_chart(selected_category, selected_gender):
    categories_to_predict = df["類別"].unique() if selected_category == "全部類別" else [selected_category]
    
    if selected_gender == "男與女共同顯示":
        genders_to_predict = ["男", "女"]
    else:
        genders_to_predict = [selected_gender]
        
    all_pred_dfs = []
    for cat in categories_to_predict:
        for gen in genders_to_predict:
            sub_df = df[(df["類別"] == cat) & (df["性別"] == gen)].sort_values("年度")
            X = sub_df["年度"].values
            y = sub_df["百分比"].values
            
            if len(X) > 1:
                slope, intercept = np.polyfit(X, y, 1)
                future_years = np.array([X[-1] + 1, X[-1] + 2, X[-1] + 3])
                future_y = slope * future_years + intercept
                
                all_years = np.concatenate([X, future_years])
                all_y = np.concatenate([y, future_y])
                
                if selected_gender == "男與女共同顯示":
                    type_labels = [f"{gen} (歷史)"] * len(X) + [f"{gen} (預測)"] * len(future_years)
                else:
                    type_labels = ["歷史數據"] * len(X) + ["AI 線性趨勢預測"] * len(future_years)
                    
                temp_pred_df = pd.DataFrame({
                    "年度": all_years,
                    "百分比": all_y,
                    "系列": f"{cat} - {gen}" if len(categories_to_predict) > 1 or selected_gender == "男與女共同顯示" else cat,
                    "資料類型": type_labels
                })
                all_pred_dfs.append(temp_pred_df)
                
    if all_pred_dfs:
        pred_df = pd.concat(all_pred_dfs, ignore_index=True)
    else:
        pred_df = pd.DataFrame(columns=["年度", "百分比", "系列", "資料類型"])
        
    if selected_category == "全部類別" or selected_gender == "男與女共同顯示":
        fig = px.line(
            pred_df,
            x="年度",
            y="百分比",
            color="系列",
            line_dash="資料類型",
            title=f"【{selected_gender}】 - {selected_category} 歷史與未來趨勢預測",
            markers=True,
            labels={"百分比": "比例 (%)", "年度": "民國年度"},
        )
    else:
        fig = px.line(
            pred_df,
            x="年度",
            y="百分比",
            color="資料類型",
            title=f"【{selected_gender}】- {selected_category} 歷史與未來趨勢預測",
            markers=True,
            labels={"百分比": "比例 (%)", "年度": "民國年度"},
            color_discrete_map={"歷史數據": "#2980B9", "AI 線性趨勢預測": "#E67E22"}
        )
        
    fig.update_traces(connectgaps=True)
    min_year = int(df["年度"].min())
    max_year = int(df["年度"].max()) + 3
    fig.update_layout(
        hovermode="x unified",
        title_font_size=18,
        height=600,
        xaxis=dict(tickmode="linear", dtick=1, range=[min_year - 0.5, max_year + 0.5]),
        yaxis=dict(autorange=True),
    )
    return fig

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)

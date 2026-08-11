import dash
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

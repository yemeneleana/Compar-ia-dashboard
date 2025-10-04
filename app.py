import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

# Page configuration
st.set_page_config(
    page_title="Compar'AI Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    h1, h2, h3 {
        color: #10b981 !important;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.title("🤖 Compar'AI Dashboard")
st.markdown("### Benchmarking LLMs: Quality, Energy & Performance")
st.markdown("---")

# Sample data
default_data = pd.DataFrame([
    {"Models": "Meta LLaMA 3.1 8B", "Size": "Small", "Question": 1, "Quality": 5, "Latency": 4, "CO2": 0.15, "Energy": 0.24, "Questions class": "Easy factual & rewriting"},
    {"Models": "Meta LLaMA 3.1 8B", "Size": "Small", "Question": 2, "Quality": 3, "Latency": 0, "CO2": 0.13, "Energy": 0.21, "Questions class": "Easy factual & rewriting"},
    {"Models": "Meta LLaMA 3.1 8B", "Size": "Small", "Question": 3, "Quality": 3, "Latency": 3, "CO2": 0.76, "Energy": 1.24, "Questions class": "Easy factual & rewriting"},
])

# Sidebar - File upload
st.sidebar.header("📁 Import Data")
uploaded_file = st.sidebar.file_uploader("Upload your Excel/CSV file", type=['csv', 'xlsx', 'xls'])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()
        st.sidebar.success(f"✅ {len(df)} rows loaded")
        st.sidebar.info(f"Detected columns: {', '.join(df.columns)}")
    except Exception as e:
        st.sidebar.error(f"❌ Error: {e}")
        df = default_data
else:
    df = default_data
    st.sidebar.info("📊 Sample data loaded")

# Check required columns
required_columns = ['Models', 'Size', 'Question', 'Quality', 'Latency', 'CO2', 'Energy', 'Questions class']
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"⚠️ Missing columns: {', '.join(missing_columns)}")
    st.info(f"Detected columns: {', '.join(df.columns)}")
    st.stop()

# Aggregated calculations
agg_df = df.groupby(['Models', 'Size']).agg({
    'Quality': 'mean',
    'Latency': 'mean',
    'CO2': ['sum', 'mean'],
    'Energy': ['sum', 'mean']
}).reset_index()

agg_df.columns = ['Models', 'Size', 'avg_quality', 'avg_latency', 'total_co2', 'avg_co2', 'total_energy', 'avg_energy']
agg_df['efficiency'] = agg_df['avg_quality'] / (agg_df['avg_energy'] + 0.01)

# Sidebar - Filters
st.sidebar.header("🔍 Filters")
models = st.sidebar.multiselect("Models", df['Models'].unique(), default=df['Models'].unique())
categories = st.sidebar.multiselect("Categories", df['Questions class'].unique(), default=df['Questions class'].unique())

# Filter data
df_filtered = df[(df['Models'].isin(models)) & (df['Questions class'].isin(categories))]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⚖️ Quality vs Energy", "⚡ Latency", "🏆 Ranking"])

# ============ TAB 1: OVERVIEW ============
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌿 Total CO₂", f"{df_filtered['CO2'].sum():.2f} kg", delta=f"{df_filtered['CO2'].mean():.3f} avg")
    with col2:
        st.metric("⚡ Total Energy", f"{df_filtered['Energy'].sum():.2f} kWh", delta=f"{df_filtered['Energy'].mean():.3f} avg")
    with col3:
        st.metric("🎯 Avg Quality", f"{df_filtered['Quality'].mean():.2f}/5", delta=f"{df_filtered['Quality'].std():.2f} σ")
    with col4:
        st.metric("🧪 Tests Run", len(df_filtered))
    
    st.markdown("---")
    
    st.subheader("Dataset Overview")
    st.dataframe(df, use_container_width=True)
    
    st.subheader("⚡ Energy & CO₂ per Question")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_filtered['Question'], y=df_filtered['Energy'], mode='lines+markers', name='Energy (kWh)', line=dict(color='#f59e0b', width=3)))
    fig2.add_trace(go.Scatter(x=df_filtered['Question'], y=df_filtered['CO2'], mode='lines+markers', name='CO₂ (kg)', line=dict(color='#ef4444', width=3)))
    fig2.update_layout(template='plotly_dark', height=400)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader("🔥 Performance Heatmap by Category")
    pivot_data = df_filtered.pivot_table(values='Quality', index='Questions class', columns='Question', aggfunc='mean')
    fig3 = px.imshow(pivot_data, color_continuous_scale='RdYlGn', aspect='auto', labels=dict(x="Question", y="Category", color="Quality"))
    fig3.update_layout(template='plotly_dark', height=300)
    st.plotly_chart(fig3, use_container_width=True)

# ============ TAB 2: QUALITY VS ENERGY ============
with tab2:
    st.subheader("Quality vs Energy")
    chart1 = alt.Chart(df_filtered).mark_circle(size=100).encode(
        x="Energy", y="Quality", color="Models", tooltip=list(df_filtered.columns)
    ).interactive()
    st.altair_chart(chart1, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Efficiency Score (Quality/Energy)")
        fig5 = px.bar(agg_df.sort_values('efficiency', ascending=False), x='Models', y='efficiency', color='efficiency', color_continuous_scale='Viridis', text='efficiency')
        fig5.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig5.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig5, use_container_width=True)
    with col2:
        st.subheader("🌍 Environmental Impact")
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(x=agg_df['Models'], y=agg_df['total_energy'], name='Total Energy (kWh)', marker_color='#f59e0b'))
        fig6.add_trace(go.Bar(x=agg_df['Models'], y=agg_df['total_co2'], name='Total CO₂ (kg)', marker_color='#ef4444'))
        fig6.update_layout(template='plotly_dark', height=400, barmode='group')
        st.plotly_chart(fig6, use_container_width=True)

# ============ TAB 3: LATENCY ============
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚡ Average Latency by Model")
        fig7 = px.bar(agg_df.sort_values('avg_latency'), x='Models', y='avg_latency', color='avg_latency', color_continuous_scale='Blues', text='avg_latency')
        fig7.update_traces(texttemplate='%{text:.2f}s', textposition='outside')
        fig7.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig7, use_container_width=True)
    with col2:
        st.subheader("📊 Latency Distribution")
        fig8 = px.box(df_filtered, x='Models', y='Latency', color='Size', color_discrete_map={'Small': '#10b981', 'Medium': '#f59e0b', 'Large': '#ef4444'})
        fig8.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig8, use_container_width=True)
    
    st.subheader("📈 Latency Evolution Over Questions")
    fig9 = px.line(df_filtered, x='Question', y='Latency', color='Models', markers=True)
    fig9.update_layout(template='plotly_dark', height=400)
    st.plotly_chart(fig9, use_container_width=True)

# ============ TAB 4: RANKING ============
with tab4:
    

    st.subheader("ℹ️ How the Efficiency Score is Calculated")
    st.markdown("""
    The **Efficiency Score** is a composite metric used to evaluate the overall performance of each model, considering **Quality, Latency, CO₂ emissions, and Energy consumption**.  

    It is calculated as:

    - 🌟 **Quality (40%)** → Higher quality increases the score.  
    - ⚡ **Latency (20%)** → Faster response times increase the score.  
    - 🌿 **CO₂ emissions (20%)** → Lower CO₂ emissions increase the score.  
    - 🔋 **Energy consumption (20%)** → Lower energy usage increases the score.  

    **Formula:**  
    Score = 0.4 * Quality_norm + 0.2 * Latency_norm + 0.2 * CO2_norm + 0.2 * Energy_norm

    Each metric is normalized between 0 and 1.  
    A higher score indicates a **better trade-off** between **accuracy, speed, and environmental impact**.
    """)
    
    st.subheader("🏆 Best Trade-off Ranking")
    # Ranking table
    ranking_df = agg_df.sort_values('efficiency', ascending=False).reset_index(drop=True)
    ranking_df.index += 1
    def add_medal(rank): 
        medals = {1: "🥇", 2: "🥈", 3: "🥉"} 
        return medals.get(rank, f"{rank}")
    ranking_df['Rank'] = ranking_df.index.map(add_medal)
    display_df = ranking_df[['Rank', 'Models', 'Size', 'avg_quality', 'avg_latency', 'total_energy', 'total_co2', 'efficiency']].copy()
    display_df.columns = ['🏅 Rank', 'Model', 'Size', 'Avg Quality', 'Avg Latency (s)', 'Total Energy (kWh)', 'Total CO₂ (kg)', 'Efficiency']
    st.dataframe(display_df.style.format({'Avg Quality':'{:.2f}','Avg Latency (s)':'{:.2f}','Total Energy (kWh)':'{:.2f}','Total CO₂ (kg)':'{:.2f}','Efficiency':'{:.2f}'}), use_container_width=True, height=400)

    # Best models per Size and Questions class using same efficiency score
    df_grouped = df.groupby(["Models", "Size", "Questions class"]).mean().reset_index()
    df_grouped = df_grouped.merge(agg_df[['Models','Size','efficiency']], on=['Models','Size'], how='left')
    best_models = df_grouped.loc[df_grouped.groupby(["Size","Questions class"])['efficiency'].idxmax()]
    best_models_display = best_models[['Models','Size','Questions class','Quality','Latency','CO2','Energy','efficiency']]
    st.subheader("🏆 Best model trade-off by Size and Questions classifications")
    st.markdown("The **Efficiency** score is used as the ranking metric.")
    st.dataframe(best_models_display.rename(columns={"Models":"Model","efficiency":"Score"}).style.format({
        "Quality":"{:.2f}",
        "Latency":"{:.2f}",
        "CO2":"{:.2f}",
        "Energy":"{:.2f}",
        "Score":"{:.3f}"
    }), use_container_width=True)


    # Best model per Questions class only (ignoring Size)
    best_models_by_class = df_grouped.loc[df_grouped.groupby(["Questions class"])['efficiency'].idxmax()]
    best_models_by_class_display = best_models_by_class[['Models', 'Questions class', 'Quality','Latency','CO2','Energy','efficiency']]

    st.subheader("🏆 Best model per Questions class")
    st.markdown("The **Efficiency** score is used to rank the models.")
    st.dataframe(best_models_by_class_display.rename(columns={"Models":"Model","efficiency":"Score"}).style.format({
        "Quality":"{:.2f}",
        "Latency":"{:.2f}",
        "CO2":"{:.2f}",
        "Energy":"{:.2f}",
        "Score":"{:.3f}"
    }), use_container_width=True)


    # Normalized scores
    st.subheader("📊 Normalized Scores (0-100)")
    scores_df = agg_df.copy()
    scores_df['Quality_Score'] = (scores_df['avg_quality'] / 5) * 100
    scores_df['Speed_Score'] = (1 - scores_df['avg_latency'] / (scores_df['avg_latency'].max() + 0.01)) * 100
    scores_df['Energy_Score'] = (1 - scores_df['total_energy'] / (scores_df['total_energy'].max() + 0.01)) * 100
    scores_df['CO2_Score'] = (1 - scores_df['total_co2'] / (scores_df['total_co2'].max() + 0.01)) * 100
    scores_df['Overall_Score'] = (scores_df['Quality_Score'] + scores_df['Speed_Score'] + 
                                   scores_df['Energy_Score'] + scores_df['CO2_Score']) / 4
    
    fig11 = go.Figure()
    categories = ['Quality', 'Speed', 'Energy', 'CO₂', 'Overall']
    for idx, row in scores_df.iterrows():
        fig11.add_trace(go.Bar(
            name=row['Models'],
            x=categories,
            y=[row['Quality_Score'], row['Speed_Score'], 
               row['Energy_Score'], row['CO2_Score'], row['Overall_Score']]
        ))
    
    fig11.update_layout(
        barmode='group',
        template='plotly_dark',
        height=400,
        yaxis_title='Score (0-100)'
    )
    st.plotly_chart(fig11, use_container_width=True)




# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 20px;'>
    <p>🌿 <b>Compar'AI Benchmarking Platform</b> | Green AI Initiative</p>
    <p>Comparing LLMs on Quality, Latency, Energy & CO₂ emissions</p>
</div>
""", unsafe_allow_html=True)

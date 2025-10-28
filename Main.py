import streamlit as st
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px


if 'analyzed_df' not in st.session_state:
    st.session_state['analyzed_df'] = None


st.title("🧠 Sentiment Analysis Web Platform")

# Sidebar Menu
choice = st.sidebar.selectbox("📋 Menu", ("Home", "Analysis", "Visualization"))


if choice == "Home":
    st.image("https://miro.medium.com/v2/resize:fit:1400/0*tkL20Gt31dYYigyV")
    st.markdown(
        """
        <div style='text-align: center; background-color: #E6F3FF; padding: 10px; border-radius: 10px;'>
            <h1 style='color: #007BFF;'>Welcome Home! 🎉</h1>
            <p style='font-size: 20px; color: #333;'>Check Your Feedback and Dive into the Analysis.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------
# Analysis Section
# ---------------------------
elif choice == "Analysis":
    st.header("📊 Perform Sentiment Analysis")
    st.info("Insert your Google Sheet link, e.g. `https://docs.google.com/spreadsheets/d/.../edit?usp=sharing` "
            "and modify it to `.../export?format=csv&usp=sharing`")

    url = st.text_input("Enter your Google Sheet (CSV) URL")
    cn = st.text_input("Enter the column name to analyze")
    btn = st.button("🔍 Analyze")

    

    if btn:
        try:
            df = pd.read_csv(url)
            if cn not in df.columns:
                st.error(f"❌ Column '{cn}' not found in the dataset.")
            else:
                x = df[cn]
                analyzer = SentimentIntensityAnalyzer()
                sentiments = []

                for text in x:
                    pred = analyzer.polarity_scores(str(text))
                    if pred['compound'] > 0.01:
                        sentiments.append("Positive")
                    elif pred['compound'] < -0.01:
                        sentiments.append("Negative")
                    else:
                        sentiments.append("Neutral")

                df["Sentiment"] = sentiments
                st.session_state['analyzed_df'] = df
                st.success("✅ Analysis completed successfully! Go to the 'Visualization' tab to see your results.")
                st.dataframe(df.head())
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download Analyzed Results as CSV",
                    data=csv,
                    file_name="sentiment_analysis_results.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# ---------------------------
# Visualization Section
# ---------------------------
elif choice == "Visualization":
    st.header("📈 Sentiment Visualization")
    st.image("https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/002/202/619/datas/original.gif")

    if st.session_state['analyzed_df'] is None:
        st.error("⚠️ No analysis results found! Please go to the 'Analysis' section and run the analysis first.")
    else:
        df = st.session_state['analyzed_df']

        choice2 = st.selectbox("Choose a visualization type:", ("None", "Table", "Pie", "Histogram"))

        if choice2 == "Table":
            st.subheader("📋 Full Analyzed Data Table")
            st.dataframe(df)

        elif choice2 == "Pie":
            st.subheader("🥧 Sentiment Distribution")
            pos_per = (len(df[df['Sentiment'] == "Positive"]) / len(df)) * 100
            neg_per = (len(df[df['Sentiment'] == "Negative"]) / len(df)) * 100
            neu_per = (len(df[df['Sentiment'] == "Neutral"]) / len(df)) * 100

            fig = px.pie(
                values=[pos_per, neg_per, neu_per],
                names=['Positive', 'Negative', 'Neutral'],
                title="Sentiment Breakdown (%)"
            )
            st.plotly_chart(fig)

        elif choice2 == "Histogram":
            st.subheader("📊 Histogram View")
            c = st.selectbox("Choose a column for histogram:", df.columns)
            fig = px.histogram(df, x=c, color="Sentiment", title=f"Distribution of {c} by Sentiment")
            st.plotly_chart(fig)

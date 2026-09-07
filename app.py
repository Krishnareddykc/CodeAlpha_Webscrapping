import streamlit as st
import pandas as pd
import os
import subprocess
import sys

# Page configuration
st.set_page_config(
    page_title="CodeAlpha Web Scraping",
    page_icon="📚",
    layout="wide"
)

# Title
st.title("📚 CodeAlpha Web Scraping Dashboard")
st.write("Web Scraping Project with Streamlit")

st.divider()

# CSV location
csv_path = os.path.join("data", "books.csv")

# Run scraper
st.subheader("🚀 Web Scraper")

if st.button("Run Web Scraper", use_container_width=True):

    try:
        result = subprocess.run(
            [sys.executable, "scraper.py"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            st.success("✅ Scraping completed successfully!")

            if result.stdout:
                st.text(result.stdout)

        else:
            st.error("❌ Scraping failed!")
            st.code(result.stderr)

    except Exception as e:
        st.error(f"Error: {e}")

st.divider()

# Display scraped data
st.subheader("📊 Scraped Book Data")

if os.path.exists(csv_path):

    try:
        df = pd.read_csv(csv_path)

        # Metrics
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Books",
            len(df)
        )

        # Find price column
        price_column = None

        for column in df.columns:
            if "price" in column.lower():
                price_column = column
                break

        if price_column:
            prices = pd.to_numeric(
                df[price_column],
                errors="coerce"
            )

            col2.metric(
                "Average Price",
                f"£{prices.mean():.2f}"
            )
        else:
            col2.metric("Average Price", "N/A")

        col3.metric(
            "Columns",
            len(df.columns)
        )

        st.divider()

        # Search
        st.subheader("🔎 Search Books")

        search = st.text_input(
            "Enter book title"
        )

        filtered_df = df.copy()

        # Find title column
        title_column = None

        for column in df.columns:
            if "title" in column.lower():
                title_column = column
                break

        if search and title_column:

            filtered_df = df[
                df[title_column]
                .astype(str)
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        # Display dataframe
        st.dataframe(
            filtered_df,
            use_container_width=True
        )

        st.write(
            f"Showing **{len(filtered_df)}** books"
        )

        st.divider()

        # Download CSV
        st.subheader("⬇️ Download Data")

        csv_data = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download books.csv",
            data=csv_data,
            file_name="books.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.divider()

        # Chart
        if price_column:

            st.subheader("📈 Price Chart")

            chart_data = filtered_df.copy()

            chart_data[price_column] = pd.to_numeric(
                chart_data[price_column],
                errors="coerce"
            )

            chart_data = chart_data.dropna(
                subset=[price_column]
            )

            if title_column:

                chart_data = chart_data.set_index(
                    title_column
                )

                st.bar_chart(
                    chart_data[price_column].head(20)
                )

    except Exception as e:

        st.error(
            f"Could not read books.csv: {e}"
        )

else:

    st.warning(
        "⚠️ books.csv not found."
    )

    st.info(
        "Click 'Run Web Scraper' after checking your scraper.py file."
    )

import streamlit as st
import pandas as pd

from src.database import create_database, execute_query
from src.sql_validator import validate_sql
from src.ai_engine import generate_sql


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Chat With Your Data",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🤖 AI Chat With Your Data")

st.write(
    "Upload your CSV file and start exploring your data using AI and SQL."
)


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📂 Upload your CSV file",
    type=["csv"]
)


# --------------------------------------------------
# APPLICATION
# --------------------------------------------------

if uploaded_file is not None:

    # --------------------------------------------------
    # READ CSV
    # --------------------------------------------------

    df = pd.read_csv(uploaded_file)

    # --------------------------------------------------
    # CREATE DUCKDB DATABASE
    # --------------------------------------------------

    connection = create_database(df)

    st.success("✅ File uploaded successfully!")

    # --------------------------------------------------
    # DATASET METRICS
    # --------------------------------------------------

    total_rows = df.shape[0]
    total_columns = df.shape[1]
    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Rows",
            f"{total_rows:,}"
        )

    with col2:
        st.metric(
            "Columns",
            total_columns
        )

    with col3:
        st.metric(
            "Missing Values",
            missing_values
        )

    with col4:
        st.metric(
            "Duplicate Rows",
            duplicate_rows
        )

    st.divider()

    # --------------------------------------------------
    # DATASET PREVIEW
    # --------------------------------------------------

    st.subheader("📊 Dataset Preview")

    st.dataframe(
    df,
    width="stretch",
    height=400
    )

    st.divider()

    # --------------------------------------------------
    # AI CHAT WITH DATA
    # --------------------------------------------------

    st.subheader("🤖 Ask AI About Your Data")

    st.write(
        "Ask a question in normal English. "
        "AI will generate DuckDB SQL and execute it safely."
    )

    # --------------------------------------------------
    # CREATE DATABASE SCHEMA FOR AI
    # --------------------------------------------------

    schema = "\n".join(
        [
            f"{column}: {dtype}"
            for column, dtype in df.dtypes.items()
        ]
    )

    # --------------------------------------------------
    # QUESTION INPUT
    # --------------------------------------------------

    question = st.text_input(
        "💬 Ask a question",
        placeholder="Example: What are the total sales by region?"
    )

    ask_ai = st.button(
        "✨ Ask AI",
        type="primary"
    )

    # --------------------------------------------------
    # AI QUERY
    # --------------------------------------------------

    if ask_ai:

        if not question.strip():

            st.warning(
                "⚠️ Please enter a question."
            )

        else:

            try:

                # --------------------------------------------------
                # GENERATE SQL
                # --------------------------------------------------

                with st.spinner(
                    "🤖 AI is generating SQL..."
                ):

                    generated_sql = generate_sql(
                        question,
                        schema
                    )

                # Remove accidental markdown fences
                generated_sql = (
                    generated_sql
                    .replace("```sql", "")
                    .replace("```", "")
                    .strip()
                )

                st.success(
                    "✅ SQL generated successfully!"
                )

                # --------------------------------------------------
                # SHOW GENERATED SQL
                # --------------------------------------------------

                st.markdown("### 🧠 Generated SQL")

                st.code(
                    generated_sql,
                    language="sql"
                )

                # --------------------------------------------------
                # VALIDATE SQL
                # --------------------------------------------------

                is_valid, message = validate_sql(
                    generated_sql
                )

                if not is_valid:

                    st.error(
                        f"❌ SQL validation failed: {message}"
                    )

                else:

                    # --------------------------------------------------
                    # EXECUTE SQL
                    # --------------------------------------------------

                    with st.spinner(
                        "📊 Running query..."
                    ):

                        result = execute_query(
                            connection,
                            generated_sql
                        )

                    st.success(
                        "✅ Query executed successfully!"
                    )

                    # --------------------------------------------------
                    # DISPLAY RESULTS
                    # --------------------------------------------------

                    st.markdown("### 📈 Results")

                    st.dataframe(
                        result,
                        width="stretch"
                    )

                    # --------------------------------------------------
                    # AUTOMATIC VISUALIZATION
                    # --------------------------------------------------

                    st.markdown(
                        "### 📊 Automatic Visualization"
                    )

                    # Check that result has enough columns
                    if len(result.columns) >= 2:

                        # Find numeric columns
                        numeric_columns = result.select_dtypes(
                            include="number"
                        ).columns.tolist()

                        if numeric_columns:

                            # Find non-numeric/category columns
                            category_columns = [
                                column
                                for column in result.columns
                                if column not in numeric_columns
                            ]

                            if category_columns:

                                category_column = category_columns[0]

                                value_column = numeric_columns[0]

                                # Prepare chart data
                                chart_data = result[
                                    [
                                        category_column,
                                        value_column
                                    ]
                                ].copy()

                                # Convert category to index
                                chart_data = chart_data.set_index(
                                    category_column
                                )

                                # Display chart
                                st.bar_chart(
                                    chart_data
                                )

                            else:

                                st.info(
                                    "ℹ️ No category column available for a chart."
                                )

                        else:

                            st.info(
                                "ℹ️ No numeric column available for visualization."
                            )

                    else:

                        st.info(
                            "ℹ️ The result does not contain enough columns for visualization."
                        )

            except Exception as error:

                st.error(
                    f"❌ AI query error: {error}"
                )

    st.divider()

    # --------------------------------------------------
    # SQL ANALYTICS
    # --------------------------------------------------

    st.subheader("🧮 SQL Analytics")

    st.write(
        "Test read-only SQL queries directly against your dataset."
    )

    sql_query = st.text_area(
        "Enter SQL query",
        value="""SELECT
    Region,
    SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Region
ORDER BY Total_Sales DESC""",
        height=180
    )

    run_query = st.button(
        "▶️ Run SQL Query"
    )

    # --------------------------------------------------
    # RUN MANUAL SQL
    # --------------------------------------------------

    if run_query:

        # --------------------------------------------------
        # VALIDATE SQL
        # --------------------------------------------------

        is_valid, message = validate_sql(
            sql_query
        )

        if not is_valid:

            st.error(
                f"❌ {message}"
            )

        else:

            try:

                # --------------------------------------------------
                # EXECUTE SQL
                # --------------------------------------------------

                result = execute_query(
                    connection,
                    sql_query
                )

                st.success(
                    "✅ Query executed successfully!"
                )

                st.dataframe(
                    result,
                    use_container_width=True
                )

            except Exception as error:

                st.error(
                    f"❌ SQL execution error: {error}"
                )


# --------------------------------------------------
# NO FILE UPLOADED
# --------------------------------------------------

else:

    st.info(
        "👆 Upload a CSV file to begin."
    )
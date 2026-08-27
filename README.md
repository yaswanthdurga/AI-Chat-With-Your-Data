# 🤖 AI Chat With Your Data

An AI-powered data analytics application that allows users to upload a CSV dataset, ask questions in natural language, automatically generate DuckDB SQL queries using Google Gemini, validate the generated SQL, and execute the query safely.

## 🚀 Project Overview

**AI Chat With Your Data** bridges Natural Language Processing and Data Analytics.

Instead of manually writing SQL queries, users can simply ask questions such as:

> "What are the total sales by region?"

The application:

1. Reads the uploaded CSV dataset.
2. Creates an in-memory DuckDB database.
3. Understands the dataset schema.
4. Sends the user's question and schema to Gemini.
5. Generates a DuckDB-compatible SQL query.
6. Validates the generated SQL.
7. Executes only safe read-only queries.
8. Displays the generated SQL and results.

---

## ✨ Features

### 📂 CSV Data Upload
- Upload CSV files directly through the Streamlit interface.
- Automatically reads the dataset using Pandas.

### 📊 Dataset Profiling
Displays:
- Total rows
- Total columns
- Missing values
- Duplicate rows
- Dataset preview

### 🤖 AI-Powered SQL Generation
Users can ask questions in normal English.

Example:

```text
What are the total sales by region?
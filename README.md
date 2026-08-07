# DataClean AI 🧹

An AI-powered data cleaning application that enables users to clean CSV datasets using natural language commands. The application leverages the Groq API with Llama 3.3 to interpret user instructions and automatically perform data preprocessing operations.

## Features

- Upload CSV datasets
- Clean data using natural language commands
- Remove duplicate records
- Handle missing values (mean, median, mode, zero)
- Sort datasets by any column
- Rename columns
- Preview cleaned data
- Download cleaned CSV files
- View cleaning logs and applied actions

## Tech Stack

- Python
- Flask
- Pandas
- Groq API (Llama 3.3)
- HTML
- CSS
- JavaScript

## System Workflow

1. Upload a CSV dataset.
2. Enter a natural language instruction.
3. The Groq LLM converts the instruction into structured JSON actions.
4. The Flask backend validates the generated actions.
5. Pandas executes the requested cleaning operations.
6. The cleaned dataset is displayed and can be downloaded.

## Supported Cleaning Operations

- Remove duplicate rows
- Drop rows with missing values
- Fill missing values using:
  - Mean
  - Median
  - Mode
  - Zero
- Sort records (Ascending/Descending)
- Rename columns

## Example Commands

```
Remove duplicate rows

Fill missing values in Age with median

Sort the dataset by Salary in descending order

Rename column Name to Employee_Name
```

## Project Structure

```
dataclean-ai/
│
├── app.py
├── requirements.txt
├── sample_data.csv
├── README.md
└── templates/
```

## Installation

```bash
git clone https://github.com/Adithyankrishna/dataclean-ai
cd dataclean-ai
pip install -r requirements.txt
```

Set your Groq API Key:

```bash
export GROQ_API_KEY=your_api_key
```

Run the application:

```bash
python app.py
```

## Future Enhancements

- Outlier detection
- Automatic data type correction
- Excel (.xlsx) support
- Data visualization
- User authentication
- AI-powered data quality reports

## Author

**Adithyan Krishna**

GitHub: https://github.com/Adithyankrishna

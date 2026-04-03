# DataClean AI 🧹
### AI-Powered CSV Data Cleaning via Natural Language

---

## What This Project Does
Upload any CSV file and clean it by typing plain English commands.
The app sends your prompt to Claude AI, which converts it to safe JSON actions,
which are then applied to your dataset using Pandas.

**Pipeline:**
```
User Prompt → Claude API → JSON Actions → Pandas → Cleaned Data
```

---

## Folder Structure
```
data-cleaner/
│
├── app.py                 ← Flask backend (main file)
├── requirements.txt       ← Python dependencies
├── sample_data.csv        ← Test CSV to try the app
├── README.md              ← This file
│
└── templates/
    └── index.html         ← Frontend UI
```

---

## Setup Instructions

### Step 1: Get your Claude API Key
- Go to https://console.anthropic.com
- Sign up / Log in
- Create an API key

### Step 2: Set the API key as environment variable

**Windows (Command Prompt):**
```
set ANTHROPIC_API_KEY=your_key_here
```

**Mac/Linux:**
```
export ANTHROPIC_API_KEY=your_key_here
```

### Step 3: Install dependencies
```
pip install -r requirements.txt
```

### Step 4: Run the app
```
python app.py
```

### Step 5: Open in browser
```
http://127.0.0.1:5000
```

---

## How to Use

1. Upload `sample_data.csv` (or any CSV)
2. See the dataset stats — rows, columns, missing values, duplicates
3. Type a natural language command, e.g.:
   - `"remove duplicates"`
   - `"fill missing age with median"`
   - `"sort by salary descending"`
   - `"rename column name to full_name"`
   - `"drop rows with missing values"`
4. Click Run → the AI applies the changes instantly
5. Download the cleaned CSV when done

---

## Supported Operations

| Command Example | Action |
|---|---|
| "remove duplicates" | Drops duplicate rows |
| "drop rows with missing values" | Removes rows with nulls |
| "fill missing salary with median" | Fills nulls with median |
| "fill missing city with mode" | Fills nulls with most common value |
| "fill missing age with zero" | Fills nulls with 0 |
| "sort by age ascending" | Sorts the dataset |
| "rename column name to full_name" | Renames a column |

---

## Interview Q&A (Study This!)

**Q: Why not let the LLM generate Python code directly?**
A: Security risk. Executing arbitrary LLM-generated code is dangerous. 
   JSON actions limit the system to only predefined, safe operations.

**Q: How do you maintain dataset state across multiple prompts?**
A: The DataFrame is stored in a Python dictionary (in-memory) keyed by 
   the user's IP address. Each new prompt loads and updates this state.

**Q: What if the LLM returns invalid JSON?**
A: The response is wrapped in try/except. If JSON parsing fails, 
   an error message is returned to the user.

**Q: Why Flask over Django?**
A: Flask is lightweight and minimal — better for small focused APIs 
   like this with just 4-5 routes.

**Q: What are the limitations of this system?**
A: Only 5 supported operations currently. No user authentication. 
   State resets if the server restarts. Cannot handle very large CSVs.

**Q: How would you scale this?**
A: Use Redis to store session state instead of in-memory dict. 
   Add user authentication. Use async processing for large files.

---

## Tech Stack
- **Backend:** Python + Flask
- **Data Processing:** Pandas
- **AI:** Claude API (Anthropic)
- **Frontend:** HTML + CSS + Vanilla JavaScript

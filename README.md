# 🖥️ OS Process Monitoring Tool

This Python project monitors currently running operating system processes, collects CPU and memory usage data at regular intervals, writes the results to a CSV file, and saves a average version to a PostgreSQL database.

---

## 🚀 Features

- Monitor all running processes using `psutil`
- Filter out excluded processes via `config.json`
- Save data into a CSV file
- Log every iteration to a log file
- Calculate average CPU and memory usage per process
- Insert average CPU and memory usage into PostgreSQL
- Full test coverage with `unittest` and `MagicMock`



---

## 🧪 Running Tests

Run the unit tests using:

```bash
python -m unittest
```

Example test files:
- `test_process_monitor.py`
- Uses `MagicMock` to simulate `psutil.Process` objects
- Verifies CSV generation, process filtering, and data structure integrity

---

## 🗂️ Project Structure

```
.
├── Process.py               # Defines the Process class
├── ProcessMonitor.py        # Handles monitoring and CSV writing
├── db.py                    # Handles PostgreSQL insertion logic
├── initLog.py               # Initializes logging system
├── config.json              # Configuration for runtime behavior
├── main.py                  # Entry point: reads config and runs monitoring
├── test_process_monitor.py  # Unit tests using unittest & mock
├── requirements.txt         # Required packages
├── README.md                # You're reading it :)
```

---

## 📦 Installation

1. Clone the repo:

```bash
git clone https://github.com/OmerLeibovich/process_test.git
cd process_test
```

2. (Recommended) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🤖 AI Usage Policy

This project uses AI assistance (ChatGPT by OpenAI) during development.

### ✅ AI was used for:

- Improving structure of `ProcessMonitor` and `db` modules
- Writing `README.md` and documentation
- Adding `type hints` and `docstrings`
- `config.json` structure and runtime behavior logic
- Refactoring and improving CSV handling,logging and unitest

### ✍️ Manually written and customized:
- Improving structure of `Process` module
- All core logic in `run_monitoring()`, CSV and DB integration
- SQL table structure and data insertion
- Designing unit tests using `unittest` and `MagicMock`


### 💬 Prompt examples used:

- "איך לסנן תהליך לפי שם עם psutil?"
- mock_proc1.cpu_percent = MagicMock(side_effect=[None, 0.0])איך אני מוצא את האיבר השני לצורך השוואה?
- mock_proc2.name = MagicMock(return_value='test_proc_name')מה זה MAGIC MOCK?
---

## 🧠 Requirements

```
psutil>=5.9.0
psycopg2>=2.9.0
```

Install with:

```bash
pip install -r requirements.txt
```

---


# srs_app

A **SRS (Spaced Repetition System)** application to help you memorise key elements of programming languages.  

## 📄 Overview

`srs_app` is a simple command-line/interactive tool written in Python that allows you to create, store, and review “flashcards” (questions/answers) so that you can memorise syntax or concepts of programming languages (or anything else). It uses spaced-repetition principles to schedule reviews for optimal long-term retention.

## 🔧 Features

- Initialize a local database of flashcards (via `init_db.py`).  
- Add and manage “questions/answers” pairs.  
- Review flashcards in spaced-repetition mode.  
- Simple and minimal dependencies — easy to run locally.
- Works out-of-the-box with Python (see Requirements below).

Then follow the prompts in main.py to add flashcards or review them.

📁 Repository Structure

srs_app/
│   init_db.py         # to initialise the flashcards database
│   main.py            # main application entrypoint
│   requirements.txt   # Python dependencies (if any)
│   .gitignore
│   answers/           # (example) directory for answers/flashcards (if used)
│   instructions/      # (example) directory for instructions or sample cards (if used)

## 🚀 Quick Start

```bash
git clone https://github.com/ygigandet/srs_app.git
cd srs_app
python3 -m venv venv          # (optional) create virtual env
source venv/bin/activate      # (on Windows: `venv\\Scripts\\activate`)
pip install -r requirements.txt
python init_db.py             # initialize database
python main.py                # start the app
```

📝 How to Use

Run init_db.py to set up the database (if not already done).

Run main.py to start the interactive session.

Use the menu/options to add new flashcards (question + answer), review due flashcards, or list existing cards.

When reviewing, cards will be scheduled by spaced-repetition logic (oldest due first), helping you memorise efficiently over time.

⚠️ Still work in progress!

The SRS is not yet done.
More exercises needed to be added.

🧾 License

“All rights reserved”

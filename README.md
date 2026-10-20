# Expense Tracker: Python, Tkinter & MongoDB

**A desktop app to log the products you buy and add up what you've spent, built with Tkinter and MongoDB.**

![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)
![PyMongo](https://img.shields.io/badge/PyMongo-driver-green)

## Overview

A small personal-finance tool: you enter the name and price (in dirhams) of each product you buy, and the app stores it in a local MongoDB database, lists your purchases and works out your spending. It was built as a mini project to practise Python GUI programming with Tkinter/ttk and full CRUD operations against a NoSQL database through PyMongo.

## Key Features

- **Add a purchase:** product name and optional price, saved as a MongoDB document.
- **Automatic date stamp:** the purchase date (`YYYY-MM-DD`) is recorded. In `better.py`, a *Save Date Added* checkbox makes it optional.
- **List purchases:** a scrollable list showing `date - name - price`, refreshed after every change.
- **Edit a purchase:** select an item and update its name and/or price in a pop-up window.
- **Delete a purchase:** select an item and remove it.
- **Spending totals:** one button for the total of all purchases, another for today's total.
- **Styled ttk interface** (`clam` theme) with colour-coded action buttons.

The repo contains two versions of the app:

| File | Description |
|---|---|
| `main.py` | First version: product name required, date always saved. |
| `better.py` | Improved version: adds the *Save Date Added* checkbox and trims whitespace from inputs. |

## Tech Stack

- **Python 3**
- **Tkinter / ttk** (standard library) for the GUI
- **MongoDB** (local instance at `mongodb://localhost:27017/`, database `product_database`, collection `products`)
- **PyMongo** as the MongoDB driver

## Project Structure

```
PythonMiniProject/
├── main.py     # version 1 of the expense tracker
└── better.py   # version 2, with optional date saving
```

Each version is one self-contained script: it connects to MongoDB at startup, defines the CRUD and total functions, builds the Tkinter window and starts the event loop. Documents look like this:

```json
{ "name": "Coffee", "price": "12.5", "date_added": "2024-04-22" }
```

## Getting Started

**Prerequisites:** Python 3 with Tkinter (bundled with most Python installers; on Debian/Ubuntu run `sudo apt install python3-tk`) and a MongoDB server running locally on the default port 27017.

```bash
git clone https://github.com/AbdouniAbdessamad/PythonMiniProject.git
cd PythonMiniProject

pip install pymongo

# make sure MongoDB is running, e.g.:
# docker run -d -p 27017:27017 --name mongo mongo

python better.py     # or: python main.py
```

The database and collection are created automatically on the first insert.

## Possible Improvements

- **Store prices as numbers and validate input.** Prices are saved as strings, so a non-numeric price breaks the totals, and `better.py` can save an empty product.
- **Select items by `_id`, not list position.** Edit and delete currently match the list index to `collection.find()` order, which can target the wrong document if the order changes.
- **Finish the monthly total** (`calculate_total_this_month` is a stub in `main.py`), show the `dh` currency consistently (the list shows `$`), and move the connection string to configuration.
- **Merge the two versions** into one structured module (separate data layer and UI) with a `requirements.txt`.

## Author

**Abdessamad Abdouni**, Information Systems Engineering student at SUPMTI Rabat, Morocco
GitHub: [github.com/AbdouniAbdessamad](https://github.com/AbdouniAbdessamad)

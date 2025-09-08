
## Gyatt Compiler Site

### Installation

1. **Clone the repository:**
	```sh
	git clone https://github.com/leighton075/gyattcompilersite.git
	cd gyattcompilersite
	```

2. **Install Python (if not already installed):**
	- Python 3.7 or newer is recommended.

3. **Install Flask:**
	```sh
	pip install flask
	```

### Project Structure

```
gyattcompilersite/
├── app.py
├── static/
│   ├── script.js
│   └── styles.css
└── templates/
	 └── index.html
```

### Usage

1. **Run the Flask app:**
	```sh
	python app.py
	```
	By default, the site will be available at [http://localhost:5000](http://localhost:5000).

2. **Access the site:**
	- Open your browser and go to [http://localhost:5000](http://localhost:5000)

### Notes

- All static files (CSS, JS) should be placed in the `static` folder.
- The main HTML file should be in the `templates` folder.
- If you want to run on a different port, you can modify `app.py` or use Flask CLI:
  ```sh
  flask run --port=8000
  ```

---
For any issues, please open an issue on GitHub.

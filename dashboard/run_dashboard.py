from app import app
from pages.main_page import layout 

if __name__ == "__main__":
    app.layout = layout
    app.run_server(debug=False, host='0.0.0.0', port=8060)

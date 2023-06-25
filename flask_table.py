from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Define a route that will render the HTML template
@app.route('/')
def index():
    # Create a Pandas DataFrame with the table data
    data = {'Name': ['Alice', 'Bob'], 'Age': [25, 30]}
    df = pd.DataFrame(data)
    
    # Generate the HTML table using the to_html method
    table_html = df.to_html(index=False)
    
    # Render the HTML template and pass in the table data
    return render_template('index.html', table=table_html)

if __name__ == '__main__':
    app.run()
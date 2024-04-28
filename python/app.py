import sys
import pandas as pd
from flask import Flask, render_template, request, render_template_string, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('parquet_view.html')

@app.route('/load_parquet', methods=['POST'])
def load_parquet():
    file = request.files['file']
    min_row = request.form['minRow']
    max_row = request.form['maxRow']
    if not (min_row and max_row):
        return jsonify({'error': 'Please provide min and max row'})
    if (int(min_row) > int(max_row)):
        return jsonify({'error': 'Min row cannot be greater than max row'})
    if (int(max_row) - int(min_row) > 200):
        return jsonify({'error': 'Cannot load more than 200 rows at a time. Please provide a smaller range.'})
    
    if file:
        if file.filename.endswith('.parquet'):
            try:
                df = pd.read_parquet(file)
                num_rows = df.shape[0]
                if num_rows < int(max_row) + 1:
                    return jsonify({'error': 'Max row is greater than the number of rows in the file'})
                df = df.iloc[int(min_row):int(max_row)+1]
                data_html = df.to_html(classes="ui celled table", border=0)
                return jsonify({'data_html': data_html, 'num_rows': num_rows})
            except Exception as e:
                return jsonify({'error': str(e)})
        else:
            return jsonify({'error': 'File must be a parquet file'})
    else:
        return jsonify({'error': 'No file uploaded'})

if __name__ == '__main__':
    app.run(port=4999, debug=True)

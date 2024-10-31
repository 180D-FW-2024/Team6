from flask import Flask, request, render_template_string

app = Flask(__name__)
received_data = []

@app.route('/receive', methods=['POST'])
def receive_data():
    data = request.json
    if data:
        received_data.append(data)
        return {"status": "success", "message": "Data received"}, 200
    return {"status": "fail", "message": "No data received"}, 400

@app.route('/display', methods=['GET'])
def display_data():
    # Define HTML template to display received data
    html_template = '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Received Data</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 2em; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 8px 12px; border: 1px solid #ddd; text-align: left; }
            th { background-color: #f4f4f4; }
        </style>
      </head>
      <body>
        <h1>Received Data</h1>
        <table>
          <tr>
            <th>#</th>
            <th>Data</th>
          </tr>
          {% for index, data in received_data %}
          <tr>
            <td>{{ index + 1 }}</td>
            <td>{{ data }}</td>
          </tr>
          {% endfor %}
        </table>
      </body>
    </html>
    '''
    return render_template_string(html_template, received_data=enumerate(received_data))

if __name__ == '__main__':
    app.run(port=5000)
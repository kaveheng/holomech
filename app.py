from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sum', methods=['POST'])
def calculate_sum():
    data = request.get_json()
    sum_result = data['number1'] + data['number2']
    return jsonify({'sum': sum_result})

if __name__ == '__main__':
    app.run(debug=True)

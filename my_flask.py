from my_flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/madmax/csit8th/<word>', methods=['GET'])
def get_definition_proxy(word):
    external_api_url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'

    try:
        response = requests.get(external_api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        data = response.json()
        # You can modify the response or add additional processing here if needed
        return jsonify(data)
    except requests.exceptions.HTTPError as errh:
        return jsonify({'error': f"HTTP Error: {errh}"}), 500   
    except requests.exceptions.ConnectionError as errc:
        return jsonify({'error': f"Error Connecting: {errc}"}), 500
    except requests.exceptions.Timeout as errt:
        return jsonify({'error': f"Timeout Error: {errt}"}), 500
    except requests.exceptions.RequestException as err:
        return jsonify({'error': f"Error: {err}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

from flask import Flask, jsonify, request
import re
import subprocess
import time

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    return jsonify(message="Hello Developer")

@app.route('/', methods=['GET'])
def index():
    return "Welcome to my api home page !!!\n"

@app.route('/ping', methods=['POST'])
def ping():
    ip = request.json
    print(ip['ip'])
    response_dict = {}
    if is_valid_ip(ip['ip']):
        try:
            result = subprocess.check_output(["ping", "-c", "4", ip['ip']])
            response_dict[0] = result.decode()
        except subprocess.CalledProcessError as e:
            response_dict[0] = str(e)
        return jsonify(response_dict)
    else:
        response_dict[0] = "Invalid IP Address!"
        return jsonify(response_dict)

@app.route('/scan', methods=['POST'])
def scan():
    ip = request.json
    response_dict = {}
    if is_valid_ip(ip['ip']):
        if ip['ip'] in ['127.0.0.1', '']:
            response_dict[0] = "Can't Scan localhost"
            return jsonify(response_dict)
        print(ip['ip'])
        try:
            result = subprocess.check_output(["nmap", "-sV", "-A", "--script=default", ip['ip']])
            output_lines = result.decode().split('\n')
            for i, line in enumerate(output_lines):
                if 'Nmap done' not in line:
                    response_dict[i] = line
                else:
                    break
            response_dict.pop(len(response_dict) - 1, None)  
            time.sleep(1)
            print("[SENT]")
            return jsonify(response_dict)
        except subprocess.CalledProcessError as e:
            response_dict[0] = str(e)
            return jsonify(response_dict)
    else:
        response_dict[0] = "Invalid IP Address!"
        return jsonify(response_dict)

def is_valid_ip(ip):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return re.match(pattern, ip) is not None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)

import json
import os
import socket
import re

import yaml
import yamlordereddictloader
from flask import Flask, jsonify, url_for, request
from flask_cors import CORS, cross_origin

import generate_model

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

# training_stats = json.loads(open('results/api_experiment_run_0/training_statistics.json').read())
root_dir = os.path.abspath(__file__).strip(os.path.basename(__file__))

def find_csv(dir):
  """Returns the csv file found within specified directory"""

  for i in os.listdir(root_dir + '/' + dir):
    print(i)
    if re.match(r'(.*?)\.(csv)$',i):
      file_name = root_dir + dir +'/'+ i
      break

  return file_name

model_obj = generate_model.model(train_file_path=find_csv('train'),test_file_path=find_csv('test'))

@app.route("/")
def hello():

    html = "<h3>Testas {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" 
    return html.format(name=os.getenv("NAME", "asd"), hostname=socket.gethostname())

@app.route('/generate-model-file', methods=['POST'])
def form_example():
    if request.method == 'POST':
        print(request.get_json())
        try:
            name = request.get_json()['name']
        except:
            name = 'file'
        model_obj.make_model_file(name = name)
        return '<h3>model.yaml file created</h3>'


@app.route('/training-stats/', methods=['GET'])
def get_training_stats():
    pass


@app.route('/model_info/', methods=['GET'])
def get_model_data():
    with open('herefile.yaml') as f:
        model_data = yaml.load(f, Loader=yamlordereddictloader.Loader)
    return json.dumps(model_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2000, debug=True)

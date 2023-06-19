from flask import Flask, request, jsonify

app = Flask(__name__)

work_queue = []
work_id = 0


@app.route('/enqueue', methods=['POST'])
def enqueue():
    global work_id
    data = request.get_json()
    buffer = data['buffer']
    iterations = data['iterations']
    work = {'id': work_id, 'buffer': buffer, 'iterations': iterations}
    work_queue.append(work)
    work_id += 1
    return jsonify({'message': 'Work enqueued successfully'}), 200


@app.route('/dequeue', methods=['PUT'])
def dequeue():
    if len(work_queue) == 0:
        return jsonify({}), 200

    work = work_queue.pop(0)
    return jsonify(work), 200


@app.route('/updateWorkDone', methods=['PUT'])
def update_work_done():
    data = request.get_json()
    work_id = data['id']
    result = data['result']
    # TODO: Update the work status or do any necessary processing
    return jsonify({'message': 'Work status updated successfully'}), 200


@app.route('/killWorker', methods=['DELETE'])
def kill_worker():
    # TODO: Implement logic to gracefully stop the worker
    return jsonify({'message': 'Worker terminated successfully'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

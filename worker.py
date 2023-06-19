import hashlib
import argparse
import time
import requests
import json
import os

first_inst_ip = ""
second_inst_ip = ""
first_inst_turn = True

log_file_path = os.path.join(os.path.dirname(__file__), 'worker.log')

last_time_work = time.time()


def process(buffer, iterations):
    output = hashlib.sha512(buffer).hexdigest()

    for i in range(iterations - 1):
        output = hashlib.sha512(output.encode()).hexdigest()

    return output


def perform_work():
    global first_inst_turn
    global last_time_work

    inst_ip = first_inst_ip if first_inst_turn else second_inst_ip
    first_inst_turn = not first_inst_turn

    try:
        response = requests.put(f"http://{inst_ip}:5000/dequeue")
        log_message(f"Calling: http://{inst_ip}:5000/dequeue")
        work_item = response.json()

        log_message(f"workItem: {json.dumps(work_item)}")

        if not work_item:
            log_message('No work available.')
            return

        last_time_work = time.time()
        buffer = work_item['buffer']
        iterations = work_item['iterations']
        work_id = work_item['id']
        result = process(buffer, iterations)

        data = {'id': work_id, 'result': result}

        try:
            requests.put(f"http://{inst_ip}:5000/updateWorkDone", json=data)
            log_message(f"Calling: http://{inst_ip}:5000/updateWorkDone, {json.dumps(data)}")
        except Exception as e:
            log_message(f"Error calling http://{inst_ip}:5000/updateWorkDone : {str(e)}")

        log_message('Work completed:', result)

    except Exception as e:
        log_message(f"Error occurred while processing work: {str(e)}")


def check_last_work_time():
    global last_time_work

    log_message("Check if worker is needed")
    current_time = time.time()
    fifteen_minutes = 15 * 60  # 15 minutes in seconds

    if current_time - last_time_work > fifteen_minutes:
        log_message('Starting shut down...')
        terminate_inst()


def terminate_inst():
    try:
        requests.delete(f"http://{first_inst_ip}:5000/killWorker")
        log_message(f"Calling: http://{first_inst_ip}:5000/killWorker")
    except Exception as e:
        log_message(f"Error calling http://{first_inst_ip}:5000/killWorker : {str(e)}")


def log_message(msg):
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{msg}\n")


parser = argparse.ArgumentParser()
parser.add_argument('--firstInstIP', help='First instance IP address')
parser.add_argument('--secondInstIP', help='Second instance IP address')
args = parser.parse_args()

first_inst_ip = args.firstInstIP
second_inst_ip = args.secondInstIP

while True:
    perform_work()
    check_last_work_time()
    time.sleep(5)  # Wait for 5 seconds between each iteration

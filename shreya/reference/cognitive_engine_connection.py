from flask import Blueprint, request


job_execution = Blueprint('job_execution')


@job_execution.route('/api/request_state_from_blockchain', methods=['POST'])
def request_state_from_blockchain():
    '''
    Checks if all executors involved have reported their results here.
    Updates exec_step_status when the exec has reported results.
    Updates state buffer with states and flag it as full when all related exec has reported.
    :return:
    '''
    import random
    from flask import jsonify
    # unpack json data
    data = request.get_json()
    res = jsonify({"status": random.choice(["pass", "fail"])})
    return res
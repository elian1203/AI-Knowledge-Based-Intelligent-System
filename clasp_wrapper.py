import subprocess


def clasp(program_input):
    run = subprocess.run(['clasp'], input=program_input.encode(), stdout=subprocess.PIPE)
    print(run.stdout)
    return run.stdout

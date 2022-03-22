import subprocess


def clasp(program_input):
    """
    Calls clasp command (executable should be in current dir or PATH
    :param program_input: clasp appropriate input (p cnf 4 6......)
    :return: True if satisfiable, False if not satisfiable
    """
    run = subprocess.run(['clasp'], input=program_input.encode(), stdout=subprocess.PIPE)

    for line in run.stdout.splitlines():
        if line.startswith('s SATISFIABLE'):
            return True
        elif line.startswith('s UNSATISFIABLE'):
            return False

    raise Exception('Missing clasp file! Unable to process constraints.')

import constants
from constants import operators_map


class VMWriter:
    def __init__(self, _vm_file):
        self.vm_file = _vm_file
        self.commands = {}
        self.init_commands()

    def init_commands(self):
        self.commands[constants.PUSH] = 'push {} {}\n'
        self.commands[constants.POP] = 'pop {} {}\n'
        self.commands[constants.ARITH] = '{}\n'
        self.commands[constants.LABEL] = 'label {}\n'
        self.commands[constants.GOTO] = 'goto {}\n'
        self.commands[constants.IF] = 'if-goto {}\n'
        self.commands[constants.CALL] = 'call {} {}\n'
        self.commands[constants.FUNCTION] = 'function {} {}\n'
        self.commands[constants.RETURN] = 'return\n'

    def write_push(self, segment, index):

        self.vm_file.write(self.commands[constants.PUSH].format(segment, index))

    def write_pop(self, segment, index):
        self.vm_file.write(self.commands[constants.POP].format(segment, index))

    def write_arithmetic(self, command):
        if command in operators_map:
            self.vm_file.write(operators_map[command] + '\n')
        elif command == constants.Symbol.STAR.value:
            self.write_call('Math.multiply', 2)
        elif command == constants.Symbol.DIV.value:
            self.write_call('Math.divide', 2)
        else:
            self.vm_file.write(command + '\n')

    def write_label(self, label):
        self.vm_file.write(self.commands[constants.LABEL].format(label))

    def write_goto(self, label):
        self.vm_file.write(self.commands[constants.GOTO].format(label))

    def write_if(self, label):
        self.vm_file.write(self.commands[constants.IF].format(label))

    def write_call(self, name, n_args):
        self.vm_file.write(self.commands[constants.CALL].format(name, n_args))

    def write_function(self, name, n_locals):
        self.vm_file.write(self.commands[constants.FUNCTION].format(name, n_locals))

    def write_return(self):
        self.vm_file.write(self.commands[constants.RETURN])






class IntcodeComputer:
    memory = None
    inputs = None
    outputs = []
    memory_index = 0
    is_complete = False
    relative_base = 0

    def __init__(self, initial_memory, initial_inputs):
        self.memory = initial_memory.copy()
        self.inputs = initial_inputs.copy()
        self.outputs = []
        self.memory_index = 0
        self.is_complete = False
        self.is_suspended = False
        self.relative_base = 0

    def extend_memory_to_size(self, size):
        current_memory_size = len(self.memory)
        self.memory = [
            self.memory[index] if index < current_memory_size else 0
            for index in range(size)
        ]

    @staticmethod
    def read_instruction(instruction):
        opcode = instruction % 100
        new_instruction = instruction // 100
        parameter_count = 3 if opcode in [1, 2, 7, 8] else 2 if opcode in [5, 6] else 1
        parameter_modes = [
            (new_instruction // (10 ** x)) % 10 for x in range(parameter_count)
        ]
        write_parameter_indexes = [2] if opcode in [1, 2, 7, 8] else [0] if opcode in [3, 9] else []
        return opcode, parameter_modes, write_parameter_indexes

    def read_parameter(self, parameter_mode, relative_index, write_parameter_indexes):
        index = self.memory_index + relative_index + 1
        raw = self.memory[index]
        literal_mode = relative_index in write_parameter_indexes
        if parameter_mode == 0:
            if literal_mode:
                return raw
            return self.memory[raw]
        elif parameter_mode == 1:
            return raw
        elif parameter_mode == 2:
            if literal_mode:
                return raw + self.relative_base
            return self.memory[raw + self.relative_base]
        else:
            raise Exception('Unexpected parameter mode: {}'.format(parameter_mode))

    def read_parameters(self, parameter_modes, write_parameter_indexes):
        return [
            self.read_parameter(parameter_mode, relative_index, write_parameter_indexes)
            for relative_index, parameter_mode in enumerate(parameter_modes)
        ]

    def safe_write_to_memory(self, index, value):
        try:
            self.memory[index] = value
        except IndexError:
            self.extend_memory_to_size(index + 1)
            self.memory[index] = value

    def execute_opcode(self, opcode, parameters):
        if opcode == 1:
            self.memory[parameters[2]] = parameters[0] + parameters[1]
        elif opcode == 2:
            self.safe_write_to_memory(parameters[2], parameters[0] * parameters[1])
        elif opcode == 3:
            try:
                input = self.inputs.pop(0)
            except IndexError:
                raise Exception('Waiting on input')
            else:
                self.safe_write_to_memory(parameters[0], input)
        elif opcode == 4:
            self.outputs.append(parameters[0])
        elif opcode == 5:
            if parameters[0] != 0:
                self.memory_index = parameters[1]
        elif opcode == 6:
            if parameters[0] == 0:
                self.memory_index = parameters[1]
        elif opcode == 7:
            value = 1 if parameters[0] < parameters[1] else 0
            self.safe_write_to_memory(parameters[2], value)
        elif opcode == 8:
            value = 1 if parameters[0] == parameters[1] else 0
            self.safe_write_to_memory(parameters[2], value)
        elif opcode == 9:
            self.relative_base += parameters[0]
        else:
            raise Exception('Invalid opcode: {}'.format(opcode))

    def append_new_input(self, new_input):
        self.inputs.append(new_input)
        self.is_suspended = False

    def get_is_complete(self):
        return self.is_complete

    def pop_last_output(self):
        try:
            return self.outputs.pop()
        except IndexError:
            return None

    def run(self):
        while not self.is_complete and not self.is_suspended:
            instruction = self.memory[self.memory_index]
            cached_memory_index = self.memory_index
            if instruction == 99:
                self.is_complete = True
                break

            opcode, parameter_modes, write_parameter_indexes = self.read_instruction(instruction)
            parameters = self.read_parameters(parameter_modes, write_parameter_indexes)

            try:
                self.execute_opcode(opcode, parameters)
            except Exception:
                self.is_suspended = True
                break

            if self.memory_index == cached_memory_index:
                self.memory_index += len(parameters) + 1

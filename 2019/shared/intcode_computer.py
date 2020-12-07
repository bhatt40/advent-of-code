class IntcodeComputer:
    memory = None
    inputs = None
    outputs = []
    memory_index = 0
    is_complete = False

    def __init__(self, initial_memory, initial_inputs):
        self.memory = initial_memory.copy()
        self.inputs = initial_inputs.copy()
        self.outputs = []
        self.memory_index = 0
        self.is_complete = False

    @staticmethod
    def read_instruction(instruction):
        opcode = instruction % 100
        new_instruction = instruction // 100
        parameter_count = 3 if opcode in [1, 2, 7, 8] else 2 if opcode in [5, 6] else 1
        parameter_modes = [
            (new_instruction // (10 ** x)) % 10 for x in range(parameter_count)
        ]
        if opcode not in [4, 5, 6]:
            parameter_modes[-1] = 1
        return opcode, parameter_modes

    def read_parameters(self, parameter_modes):
        return [
            self.memory[self.memory[self.memory_index + index + 1]] if parameter_mode == 0 else
            self.memory[self.memory_index + index + 1]
            for index, parameter_mode in enumerate(parameter_modes)
        ]

    def calculate_target_value(self, opcode, parameters):
        if opcode == 1:
            return parameters[0] + parameters[1]
        elif opcode == 2:
            return parameters[0] * parameters[1]
        elif opcode == 3:
            try:
                return self.inputs.pop(0)
            except IndexError:
                raise Exception('Waiting on input')
        elif opcode == 4:
            return parameters[0]
        elif opcode == 5:
            return parameters[1] if parameters[0] != 0 else None
        elif opcode == 6:
            return parameters[1] if parameters[0] == 0 else None
        elif opcode == 7:
            return 1 if parameters[0] < parameters[1] else 0
        elif opcode == 8:
            return 1 if parameters[0] == parameters[1] else 0

        raise Exception('Invalid opcode: {}'.format(opcode))

    def calculate_target_index(self, opcode, parameters):
        if opcode in [1, 2, 7, 8]:
            return parameters[2]
        elif opcode in [5, 6]:
            return self.memory_index
        return parameters[0]

    def write_to_output(self, opcode, value):
        if opcode == 4:
            self.outputs.append(value)

    def write_to_memory(self, opcode, index, value):
        if opcode != 4 and value is not None:
            self.memory[index] = value

    # @staticmethod
    # def calculate_new_input_index(opcode, input_index):
    #     if opcode == 3:
    #         return input_index + 1
    #     return input_index

    def get_is_complete(self):
        return self.is_complete

    def get_outputs(self):
        return self.outputs

    def run(self):
        while self.memory_index < len(self.memory):
            if self.memory[self.memory_index] == 99:
                self.is_complete = True
                break

            instruction = self.memory[self.memory_index]
            opcode, parameter_modes = self.read_instruction(instruction)
            parameters = self.read_parameters(parameter_modes)

            try:
                target_value = self.calculate_target_value(opcode, parameters)
            except Exception:
                break
            target_index = self.calculate_target_index(opcode, parameters)

            self.write_to_output(opcode, target_value)
            self.write_to_memory(opcode, target_index, target_value)

            if self.memory[self.memory_index] == instruction:
                self.memory_index += len(parameters) + 1
            else:
                self.memory_index = target_value

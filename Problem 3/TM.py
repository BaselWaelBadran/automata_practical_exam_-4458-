class TuringMachine:
    def __init__(self):
        # Define states
        self.states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q_accept', 'q_reject'}
        # Define input alphabet
        self.input_alphabet = {'0', '1'}
        # Define tape alphabet (including blank and markers)
        self.tape_alphabet = {'0', '1', 'X', 'Y', 'W', 'Z', '_'}  # _ is blank
        # Transition function: (state, tape_symbol) -> (next_state, write_symbol, direction)
        self.transitions = {}
        # Start state
        self.start_state = 'q0'
        # Accept and reject states
        self.accept_state = 'q_accept'
        self.reject_state = 'q_reject'
        # Configure transitions
        self.configure_transitions()

    def configure_transitions(self):
        # q0: Check if tape is empty or start processing
        self.transitions[('q0', '_')] = ('q_accept', '_', 'R')  # Empty tape, accept (n=0)
        self.transitions[('q0', '0')] = ('q1', 'X', 'R')  # Mark first 0
        self.transitions[('q0', '1')] = ('q_reject', '1', 'R')  # No 0, reject
        
        # q1: Move right to find first unmarked 1 (second block)
        self.transitions[('q1', '0')] = ('q1', '0', 'R')
        self.transitions[('q1', '1')] = ('q2', 'Y', 'R')  # Mark first 1
        self.transitions[('q1', 'X')] = ('q1', 'X', 'R')
        self.transitions[('q1', 'Y')] = ('q1', 'Y', 'R')
        self.transitions[('q1', 'W')] = ('q1', 'W', 'R')
        self.transitions[('q1', 'Z')] = ('q1', 'Z', 'R')
        self.transitions[('q1', '_')] = ('q_reject', '_', 'R')  # No 1, reject
        
        # q2: Move right to find first unmarked 0 (third block)
        self.transitions[('q2', '1')] = ('q2', '1', 'R')
        self.transitions[('q2', '0')] = ('q3', 'W', 'R')  # Mark second 0
        self.transitions[('q2', 'X')] = ('q2', 'X', 'R')
        self.transitions[('q2', 'Y')] = ('q2', 'Y', 'R')
        self.transitions[('q2', 'W')] = ('q2', 'W', 'R')
        self.transitions[('q2', 'Z')] = ('q2', 'Z', 'R')
        self.transitions[('q2', '_')] = ('q_reject', '_', 'R')  # No 0, reject
        
        # q3: Move right to find first unmarked 1 (fourth block)
        self.transitions[('q3', '0')] = ('q3', '0', 'R')
        self.transitions[('q3', '1')] = ('q4', 'Z', 'L')  # Mark second 1
        self.transitions[('q3', 'X')] = ('q3', 'X', 'R')
        self.transitions[('q3', 'Y')] = ('q3', 'Y', 'R')
        self.transitions[('q3', 'W')] = ('q3', 'W', 'R')
        self.transitions[('q3', 'Z')] = ('q3', 'Z', 'R')
        self.transitions[('q3', '_')] = ('q_reject', '_', 'R')  # No 1, reject
        
        # q4: Move left to find start of tape
        self.transitions[('q4', '0')] = ('q4', '0', 'L')
        self.transitions[('q4', '1')] = ('q4', '1', 'L')
        self.transitions[('q4', 'X')] = ('q4', 'X', 'L')
        self.transitions[('q4', 'Y')] = ('q4', 'Y', 'L')
        self.transitions[('q4', 'W')] = ('q4', 'W', 'L')
        self.transitions[('q4', 'Z')] = ('q4', 'Z', 'L')
        self.transitions[('q4', '_')] = ('q5', '_', 'R')  # Found start, move right
        
        # q5: Check if more unmarked 0, 1 exist
        self.transitions[('q5', '0')] = ('q1', 'X', 'R')  # More 0, repeat
        self.transitions[('q5', '1')] = ('q_reject', '1', 'R')  # Unmarked 1, reject
        self.transitions[('q5', 'X')] = ('q5', 'X', 'R')
        self.transitions[('q5', 'Y')] = ('q5', 'Y', 'R')
        self.transitions[('q5', 'W')] = ('q5', 'W', 'R')
        self.transitions[('q5', 'Z')] = ('q5', 'Z', 'R')
        self.transitions[('q5', '_')] = ('q6', '_', 'L')  # No more 0, check tape
        
        # q6: Verify tape is fully marked
        self.transitions[('q6', '0')] = ('q_reject', '0', 'L')
        self.transitions[('q6', '1')] = ('q_reject', '1', 'L')
        self.transitions[('q6', 'X')] = ('q6', 'X', 'L')
        self.transitions[('q6', 'Y')] = ('q6', 'Y', 'L')
        self.transitions[('q6', 'W')] = ('q6', 'W', 'L')
        self.transitions[('q6', 'Z')] = ('q6', 'Z', 'L')
        self.transitions[('q6', '_')] = ('q_accept', '_', 'R')  # Fully marked, accept

    def simulate(self, input_string):
        # Initialize tape (dictionary for sparse representation)
        tape = {}
        for i, char in enumerate(input_string):
            tape[i] = char
        head = 0  # Start at leftmost position
        
        # Initialize state
        current_state = self.start_state
        
        # Validate input
        for char in input_string:
            if char not in self.input_alphabet:
                return False
        
        # Simulate TM
        while True:
            # Get current tape symbol (blank if position not in tape)
            tape_symbol = tape.get(head, '_')
            
            # Check if in accept or reject state
            if current_state == self.accept_state:
                return True
            if current_state == self.reject_state:
                return False
            
            # Get transition
            transition = self.transitions.get((current_state, tape_symbol))
            if transition is None:
                return False  # No transition, reject
            
            # Apply transition
            next_state, write_symbol, direction = transition
            tape[head] = write_symbol  # Write to tape
            current_state = next_state  # Update state
            
            # Move head
            if direction == 'L':
                head -= 1
            elif direction == 'R':
                head += 1
            # No need for 'H' as we halt on accept/reject

# Test the implementation
def test():
    tm = TuringMachine()
    
    # Unit-Test cases
    string = "0101"
    if tm.simulate(string) == True:
        print("String accepted!")
    else:
        print("String rejected!")

if __name__ == "__main__":
    test()
class PDA:
    def __init__(self):
        # Define states
        self.states = {'q0', 'q1', 'q2', 'q_accept'}
        # Define input alphabet
        self.input_alphabet = {'a', 'b'}
        # Define stack alphabet (including bottom marker Z)
        self.stack_alphabet = {'a', 'b', 'Z'}
        # Transition function (simplified as a dictionary of tuples)
        self.transitions = {}
        # Start state
        self.start_state = 'q0'
        # Accept state
        self.accept_state = 'q_accept'
        # Initial stack symbol
        self.stack_start = 'Z'

    def configure_transitions(self):
        # q0: Push first half
        for symbol in self.input_alphabet:
            self.transitions[('q0', symbol, None)] = ('q0', [symbol])  # Push symbol
        # q0 to q1: Middle transition
        self.transitions[('q0', None, None)] = ('q1', [])  # No input, move to q1
        # q1 to q2: Move to pop state (consume middle character)
        for symbol in self.input_alphabet:
            self.transitions[('q1', symbol, None)] = ('q2', [])  # Consume middle, move to q2
        # q2: Pop and match second half
        for symbol in self.input_alphabet:
            self.transitions[('q2', symbol, symbol)] = ('q2', [])  # Pop if match
        # q2 to q_accept: Accept if stack is at Z
        self.transitions[('q2', None, 'Z')] = ('q_accept', [])  # Pop Z, accept

    def simulate(self, input_string):
        # Check if length is odd
        length = len(input_string)
        if length % 2 == 0:  # Even length, reject immediately
            return False
        
        # Initialize current state and stack
        current_state = self.start_state
        stack = [self.stack_start]
        
        # Configure transitions before simulation
        self.configure_transitions()
        
        # Push first (length - 1) // 2 characters
        i = 0
        half = (length - 1) // 2  # Number of characters to push
        while i < half:
            symbol = input_string[i]
            if symbol not in self.input_alphabet:
                return False
            # Push transition
            transition = self.transitions.get(('q0', symbol, None))
            if transition:
                next_state, stack_action = transition
                current_state = next_state
                stack.extend(stack_action)
            else:
                return False
            i += 1
        
        # Middle transition (consume middle character)
        if i < length:
            # Move to q1
            transition = self.transitions.get(('q0', None, None))
            if transition:
                next_state, stack_action = transition
                current_state = next_state
            else:
                return False
            
            # Consume middle character
            symbol = input_string[i]
            if symbol not in self.input_alphabet:
                return False
            top_stack = stack[-1] if stack else None
            transition = self.transitions.get(('q1', symbol, None))
            if transition:
                next_state, stack_action = transition
                current_state = next_state
            else:
                return False
            i += 1
        
        # Pop and match the rest
        while i < length:
            symbol = input_string[i]
            if symbol not in self.input_alphabet:
                return False
            top_stack = stack[-1] if stack else None
            transition = self.transitions.get(('q2', symbol, top_stack))
            if transition:
                next_state, stack_action = transition
                current_state = next_state
                if top_stack in self.input_alphabet:
                    stack.pop()
            else:
                return False
            i += 1
        
        # Final checks
        while current_state == 'q2':
            top_stack = stack[-1] if stack else None
            transition = self.transitions.get(('q2', None, top_stack))
            if transition:
                next_state, stack_action = transition
                current_state = next_state
                if top_stack == 'Z':
                    break
            else:
                return False
        
        return current_state == self.accept_state and len(stack) == 1 and stack[0] == 'Z'

# Test the implementation
def test():
    pda = PDA()
    
    # Unit-Test cases
    string = "ababa"
    if pda.simulate(string) == True:
        print("String accepted!")
    else:
        print("String rejected!")

if __name__ == "__main__":
    test()

    # pda = PDA()
    # # Test cases
    # assert pda.simulate("a") == True, "Single 'a' should be accepted"
    # assert pda.simulate("aba") == True, "'aba' should be accepted"
    # assert pda.simulate("abcba") == True, "'abcba' should be accepted"
    # assert pda.simulate("ab") == False, "'ab' (even) should be rejected"
    # assert pda.simulate("abba") == False, "'abba' (even) should be rejected"
    # assert pda.simulate("abca") == False, "'abca' (not palindrome) should be rejected"
    # print("All tests passed!")
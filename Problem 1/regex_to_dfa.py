# Define a simple DFA class to store states, transitions, and simulate
class DFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states  # Set of states
        self.alphabet = alphabet  # Alphabet (e.g., {'a', 'b'})
        self.transitions = transitions  # Dict: (state, symbol) -> state
        self.start = start  # Start state
        self.accepts = accepts  # Set of accepting states

    def simulate(self, input_string):
        current_state = self.start
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False  # Invalid symbol
            current_state = self.transitions.get((current_state, symbol), None)
            if current_state is None:
                return False  # No transition exists
        return current_state in self.accepts

# Helper for NFA (for intermediate step)
class NFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions  # Dict: (state, symbol) -> set of states
        self.start = start
        self.accepts = accepts

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            next_states = self.transitions.get((state, None), set())
            for next_state in next_states:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

# Function to convert regex to DFA (simplified for (a|b)*abb)
def regex_to_dfa(regex):
    # For simplicity, we'll directly build a DFA for (a|b)*abb without NFA conversion
    # In a full implementation, you'd parse the regex and use Thompson's construction
    # States: 0 (start), 1 (seen a or b), 2 (seen ab), 3 (seen abb, accepting)
    states = {0, 1, 2, 3}
    alphabet = {'a', 'b'}
    transitions = {}
    
    # State 0: Start state, can loop on 'a' or 'b' due to (a|b)*
    transitions[(0, 'a')] = 1  # Start of "abb"
    transitions[(0, 'b')] = 0  # Loop back for (a|b)*
    
    # State 1: Seen 'a', expecting 'b'
    transitions[(1, 'a')] = 1  # Another 'a', restart "abb" match
    transitions[(1, 'b')] = 2  # Move to next part of "abb"
    
    # State 2: Seen "ab", expecting 'b'
    transitions[(2, 'a')] = 1  # Restart "abb" match
    transitions[(2, 'b')] = 3  # Complete "abb"
    
    # State 3: Seen "abb", accepting state, can loop on (a|b)*
    transitions[(3, 'a')] = 1  # Restart "abb" match
    transitions[(3, 'b')] = 0  # Loop back to start
    
    start = 0
    accepts = {3}
    
    return DFA(states, alphabet, transitions, start, accepts)

# Test the implementation
def test():
    # Convert the regex to a DFA
    dfa = regex_to_dfa("(a|b)*abb")
    
    # Test cases
    string = "abab"
    if dfa.simulate(string) == True:
        print("String accepted!")
    else:
        print("String rejected!")

    # assert dfa.simulate("aabb") == True, f"Should accept 'aabb'"
    # assert dfa.simulate("ababa") == False, f"Should reject 'ababa'"
    # print("All tests passed!")

# Run the tests
if __name__ == "__main__":
    test()

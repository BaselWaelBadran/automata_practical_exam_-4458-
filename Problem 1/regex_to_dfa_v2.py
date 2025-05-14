# Define NFA class with epsilon transitions
class NFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions  # (state, symbol) -> set of states (symbol can be None for epsilon)
        self.start = start
        self.accepts = accepts

    def epsilon_closure(self, states):
        """
            Computes the set of all states reachable from a given set via epsilon transitions
        """
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()  # Pops a state from the stack to process.
            next_states = self.transitions.get((state, None), set())  # Looks up epsilon transitions from the current state
            for next_state in next_states:  # Iterates over all states reachable via epsilon transitions.
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

# Define DFA class
class DFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start = start
        self.accepts = accepts

    def simulate(self, input_string):
        """
            Determines whether an input string is accepted by the DFA, fulfilling the problem's simulation requirement.
        """
        current_state = self.start
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            current_state = self.transitions.get((current_state, symbol), None)
            if current_state is None:
                return False
        return current_state in self.accepts

# Helper to create unique state IDs
state_counter = 0
def new_state():  # function to generate unique state IDs.
    """
        Provides fresh state IDs to avoid conflicts when building NFAs and DFAs.
    """
    global state_counter
    state_counter += 1
    return state_counter

# Convert infix regex to postfix notation (handles operator precedence)
def to_postfix(regex):
    """
        Prepares for parsing the regex into a form where operators are applied in the correct order.
        Sets up precedence levels (star > concatenation > union), an operator stack, a postfix list, and an index to traverse the regex.
    """
    precedence = {'*': 3, '.': 2, '|': 1}  # Implicit concatenation as '.'
    operators = []
    postfix = []
    i = 0
    while i < len(regex):  # Loops through each character in the regex.
        """
            - Adds symbols (a, b) directly to postfix.
            - Pushes opening parentheses onto operators.
            - Pops operators to postfix until a matching parenthesis is found for closing parentheses.
            - Pops operators with higher or equal precedence and pushes the current operator (* or |).
            - Inserts implicit concatenation (.) when symbols or closing parentheses are followed by symbols or opening parentheses.
        """
        c = regex[i]  # Gets the current character
        if c in 'ab':  # Symbols
            postfix.append(c)  # If it’s a symbol, adds it directly to the postfix expression.
        elif c == '(':
            operators.append(c)  # Pushes the parenthesis onto the operator stack.
        elif c == ')':
            while operators and operators[-1] != '(':  # 
                postfix.append(operators.pop())  # Pops operators and adds them to postfix until an opening parenthesis is found.
            operators.pop()  # Remove '('
        elif c in '*|':
            while (operators and operators[-1] != '(' and precedence.get(operators[-1], 0) >= precedence[c]):
                postfix.append(operators.pop())
            operators.append(c)
        # Insert implicit concatenation (.) between consecutive symbols or after ')'
        if i + 1 < len(regex):
            next_char = regex[i + 1]
            if (c in 'ab)' and next_char in 'ab(') or (c in '*' and next_char in 'ab('):
                while (operators and operators[-1] != '(' and 
                       precedence.get(operators[-1], 0) >= precedence['.']):
                    postfix.append(operators.pop())
                operators.append('.')
        i += 1
    
    while operators:
        postfix.append(operators.pop())
    return ''.join(postfix)

# Build NFA from postfix regex using Thompson's construction
def build_nfa(regex):
    global state_counter  # Declares state_counter as global to reset it.
    state_counter = 0
    stack = []
    
    # Convert to postfix
    postfix = to_postfix(regex)
    
    for c in postfix:
        if c in 'ab':  # Symbol
            "Symbol (a, b): Creates a 2-state NFA (start → accept on symbol) and pushes it."
            start = new_state()
            accept = new_state()
            transitions = {(start, c): {accept}}
            alphabet = {c}
            stack.append(NFA({start, accept}, alphabet, transitions, start, {accept}))
        elif c == '.':  # Concatenation
            "Concatenation (.): Pops two NFAs, connects the first's accept state to the second's start with an epsilon transition, and pushes the combined NFA."
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            # Connect nfa1's accept state to nfa2's start state with epsilon transition
            transitions = nfa1.transitions.copy()
            transitions.update(nfa2.transitions)
            transitions[(nfa1.accepts.pop(), None)] = {nfa2.start}  # Connects the accepting state of the first NFA to the start state of the second NFA with an epsilon transition.
            states = nfa1.states | nfa2.states
            alphabet = nfa1.alphabet | nfa2.alphabet
            stack.append(NFA(states, alphabet, transitions, nfa1.start, nfa2.accepts))
        elif c == '|':  # Union
            "Union (|): Pops two NFAs, creates a new start and accept state with epsilon transitions to/from both NFAs, and pushes the result."
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = new_state()
            accept = new_state()
            transitions = nfa1.transitions.copy()
            transitions.update(nfa2.transitions)
            transitions[(start, None)] = {nfa1.start, nfa2.start}  # Adds epsilon transitions from the new start state to the start states of both NFAs.
            transitions[(list(nfa1.accepts)[0], None)] = {accept}  # Adds an epsilon transition from the first NFA’s accepting state to the new accepting state.
            transitions[(list(nfa2.accepts)[0], None)] = {accept}
            states = nfa1.states | nfa2.states | {start, accept}
            alphabet = nfa1.alphabet | nfa2.alphabet
            stack.append(NFA(states, alphabet, transitions, start, {accept}))
        elif c == '*':  # Kleene star
            "Kleene Star (*): Pops an NFA, adds new start and accept states with epsilon loops, and pushes the result."
            nfa = stack.pop()
            start = new_state()
            accept = new_state()
            transitions = nfa.transitions.copy()
            transitions[(start, None)] = {nfa.start, accept}  # Skip or enter, Adds epsilon transitions from the new start state to the original start state and the new accepting state (allows skipping the NFA).
            transitions[(list(nfa.accepts)[0], None)] = {nfa.start, accept}  # Loop back or exit (allows repetition)
            states = nfa.states | {start, accept}
            alphabet = nfa.alphabet
            stack.append(NFA(states, alphabet, transitions, start, {accept}))
    
    return stack[0]

# Convert NFA to DFA using subset construction
def nfa_to_dfa(nfa):
    dfa_states = {}
    state_id = 0
    dfa_transitions = {}
    dfa_accepts = set()
    dfa_alphabet = nfa.alphabet
    # A frozenset is immutable, meaning once it’s created, it cannot be modified it
    start_set = frozenset(nfa.epsilon_closure({nfa.start}))  # it finds all states reachable from nfa.start via epsilon transitions
    dfa_states[start_set] = state_id
    state_id += 1
    
    queue = [start_set]
    while queue:  # Loops until the queue is empty.
        current_set = queue.pop(0)
        current_dfa_state = dfa_states[current_set]
        
        if any(state in nfa.accepts for state in current_set): 
            """For each set, checks if it contains an NFA accepting state to mark it as a DFA accepting state."""
            dfa_accepts.add(current_dfa_state)
        
        for symbol in dfa_alphabet: 
            """For each symbol, computes the set of NFA states reachable (including epsilon closures) and creates a new DFA state if unseen."""
            next_states = set()
            for state in current_set:
                next_states.update(nfa.transitions.get((state, symbol), set()))
            next_set = frozenset(nfa.epsilon_closure(next_states))
            
            if not next_set:
                continue
                
            if next_set not in dfa_states:
                dfa_states[next_set] = state_id
                state_id += 1
                queue.append(next_set)
            
            dfa_transitions[(current_dfa_state, symbol)] = dfa_states[next_set]
    
    return DFA(set(dfa_states.values()), dfa_alphabet, dfa_transitions, dfa_states[start_set], dfa_accepts)  # Creates a DFA with the computed states, alphabet, transitions, start state, and accepting states.

# Main function to convert regex to DFA
def regex_to_dfa(regex):
    nfa = build_nfa(regex)
    dfa = nfa_to_dfa(nfa)
    return dfa

# Test the implementation
def test():

    # Convert the regex to a DFA
    dfa = regex_to_dfa("(a|b)*abb")
    
    # Unit-Test cases
    string = "aabb"
    if dfa.simulate(string) == True:
        print("String accepted!")
    else:
        print("String rejected!")


# Run the tests
if __name__ == "__main__":
    test()
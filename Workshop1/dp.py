import numpy as np

def one_step_lookahead(environment, state, V, discount_factor):
    """
    Helper function to calculate a state-value function.
    :param environment: Initialized OpenAI gym environment object.
    :param state: Agent's state to consider (integer).
    :param V: The value-function represented as an array. Vector of length nS.
    :param discount_factor: MDP discount factor.
    :return: A vector of length nA containing the expected value of each action.
    """

    action_values = np.zeros(environment.nA)

    for action in range(environment.nA):

        for probability, next_state, reward, terminated in environment.P[state][action]:
            action_values[action] += probability * (reward + discount_factor * V[next_state])

    return action_values


def policy_evaluation(policy, environment, V, discount_factor=1.0, theta=1e-9):
    """
    Evaluate a policy given a deterministic environment.
    :param policy: Matrix of a size nSxnA, each cell represents a probability of taking action a in state s.
    :param environment: Initialized OpenAI gym environment object.
    :param V: The value-function represented as an array. Vector of length nS.
    :param discount_factor: MDP discount factor. Float in range from 0 to 1.
    :param theta: A threshold of a value function change.
    :return: A vector of size nS, which represent a value function for each state.
    """

    # Number of evaluation iterations
    evaluation_iterations = 1

    # Repeat until value change is below the threshold
    while True:

        # Initialize a change of value function as zero
        delta = 0

        # Iterate though each state
        for state in range(environment.nS):

            # Initial a new value of current state
            v = 0

            # Try all possible actions which can be taken from this state
            for action, action_probability in enumerate(policy[state]):

                # Evaluate how good each next state will be
                for state_probability, next_state, reward, terminated in environment.P[state][action]:

                    # Calculate the expected value
                    v += action_probability * state_probability * (reward + discount_factor * V[next_state])

            # Calculate the absolute change of value function
            delta = max(delta, np.abs(V[state] - v))

            # Update value function
            V[state] = v

        evaluation_iterations += 1

        # Terminate if value change is insignificant
        if delta < theta:
            print(f'Policy evaluated in {evaluation_iterations} iterations.')
            return V


def policy_iteration(environment, discount_factor=1.0):
    """
    Policy iteration algorithm to solve MDP.
    :param environment: Initialized OpenAI gym environment object.
    :param discount_factor: MPD discount factor. Float in range from 0 to 1.
    :return: tuple(policy, V), which consist of an optimal policy matrix and value function for each state.
    """
    # Start with a random policy
    policy = np.ones([environment.nS, environment.nA]) / environment.nA

    # Initialize state-value function with zeros for each environment state
    V = np.zeros(environment.nS)

    # Initialize counter of evaluated policies
    evaluated_policies = 1

    # Repeat until convergence or critical number of iterations reached
    while True:

        stable_policy = True

        # Evaluate current policy
        V = policy_evaluation(policy, environment, V, discount_factor=discount_factor)

        # Go through each state and try to improve actions that were taken
        for state in range(environment.nS):

            # Choose the best action in a current state under current policy
            current_action = np.argmax(policy[state])

            # Look one step ahead and evaluate if current action is optimal
            # We will try every possible action in a current state
            action_values = one_step_lookahead(environment, state, V, discount_factor)

            # Select a better action
            best_action = np.argmax(action_values)

            # If action didn't change
            if current_action != best_action:
                stable_policy = False

            # Greedy policy update
            policy[state] = np.eye(environment.nA)[best_action]

        evaluated_policies += 1

        # If the algorithm converged and policy is not changing anymore, than return final policy and value function
        if stable_policy:
            print(f'Evaluated {evaluated_policies} policies.')
            return policy, V

####################### TO-DO #######################
# Replace None with your code
def value_iteration(environment, discount_factor=1.0, theta=1e-9):
    """
    Value Iteration algorithm to solve MDP.
    :param environment: Initialized OpenAI environment object.
    :param theta: Stopping threshold. If the value of all states changes less than theta in one iteration - we are done.
    :param discount_factor: MDP discount factor.
    :return: tuple (policy, V) which contains optimal policy and optimal value function.
    """

    # Initialize state-value function with zeros for each environment state
    V = np.zeros(environment.nS)
    
    iteration = 0
    
    while True:

        # Early stopping condition
        delta = 0

        # Update each state
        for state in range(environment.nS):

            # Do a one-step lookahead to calculate state-action values
            action_values = None

            # Select the highest state-action value
            best_action_value = None

            # Calculate change in value
            delta = max(delta, np.abs(V[state] - best_action_value))

            # Update the value function for current state
            V[state] = None

        iteration += 1
        # Check if we can stop
        if delta < theta:
            print(f'Value-iteration converged at iteration #{iteration}.')
            break

    # Create a deterministic policy using the optimal value function
    policy = np.zeros([environment.nS, environment.nA])

    for state in range(environment.nS):

        # One step lookahead to find the best action for this state
        action_values = None

        # Select best action based on the highest state-action value
        best_action = None

        # Update the policy to perform a better action at a current state
        policy[state, best_action] = None

    return policy, V
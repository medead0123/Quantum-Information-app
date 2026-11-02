import math

def simulate_grover(n_qubits, max_iterations=10):
    """
    Simulates Grover's algorithm success probability over iterations.
    
    Args:
        n_qubits: Number of qubits
        max_iterations: Maximum number of iterations
    
    Returns:
        (iterations_list, probabilities_list)
    """
    N = 2 ** n_qubits
    theta = math.asin(1 / math.sqrt(N))
    iters = list(range(max_iterations + 1))
    probs = [math.sin((2*r + 1) * theta) ** 2 for r in iters]
    return iters, probs

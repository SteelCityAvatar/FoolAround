from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Dictionary with full explanations and LaTeX-style formulas
formulas = {
    "Bernoulli Variance": {
            "formula": r"\text{Var}(X) = p(1 - p)",
            "explanation": """
            A Bernoulli random variable \( X \) takes values 0 or 1, with probability \( p \) of being 1. 
            - Expected value of \( X \): \( E[X] = p \)
            - Variance: \( \text{Var}(X) = E[(X - E[X])^2] = p(1 - p) \)
        The variance is highest when \( p = \dfrac{1}{2} \), and it is 0 when \( p = 0 \) or \( p = 1 \).
    """
    },

    "Uniform Variance": {
        "formula": r"\text{Var}(X) = \frac{n(n + 2)}{12}",
        "explanation": """
            The variance of a uniform random variable \( X \) that takes equally likely values from 0 to \( n \):
            - Mean: \( E[X] = \dfrac{n}{2} \)
            - Variance: \( \text{Var}(X) = \dfrac{n(n + 2)}{12} \)
            
            This measures the spread of values in a uniform distribution.
        """
    },
    "General Uniform Variance": {
    "formula": r"\text{Var}(X) = \dfrac{(b - a)(b - a + 2)}{12}",
    "explanation": """
        For a uniform random variable \( X \) over a general range \([a, b]\), the variance is:

        - \( \text{Var}(X) = \dfrac{(b - a)(b - a + 2)}{12} \)

        This generalizes the variance formula for uniformly distributed values over any range.
    """
    },
    "Geometric Distribution PMF": {
        "formula": r"P(X = k) = (1 - p)^{k-1} p",
        "explanation": """
            The probability mass function (PMF) of a geometric random variable \( X \), 
            which represents the number of independent coin tosses until the first heads occurs:
            
            - \( p \) is the probability of getting heads on any given toss.
            - \( (1 - p) \) is the probability of getting tails.
            - The term \( (1 - p)^{k-1} \) accounts for getting tails on the first \( k-1 \) tosses.
            
            This formula gives the probability that you need exactly \( k \) tosses to get the first heads.
        """
    },
    "Memorylessness Property": {
        "formula": r"P(X = k + n \mid X > n) = P(X = k)",
        "explanation": """
            The memorylessness property of the geometric distribution states that the remaining number of tosses,
            after a certain number of tails, still follows the same geometric distribution as the original tosses.
            
            - \( X \) is the number of tosses until the first heads.
            - \( n \) is the number of past tosses that resulted in tails.
            - The probability that we need \( k \) more tosses given that \( n \) tosses resulted in tails is the same as the original probability.

            Formally, the conditional probability is the same as the unconditional probability:
            \[
            P(X = k + n \mid X > n) = P(X = k)
            \]
        """
    },
    "Expected Value of Geometric Distribution": {
        "formula": r"E[X] = \frac{1}{p}",
        "explanation": """
            The expected value (mean) of a geometric random variable \( X \), representing the number of tosses until the first heads, is:
            \[
            E[X] = \frac{1}{p}
            \]
            Where \( p \) is the probability of heads on each toss.

            This result makes intuitive sense: if \( p \) is small (i.e., heads is unlikely), we expect to wait longer on average to get the first heads.
        """
    },
    "Total Expectation Theorem for Geometric Distribution": {
        "formula": r"E[X] = p \cdot 1 + (1 - p) \cdot (E[X - 1] + 1)",
        "explanation": """
            The expected value of a geometric distribution can be derived using the total expectation theorem.
            We break down the expected value into two scenarios:
            
            1. First toss is heads: \( X = 1 \).
               - This happens with probability \( p \), so the contribution is \( p \cdot 1 \).
            2. First toss is tails: \( X > 1 \), and the expected number of additional tosses is \( E[X - 1] \).
               - This happens with probability \( 1 - p \), so the contribution is \( (1 - p) \cdot (E[X - 1] + 1) \).

            Solving this equation gives the result \( E[X] = \frac{1}{p} \).
        """
    }
}

@app.route('/')
def index():
    return render_template('index.html', formulas=formulas)

@app.route('/explanation/<formula_name>')
def explanation(formula_name):
    explanation = formulas.get(formula_name, {}).get('explanation', 'Explanation not available.')
    return jsonify({'explanation': explanation})

if __name__ == '__main__':
    app.run(debug=True)

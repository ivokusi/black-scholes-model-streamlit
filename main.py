from scipy.stats import norm
import numpy as np

class BlackScholes:

    """
    The formulas used in this class are dervied from https://www.macroption.com/black-scholes-formula/
    """


    @staticmethod
    def call_price(S: float, K: float, sigma: float, r: float, t: float, q: float=0.0):

        """
        Calculate the theoretical call price of the European style option

        S: Underlying price (31.55 represents $31.55)
        K: Strike price (22.75 represents $22.75)
        sigma: volatility (0.50 represents 50%)
        r: continuously compounded risk-free interest rate (0.05 represents 5%)
        t: time to expiration (3.5 represents 3.5yrs)
        q: continuously compounded dividend yield (0.05 represents 5%) (optional: 0.0)
        """

        d1 = (np.log(S / K) + t * (r - q + (sigma * sigma) / 2)) / (sigma * np.sqrt(t))
        d2 = d1 - sigma * np.sqrt(t)

        C = S * np.exp(-(q * t)) * norm.cdf(d1) - K * np.exp(-(r * t)) * norm.cdf(d2)
        
        return f"${C:.2f}"
    
    @staticmethod
    def put_price(S: float, K: float, sigma: float, r: float, t: float, q: float=0.0):

        """
        Calculate the theoretical put price of the European style option

        S: Underlying price
        K: Strike price
        sigma: volatility
        r: continuously compounded risk-free interest rate
        t: time to expiration
        q: continuously compounded dividend yield (optional: 1.0)
        """

        d1 = (np.log(S / K) + t * (r - q + (sigma * sigma) / 2)) / (sigma * np.sqrt(t))
        d2 = d1 - sigma * np.sqrt(t)

        P = K * np.exp(-(r * t)) * norm.cdf(-d2) - S * np.exp(-(q * t)) * norm.cdf(-d1)
        
        return f"${P:.2f}"
    
print(BlackScholes.call_price(31.55, 22.75, 0.5, 0.05, 3.5, 0.05))
print(BlackScholes.put_price(31.55, 22.75, 0.5, 0.05, 3.5, 0.05))
import math

def solve_quadratic(a, b, c):
    # Step 1: Calculate the discriminant
    discriminant = b**2 - 4*a*c
    print(f"Step 1: Calculate the discriminant (b^2 - 4ac)")
    print(f"Discriminant = {b}^2 - 4 * {a} * {c} = {discriminant}")
    
    # Step 2: Check if the discriminant is positive, zero, or negative
    if discriminant > 0:
        print("\nStep 2: The discriminant is positive, so there are two real roots.")
    elif discriminant == 0:
        print("\nStep 2: The discriminant is zero, so there is one real root.")
    else:
        print("\nStep 2: The discriminant is negative, so there are no real roots.")
    
    # Step 3: Calculate the two roots if discriminant is positive or zero
    if discriminant >= 0:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        
        print("\nStep 3: Calculate the roots using the quadratic formula:")
        print(f"Root 1 = (-{b} + sqrt({discriminant})) / (2 * {a}) = {root1}")
        print(f"Root 2 = (-{b} - sqrt({discriminant})) / (2 * {a}) = {root2}")
    else:
        print("\nThere are no real roots.")

# Example usage
a = 1
b = -3
c = 2

solve_quadratic(a, b, c)

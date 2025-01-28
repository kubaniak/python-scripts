function_calls = 0

def memo_fib(n, memo=None):
    function_calls += 1
    
    if memo == None:
        memo = [None] * (n + 1)
    
    if memo[n] is not None:
        return memo[n]
    
    if n == 1:
        memo[n] = 1
        return 1
    
    if n == 0:
        memo[n] = 0
        return 0
    


    memo[n] = memo_fib(n-1, memo) + memo_fib(n-2, memo)
    return memo[n]


print(memo_fib(50))
print("Function calls: ", function_calls)




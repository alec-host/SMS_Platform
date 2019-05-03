def count_change(amount, coins):
    change_combination = [0] * (amount + 1)
    change_combination[0] = 1
    for coin in coins:
        for j in xrange(coin, amount + 1):
            change_combination[j] += change_combination[j - coin]
    return change_combination[amount]
 
print count_change(10,[5,2,3]);
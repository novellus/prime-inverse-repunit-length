from matplotlib import pyplot as plt
import bisect
import math
import matplotlib
import re
import sys
import labmath

f = open('first_1million_prime_numbers.txt')
text = f.read()
f.close()
texts = re.split('\s+', text)
prime_numbers = [int(x) for x in texts if x]

num_points = 10000
if len(sys.argv) > 1:
    num_points = int(sys.argv[1])
# exclude indeces 0 and 2, corresponding to entries 2 and 5
# These are the only 2 primes which do not divide a repunit-9 integer in base 10
prime_numbers = prime_numbers[1:2] + prime_numbers[3 : 3-1 + num_points]


@profile
def smallest_repunit_factor_v3(prime_num, factor):
    for subfactor in labmath.divisors(factor):
        if subfactor != factor:
            mod = pow(10, subfactor, prime_num)
            if mod == 1:
                return smallest_repunit_factor_v3(prime_num, subfactor)
    return factor  # no subfactors were repunits, so factor must be the smallest repunit


@profile
def find_lowest_repunit_9_product_v8(prime_num):
    # check only repunit lengths which are factors of (prime_num-1) - this is guaranteed to capture smallest repunit judging by the first 1000 primes
    #   to confirm, reason is outlined on wikipedia: https://en.wikipedia.org/wiki/Repeating_decimal#Fractions_with_prime_denominators
    # Ideally check the biggest factor first, and when a factor is identified as a repunit, redefine scope of search to only factors (subharmonics) of that factor
    #   Largest repunit length has the highest hit rate, then progress down in the roughly negative hit rate order
    return smallest_repunit_factor_v3(prime_num, prime_num - 1)


@profile
def calculate_closest_ratio_limit(actual_ratio):
    # all ratios approach 1/integer for positive integers up to max_prime_number, via visual observation of distribution over 10000 numbers
    index = bisect.bisect_left(possible_ratio_limits, actual_ratio)
    if index == 0:
        return possible_ratio_limits[0]
    if index == len(possible_ratio_limits):
        return possible_ratio_limits[-1]
    smaller_num = possible_ratio_limits[index - 1]
    larger_num = possible_ratio_limits[index]
    if larger_num - actual_ratio < actual_ratio - smaller_num:
       return larger_num, index
    else:
       return smaller_num, index - 1

# precompute all possible ratio limits
# smallest achievable ratio is limited by inverse of maximum prime number
min_prime_number = prime_numbers[0]
max_prime_number = prime_numbers[-1]
possible_ratio_limits = sorted([1.0 / divisor for divisor in range(1, max_prime_number + 1)])


# prepare persistent data bins
lowest_repunit_9_products = []
ratios = []
ratio_limits = []
ratio_limit_counters = [0 for _ in possible_ratio_limits]

# kernprof -l 99999_analysis_4_profile.py ; python -m line_profiler 99999_analysis_4_profile.py.lprof > tmp
@profile
def main():
    # calculate lowest repunit 9 product
    global lowest_repunit_9_products
    for prime_num in prime_numbers:
        lowest_repunit_9_products.append(find_lowest_repunit_9_product_v8(prime_num))
        # assert find_lowest_repunit_9_product_v7(prime_num) == find_lowest_repunit_9_product_v8(prime_num), ('--Z--', prime_num, find_lowest_repunit_9_product_v7(prime_num), find_lowest_repunit_9_product_v8(prime_num))

    # calculate repunit-length ratio to prime number
    global ratios
    for i, prime_num in enumerate(prime_numbers):
        ratios.append(lowest_repunit_9_products[i] / float(prime_num))

    # calculate ratio limit, and count number of times each limit is achieved
    global ratio_limits
    global ratio_limit_counters
    for ratio in ratios:
        ratio_limit, limit_index = calculate_closest_ratio_limit(ratio)
        ratio_limits.append(ratio_limit)
        ratio_limit_counters[limit_index] += 1

    # # developmental tests
    # for i, prime_num in enumerate(prime_numbers):
    #     # check whether the achieved ratio is always below the limit - False
    #     # assert ratios[i] <= ratio_limits[i], ('--A--', prime_num, ratios[i], ratio_limits[i])
    #
    #     # check whether the achieved ratio is always as close as possible to ratio-limit within set of realizable ratios - True
    #     distance_ratio_limit = abs(lowest_repunit_9_products[i] / float(prime_num) - ratio_limits[i])
    #     distance_ratio_limit_next_bigger = abs((lowest_repunit_9_products[i] + 1) / float(prime_num) - ratio_limits[i])
    #     distance_ratio_limit_next_smaller = abs((lowest_repunit_9_products[i] - 1) / float(prime_num) - ratio_limits[i])
    #     assert (distance_ratio_limit < distance_ratio_limit_next_bigger) or (math.isclose(distance_ratio_limit, distance_ratio_limit_next_bigger)) or (lowest_repunit_9_products[i] + 1 == prime_num), ('--B--', prime_num, lowest_repunit_9_products[i], ratio_limits[i])
    #     assert (distance_ratio_limit < distance_ratio_limit_next_smaller) or (math.isclose(distance_ratio_limit, distance_ratio_limit_next_smaller)) or (lowest_repunit_9_products[i] == 1), ('--C--', prime_num, lowest_repunit_9_products[i], ratio_limits[i])
    #
    #     # check whether, when equal distance to limit occurs for 2 acievable ratios, the lower achievable ratio is always the lowest_repunit_9_product - True
    #     assert not math.isclose(distance_ratio_limit, distance_ratio_limit_next_smaller), ('--D--', prime_num, lowest_repunit_9_products[i], ratio_limits[i])
    #
    #     # check whether repunit length is always an integer factor of (prime_num-1) - True
    #     assert (lowest_repunit_9_products[i] == prime_num - 1) or (lowest_repunit_9_products[i] in smaller_factors(prime_num - 1))


@profile
def plot():
    # separated for profiling

    plt.figure()
    plt.title('Repunit Length\nFirst ' + str(num_points) + ' Prime Numbers, excluding 2 and 5')
    plt.xlabel('prime numbers')
    plt.ylabel('lowest repunit-9 product')
    plt.scatter(prime_numbers, lowest_repunit_9_products, s=2, marker='x')

    plt.figure()
    plt.title('Repunit Length Ratio of Prime Num\nFirst ' + str(num_points) + ' Prime Numbers, excluding 2 and 5')
    plt.xlabel('prime numbers')
    plt.ylabel('ratio to prime number')
    plt.scatter(prime_numbers, ratios, s=2, marker='x')


    # # developmental
    # # more verbose version
    # plt.figure()
    # plt.title('Verbose: Repunit Length Ratio of Prime Num\nFirst ' + str(num_points) + ' Prime Numbers, excluding 2 and 5')
    # plt.xlabel('prime numbers')
    # plt.ylabel('ratio to prime number')
    # # plot possible limits as lines across whole graph
    # for i_limit, limit in enumerate(possible_ratio_limits):
    #     label = 'possible inverse int limits' if i_limit == 0 else None
    #     plt.plot([min_prime_number, max_prime_number], [limit, limit], c='green', marker=None, label=label)
    # # plot actual limit approached for each prime
    # line_half_width = 0.25
    # for i_prime_num, prime_num in enumerate(prime_numbers):
    #     label = 'actual inverse int limit' if i_prime_num == 0 else None
    #     limit = ratio_limits[i_prime_num]
    #     plt.plot([prime_num - line_half_width, prime_num + line_half_width], [limit, limit], c='red', marker=None, label=label)
    # # plot realizable ratios for each prime
    # for i_prime_num, prime_num in enumerate(prime_numbers):
    #     label = 'realizable ratios' if i_prime_num == 0 else None
    #     realizable_ratios = [x/float(prime_num) for x in list(range(1, prime_num))]
    #     plt.scatter([prime_num]*len(realizable_ratios), realizable_ratios, c='blue', marker='x', s=2, label=label)
    # # plot actual ratio
    # plt.scatter(prime_numbers, ratios, c='red', marker='x', s=50, label='actual inverse int limit')
    # plt.legend(loc=1)


    plt.figure()
    plt.title('Repunit-Length Ratio-Limit Distribution\nFirst ' + str(num_points) + ' Prime Numbers, excluding 2 and 5')
    plt.xlabel('possible_ratio_limits')
    plt.ylabel('ratio limit count')
    plt.plot(possible_ratio_limits, ratio_limit_counters, markersize=5, marker='x')

    plt.show()

main()
# plot()
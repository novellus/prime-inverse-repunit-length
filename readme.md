# Premise
* prime number inverses (1/p) result in repeating decimals for all prime numbers other than 2 and 5 in base 10
* these repeating decimals have repeating sequence lengths <= (prime_num - 1)
* an individual length is not immediately obvious from inspection of the prime or the sequence of primes
* the length of the prime number inverse repeating sequence is exactly equal to the minimum repdigit-9 number divided by the prime
  * This is obvious from the ureduced form of any repeating decimal: (repend / (sum from i=0 to i=n-1 [9*10^i]) * 10^k + c)
  * where repend is an integer and the value of the repeating terminus; n is the number of digits of repend in base 10; and k (integer) and c (terminating decimal) are chosen to set the non-repeating beginning of the decimal number (if any)
* this program uses that equivilence to calculate the length of the repeating decimal sequences of prime inverses, by directly calculating the minimum repdigit-9 number divided by that prime

# Findings
### Figure 1
* plots sequence length vs prime number value
* The point-to-point distribution of repeating sequence lengths for prime number inverses is shown to be non-trivial, with no obvious predictive pattern for individual points
* The values do however form several obvious lines

### Figure 2
* transforms Figure 1 sequence lengths as a ratio to prime number, in order to separate the lines into distinct strata
* This shows that all sequence lengths are near to a discrete set of ratios to their prime, (1/k) for positive integers k
  * all values for k are apparently represented by utilizing large enough prime numbers
* and that ratios approach these ratio-limits more closely as prime number increases (discrete fractions of larger primes are higher density in the reals (0-1))

### Figure 3
* transforms Figure 2 ratios into bins counting which ratio-limit each point is near
* even for large number of primes processed, the distribution does not appear to approach smoothness
  * the distribution generally decreases as the limit decreases, but with an alternating peakiness
* the right-most number, represented as a fraction of total primes counted, approaches Artin's Constant, approx 0.3739558..., or about 37.39558% of all primes

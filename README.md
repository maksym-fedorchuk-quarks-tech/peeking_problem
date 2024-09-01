# peeking_problem

Here we going to do experiment for the Peeking Problem explanation

A brief definition of the Peeking Problem is that it arises when there is 
constant "peeking" at the test results before they reach statistical 
significance or the planned and predetermined duration of the test. As a result,
this can lead to incorrect data interpretation.

Most of analytics do split tests (or are present during the process - it's how 
lucky they are), and generally, they know that a standard test (like the 
Student's t-test) doesn't answer the question, "Is the new payment screen better?" 
but rather answers, "What is the probability that the differences between our 
test and control groups are due to chance?". And if an analyst has agreed with a
manager that the test will be accepted at a 95% significance level (meaning that
they choose a 5% probability that the result is not random), the practice of 
peeking allows for the "accidental" acceptance of a test (which shouldn't have 
been accepted) with a much higher probability 🙂. The materials I've come across 
online suggest that, based on their experiments, this percentage can reach up
to 20%. And this potentially means that every 5th rejected split-test rejected 
with no good reason 😣...

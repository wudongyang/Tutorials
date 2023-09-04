
// Checks that a voter's "registered" mark is changed correctly -
// if it's false after a function call, it was false before
// if it's true after a function call it either started as true or changed from false to true via registerVoter()
rule registeredCannotChangeOnceSet(method f, address voter) {
	env e;
	calldataarg args;
	uint256 age;
	bool voterRegBefore;
	bool voted;
	uint256 vote_attempts;
	bool black_listed;
	age, voterRegBefore, voted, vote_attempts, black_listed = getFullVoterDetails(e, voter);
	f(e, args);
	bool voterRegAfter;
	age, voterRegAfter, voted, vote_attempts, black_listed = getFullVoterDetails(e, voter);
	
	assert(voterRegAfter != voterRegBefore =>
		(!voterRegBefore && voterRegAfter && f.selector == sig:registerVoter(uint8).selector),
		"voter was registered from an unregistered state, by other function than registerVoter()");
}


/* Explanation on f.selector

 * On the right side of the implication above we see a f.selector.
 * The use of f.selector is very similar to its use in solidity -
 * since f is a parametric method that calls every function in contract in parallel,
 * we specify (or selecting) to address one particular path - when the f.selector was a specific function.
 */


// Checks that a each voted contender's points received the correct amount of points
rule correctPointsIncreaseToContenders(address first, address second, address third) {
	env e;
	mathint firstPointsBefore = getPointsOfContender(e, first);
	mathint secondPointsBefore = getPointsOfContender(e, second);
	mathint thirdPointsBefore = getPointsOfContender(e, third);
	
	vote(e, first, second, third);
	
	assert(getPointsOfContender(e, first) - firstPointsBefore == 3, "first choice received other amount than 3 points");
	assert(getPointsOfContender(e, second) - secondPointsBefore == 2, "second choice received other amount than 2 points");
	assert(getPointsOfContender(e, third) - thirdPointsBefore == 1, "third choice received other amount than 1 points");
	
}

// Checks that a black listed voter can not get unlisted
rule onceBlackListedNotOut(method f, address voter) {
	env e;
	calldataarg args;
	uint256 age;
	bool registeredBefore;
	bool voted;
	uint256 vote_attempts;
	bool black_listed_Before;
	age, registeredBefore, voted, vote_attempts, black_listed_Before = getFullVoterDetails(e, voter);
	f(e, args);
	bool registeredAfter;
	bool black_listed_After;
	age, registeredAfter, voted, vote_attempts, black_listed_After = getFullVoterDetails(e, voter);
	
	assert(registeredBefore && black_listed_Before) => black_listed_After, "the specified user got out of the black list";
}

// Checks that a contender's point count is non-decreasing
rule contendersPointsNonDecreasing(method f, address contender) {
	env e;
	calldataarg args;
	uint8 age;
	bool registeredBefore;
	uint256 pointsBefore;
	age, registeredBefore, pointsBefore = getFullContenderDetails(e, contender);
	require pointsBefore > 0 => registeredBefore;
	// why is this needed? try to omit this line and see what happens (registering sets points to 0, positive to 0 is a decrease)
	f(e, args);
	bool registeredAfter;
	uint256 pointsAfter;
	age, registeredAfter, pointsAfter = getFullContenderDetails(e, contender);
	
	assert(pointsAfter >= pointsBefore);
}
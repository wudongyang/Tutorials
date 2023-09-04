
/*
   This is a specification file for EnglishAuction's formal verification
   using the Certora prover.
 */
 



/*
    Declaration of methods that are used in the rules. envfree indicate that
    the method is not dependent on the environment (msg.value, msg.sender).
    Methods that are not declared here are assumed to be dependent on env.
*/


methods {
    // auction getters 
    function seller() external returns (address)                                              envfree;
    function nftId() external returns (uint)                                                  envfree;
    function nft() external returns(address)                                                  envfree;
    function endAt() external returns (uint256)                                               envfree;
    function started() external returns (bool)                                                envfree;
    function ended() external returns (bool)                                                  envfree;
    function highestBidder() external returns (address)                                       envfree;
    function highestBid() external returns (uint256)                                          envfree;
    function bids(address) external returns (uint256)                                         envfree;
    function operators(address, address) external returns (bool)                              envfree;


}



// check highestBidder correlation with highestBid from bids mapping
invariant highestBidVSBids() 
    bids( highestBidder()) == highestBid();




// Nobody can have more bids than highestBid
invariant integrityOfHighestBid(address any) 
    bids(any) <= highestBid();

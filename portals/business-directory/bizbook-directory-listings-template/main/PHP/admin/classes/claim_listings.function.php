<?php

//Get All Claim Listings
function getAllClaimListings()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "claim_listings ORDER BY claim_listing_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}



//Get All Claim request with given Listing Id
function getListingClaimListings($arg)
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "claim_listings where listing_id='" . $arg . "'  ORDER BY claim_listing_id DESC";
    $rs = mysqli_query($conn, $sql);
    return $rs;

}

//Get All Claim Listings Count
function getCountClaimListings()
{
    global $conn;

    $sql = "SELECT * FROM  " . TBL . "claim_listings ";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_num_rows($rs);
    return $row;

}




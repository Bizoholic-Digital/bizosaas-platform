<?php
if ($current_page == "company-profile.php" || $current_page == "profile.php" || $current_page == "event-details.php"
    || $current_page == "blog-details.php" || $current_page == "product-details.php" || $current_page == "listing-details.php"
    || $current_page == "all-listing.php" || $current_page == "filter_listing.php"
    || $current_page == "all-products.php" || $current_page == "filter_product.php"
    || $current_page == "listing-map-view.php" || $current_page == "target-listing.php"
    || $current_page == "ebook.php" || $current_page == "template-default.php"
    || $current_page == "job-details.php" || $current_page == "all-jobs.php" || $current_page == "filter_job.php"
    || $current_page == "job-profile.php" || $current_job_page == "jobs/index.php" || $current_page == "db-jobs.php"
    || $current_page == "db-jobs-applicant-profile.php" || $current_page == "create-job.php" || $current_page == "create-job-seeker-profile.php"
    || $current_page == "delete-job.php" || $current_page == "edit-job.php" || $current_page == "db-user-applied-jobs.php"
    || $current_page == "create-service-expert-profile.php" || $current_page == "service-confirmation.php"
    || $current_page == "db-service-expert.php" || $current_expert_page == "service-experts/index.php"
    || $current_page == "all-service-experts.php" || $current_page == "service-experts-profile.php"
    || $current_page == "db-my-service-bookings.php" || $current_news_page == "news/index.php"
    || $current_page == "news-all.php" || $current_page == "news-details.php"
    || $current_place_page == "places/index.php" || $current_page == "place-details.php"
) {
    $slash = $webpage_full_link;
} else {
    $slash = '';
}

if ($current_page == "listing-details.php") {

    if ($_GET['code'] == NULL && empty($_GET['code'])) {

        header("Location: all-listing");
    }
    $listing_codea1 = str_replace('-', ' ', $_GET['code']);
    $listing_codea = str_replace('.php', '', $listing_codea1);

    $listrow = getSlugListing($listing_codea); //To Fetch the listing

}

if ($current_page == "event-details.php") {


    if ($_GET['row'] == NULL && empty($_GET['row'])) {

        header("Location: events");
    }

    $event_codea1 = str_replace('-', ' ', $_GET['row']);
    $event_codea = str_replace('.php', '', $event_codea1);

    $events_a_row = getSlugEvent($event_codea); //To Fetch the Events

}

if ($current_page == "blog-details.php") {

    if ($_GET['row'] == NULL && empty($_GET['row'])) {

        header("Location: blog-posts");
    }

    $blog_codea1 = str_replace('-', ' ', $_GET['row']);
    $blog_codea = str_replace('.php', '', $blog_codea1);
    $blogs_a_row = getSlugBlog($blog_codea); //To Fetch the Blogs

}

if ($current_page == "product-details.php") {

    if ($_GET['code'] == NULL && empty($_GET['code'])) {

        header("Location: all-products");
    }

    $product_codea1 = str_replace('-', ' ', $_GET['code']);
    $product_codea = str_replace('.php', '', $product_codea1);
    $productrow = getSlugProduct($product_codea); //To Fetch the product

}

if ($current_page == "profile.php") {

    if ($_GET['code'] == NULL && empty($_GET['code'])) {

        header("Location: dashboard");
    }

    $user_user_codea1 = str_replace('-', ' ', $_GET['code']);
    $user_user_codea = str_replace('.php', '', $user_user_codea1);

    $user_usersqlrow = getActiveUser($user_user_codea); // To Fetch particular User Data

}

if ($current_page == "company-profile.php") {

    if ($_GET['code'] == NULL && empty($_GET['code'])) {

        header("Location: dashboard");
    }

    $user_codea1 = str_replace('-', ' ', $_GET['code']);
    $user_codea = str_replace('.php', '', $user_codea1);

    $company_row = getActiveUserCompany($user_codea); // To Fetch Company Details Data

}
if ($current_page == "target-listing.php") {

    if ($_GET['code'] == NULL && empty($_GET['code'])) {

        header("Location: dashboard");
    }

    $page_codea1 = str_replace('-', ' ', $_GET['code']);
    $page_codea = str_replace('.php', '', $page_codea1);

    $page_row = getActivePageSlugwithoutStatus(1, $page_codea); // To Fetch particular Target Listing Data

}
if ($current_page == "ebook.php") {

    if ($_GET['code'] == NULL && empty($_GET['code'])) {

        header("Location: dashboard");
    }

    $page_codea1 = str_replace('-', ' ', $_GET['code']);
    $page_codea = str_replace('.php', '', $page_codea1);

    $page_row = getActivePageSlug(3, $page_codea); // To Fetch particular Ebook Data

}
if ($current_page == "template-default.php") {

    if ($_GET['code'] == NULL && empty($_GET['code'])) {

        header("Location: dashboard");
    }

    $page_codea1 = str_replace('-', ' ', $_GET['code']);
    $page_codea = str_replace('.php', '', $page_codea1);

    $page_row = getActivePageSlug(2, $page_codea); // To Fetch particular General Promotion Data

}
if ($current_page == "all-listing.php") {

    if (isset($_GET['category'])) {

        $category_search_slug1 = str_replace('-', ' ', $_GET['category']);
        $category_search_slug = str_replace('.php', '', $category_search_slug1);

        $cat_search_row = getSlugCategory($category_search_slug);  //Fetch Category Id using category name
    }

}

if ($current_page == "all-jobs.php") {

    if (isset($_GET['category'])) {

        $category_search_slug1 = str_replace('-', ' ', $_GET['category']);
        $category_search_slug = str_replace('.php', '', $category_search_slug1);

        $cat_search_row = getSlugJobCategory($category_search_slug);  //Fetch Category Id using job category name
    }

}

if ($current_page == "job-details.php") {

    if ($_GET['code'] == NULL && empty($_GET['code'])) {

        header("Location: all-jobs");
    }
    $job_codea1 = str_replace('-', ' ', $_GET['code']);
    $job_codea = str_replace('.php', '', $job_codea1);

    $jobrow = getSlugJob($job_codea); //To Fetch the Job

}

if ($current_page == "job-profile.php") {

    if ($_GET['code'] == NULL && empty($_GET['code'])) {

        header("Location: all-jobs");
    }

    $job_profile_codea1 = str_replace('-', ' ', $_GET['code']);

    $job_profile_codea = str_replace('.php', '', $job_profile_codea1);

    $job_profile_row = getJobProfileSlug($job_profile_codea); // To Fetch particular User Data

    $job_profile_sub_category_id = $job_profile_row['sub_category_id'];

    $job_profile_sub_category_row = getJobSubCategory($job_profile_sub_category_id);

    $job_sub_category_name = $job_profile_sub_category_row['sub_category_name'];

}

if ($current_page == "service-experts-profile.php") {

    if ($_GET['code'] == NULL && empty($_GET['code'])) {

        header("Location: all-service-experts");
    }

    //$expert_profile_codea = $_GET['code'];
    $expert_profile_codea1 = str_replace('-', ' ', $_GET['code']);
    $expert_profile_codea = str_replace('.php', '', $expert_profile_codea1);

    $expertprofilerow = getSlugExpert($expert_profile_codea); // To Fetch particular Expert Data

    $expert_profile_category_id = $expertprofilerow['category_id'];

    $expert_profile_city_id = $expertprofilerow['city_id'];

    $expert_profile_category_row = getExpertCategory($expert_profile_category_id);

    $expert_category_name = $expert_profile_category_row['category_name'];

    $expert_profile_city_row = getExpertCity($expert_profile_city_id);

    $expert_city_name = $expert_profile_city_row['country_name'];

    $sub_category_namestr = array();

    $sub_category = explode(',', $expertprofilerow['sub_category_id']);

    foreach ($sub_category as $sub_category_id) {
        $sub_category_name = getExpertSubCategory($sub_category_id);
        $sub_category_namestr[] = $sub_category_name['sub_category_name'];
    }

    $subbbb_cat_nameee = implode(", ", $sub_category_namestr);

}

if ($current_page == "news-all.php") {

    $category_search_slug1 = str_replace('-', ' ', $_GET['category']);

    $category_search_slug = str_replace('.php', '', $category_search_slug1);

    $cat_search_row = getSlugNewsCategory($category_search_slug);  //Fetch Category Id using category name

}

if ($current_page == "news-details.php") {

    if ($_GET['code'] == NULL && empty($_GET['code'])) {

        header("Location: $redirect_url");  //Redirect When code parameter is empty
    }

    $news_codea1 = str_replace('-', ' ', $_GET['code']);
    $news_codea = str_replace('.php', '', $news_codea1);

    $news_row = getSlugNews($news_codea); // To Fetch particular News Data

    if ($news_row['news_id'] == NULL && empty($news_row['news_id'])) {


        header("Location: $redirect_url");  //Redirect When No User Found in Table
    }

    $news_id = $news_row['news_id'];

    $news_category_id = $news_row['category_id'];

    $news_category_row = getNewsCategory($news_category_id);

    $news_category_name = $news_category_row['category_name'];

}

if ($current_page == "place-details.php") {

    if ($_GET['code'] == NULL && empty($_GET['code'])) {

        header("Location: $redirect_url");  //Redirect When code parameter is empty
    }

//$place_codea = $_GET['code'];
    $place_codea1 = str_replace('-', ' ', $_GET['code']);
    $place_codea = str_replace('.php', '', $place_codea1);

    $place_row = getSlugPlaces($place_codea); // To Fetch particular place Data

    if ($place_row['place_id'] == NULL && empty($place_row['place_id'])) {

        header("Location: $redirect_url");  //Redirect When No User Found in Table
    }

    $place_id = $place_row['place_id'];

    $place_category_id = $place_row['category_id'];

    $place_category_row = getPlaceCategory($place_category_id);

    $place_category_name = $place_category_row['category_name'];
}

?>

<title>
    <?php
    if ($current_page == "listing-details.php") {
        if (!empty($listrow['seo_title']) || $listrow['seo_title'] != NULL) {
            echo $listrow['seo_title'];
        } else {
            echo $listrow['listing_name'];
        }
    } elseif ($current_page == "event-details.php") {

        if (!empty($events_a_row['seo_title']) || $events_a_row['seo_title'] != NULL) {
            echo $events_a_row['seo_title'];
        } else {
            echo $events_a_row['event_name'];
        }
    } elseif ($current_page == "blog-details.php") {

        if (!empty($blogs_a_row['seo_title']) || $blogs_a_row['seo_title'] != NULL) {
            echo $blogs_a_row['seo_title'];
        } else {
            echo $blogs_a_row['blog_name'];
        }
    } elseif ($current_page == "product-details.php") {
        if (!empty($productrow['seo_title']) || $productrow['seo_title'] != NULL) {
            echo $productrow['seo_title'];
        } else {
            echo $productrow['product_name'];
        }
    } elseif ($current_page == "profile.php") {

        echo $user_usersqlrow['first_name'] . ' - ' . $footer_row['website_address'];

    } elseif ($current_page == "company-profile.php") {

        echo $company_row['company_name'] . " | " . $footer_row['website_address'];

    } elseif ($current_page == $slash) {

        $seo_details_row = getSeo(1); //if Current Page is Home page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {

            echo $seo_details_row['seo_page_title'];

        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_page == "all-category.php") {

        $seo_details_row = getSeo(2); //if Current Page is All Service page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {
            echo $seo_details_row['seo_page_title'];
        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_page == "events.php") {

        $seo_details_row = getSeo(3); //if Current Page is All Events page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {
            echo $seo_details_row['seo_page_title'];
        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_page == "all-products.php") {

        $seo_details_row = getSeo(4); //if Current Page is All Products page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {
            echo $seo_details_row['seo_page_title'];
        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_page == "blog-posts.php") {

        $seo_details_row = getSeo(5); //if Current Page is All Blogs page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {
            echo $seo_details_row['seo_page_title'];
        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_job_page == "jobs/index.php") {

        $seo_details_row = getSeo(6); //if Current Page is Home page Jobs page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {
            echo $seo_details_row['seo_page_title'];
        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_page == "all-jobs.php") {

        $seo_details_row = getSeo(7); //if Current Page is All Jobs page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {
            echo $seo_details_row['seo_page_title'];
        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_page == "job-details.php") {
        if (!empty($jobrow['seo_title']) || $jobrow['seo_title'] != NULL) {
            echo $jobrow['seo_title'];
        } else {
            echo $jobrow['job_title'];
        }
    } elseif ($current_page == "job-profile.php") {

        echo $job_profile_row['profile_name'] . ' ' . $job_sub_category_name . " at " . $job_profile_row['current_company'] . " | " . $footer_row['website_address'];

    } elseif ($current_expert_page == "service-experts/index.php") {

        $seo_details_row = getSeo(8); //if Current Page is Home service expert page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {
            echo $seo_details_row['seo_page_title'];
        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_page == "all-service-experts.php") {

        $seo_details_row = getSeo(9); //if Current Page is All service expert page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {
            echo $seo_details_row['seo_page_title'];
        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_page == "service-experts-profile.php") {

        if (!empty($expertprofilerow['seo_title']) || $expertprofilerow['seo_title'] != NULL) {
            echo $expertprofilerow['seo_title'] . " - " . $expert_category_name . " Experts in " . $expert_city_name;
        } else {
            echo $expertprofilerow['profile_name'] . " - " . $expert_category_name . " Experts in " . $expert_city_name;
        }
    } elseif ($current_page == "news-all.php") {

        if (!empty($cat_search_row['category_seo_title']) || $cat_search_row['category_seo_title'] != NULL) {
            echo $cat_search_row['category_seo_title'];
        } else {
            echo $cat_search_row['category_name'];
        }
    } elseif ($current_page == "news-details.php") {

        if (!empty($news_row['seo_title']) || $news_row['seo_title'] != NULL) {
            echo $news_row['seo_title'];
        } else {
            echo stripslashes($news_row['news_title']);
        }
    } elseif ($current_page == "place-details.php") {

        if (!empty($place_row['seo_title']) || $place_row['seo_title'] != NULL) {
            echo $place_row['seo_title'];
        } else {
            echo stripslashes($place_row['news_title']);
        }
    } elseif ($current_page == "community.php") {

        $seo_details_row = getSeo(10); //if Current Page is Community page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {
            echo $seo_details_row['seo_page_title'];
        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_page == "pricing-details.php") {

        $seo_details_row = getSeo(11); //if Current Page is Pricing Plan page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {
            echo $seo_details_row['seo_page_title'];
        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_page == "login.php") {

        $seo_details_row = getSeo(12); //if Current Page is Login page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {
            echo $seo_details_row['seo_page_title'];
        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_page == "about.php") {

        $seo_details_row = getSeo(13); //if Current Page is About Us page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {
            echo $seo_details_row['seo_page_title'];
        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_page == "faq.php") {

        $seo_details_row = getSeo(14); //if Current Page is FAQ page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {
            echo $seo_details_row['seo_page_title'];
        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_page == "feedback.php") {

        $seo_details_row = getSeo(15); //if Current Page is Feedback page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {
            echo $seo_details_row['seo_page_title'];
        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_page == "contact-us.php") {

        $seo_details_row = getSeo(16); //if Current Page is Contact Us page

        if (!empty($seo_details_row['seo_page_title']) || $seo_details_row['seo_page_title'] != NULL) {
            echo $seo_details_row['seo_page_title'];
        } else {
            echo $footer_row['admin_seo_title'];
        }

    } elseif ($current_page == "all-listing.php") {

        if (isset($_GET['category'])) {
            if (!empty($cat_search_row['category_seo_title'])) {
                echo $cat_search_row['category_seo_title'];
            } else {
                echo $cat_search_row['category_name'];
            }
        }
    } elseif ($current_page == "target-listing.php") {

        echo $page_row['page_seo_title'];

    } elseif ($current_page == "ebook.php") {

        echo $page_row['page_seo_title'];

    } elseif ($current_page == "template-default.php") {

        echo $page_row['page_seo_title'];

    } else {
        echo $footer_row['admin_seo_title'];
    } ?>
</title>
<!--== META TAGS ==-->
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<meta name="theme-color" content="#76cef1"/>
<meta property="og:image" content="<?php
if ($current_page == "listing-details.php") {
    if ($listrow['profile_image'] != NULL || !empty($listrow['profile_image'])) {
        echo $slash . "images/listings/" . $listrow['profile_image'];
    } else {
        echo $slash . "images/listings/hot4.jpg";
    }
} elseif ($current_page == "event-details.php") {

    echo $slash . "images/events/" . $events_a_row['event_image'];

} elseif ($current_page == "blog-details.php") {

    echo $slash . "images/blogs/" . $blogs_a_row['blog_image'];

} elseif ($current_page == "product-details.php") {
    if ($productrow['gallery_image'] != NULL || !empty($productrow['gallery_image'])) {
        echo $slash . "images/products/" . array_shift(explode(',', $productrow['gallery_image']));
    } else {
        echo $slash . "images/listings/hot4.jpg";
    }

} elseif ($current_page == "all-listing.php") {
    if ($cat_search_row['category_image'] != NULL || !empty($cat_search_row['category_image'])) {
        echo $slash . "images/services/" . $cat_search_row['category_image'];
    } else {
        echo $slash . "images/home/" . $footer_row['header_logo'];
    }

} else {
    echo $slash . "images/home/" . $footer_row['header_logo'];
} ?>"/>
<meta name="description"
      content="<?php if (!empty($listrow['seo_description']) || $listrow['seo_description'] != NULL) {
          echo $listrow['seo_description'];
      } elseif (!empty($events_a_row['seo_description']) || $events_a_row['seo_description'] != NULL) {
          echo $events_a_row['seo_description'];
      } elseif (!empty($blogs_a_row['seo_description']) || $blogs_a_row['seo_description'] != NULL) {
          echo $blogs_a_row['seo_description'];
      } elseif (!empty($productrow['seo_description']) || $productrow['seo_description'] != NULL) {
          echo $productrow['seo_description'];
      } elseif (!empty($company_row['company_seo_description']) || $company_row['company_seo_description'] != NULL) {
          echo $company_row['company_seo_description'];
      } elseif ($current_page == $slash) {

          $seo_details_row = getSeo(1); //if Current Page is Home page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {

              echo $seo_details_row['seo_page_description'];

          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "all-category.php") {

          $seo_details_row = getSeo(2); //if Current Page is All Service page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {
              echo $seo_details_row['seo_page_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "events.php") {

          $seo_details_row = getSeo(3); //if Current Page is All Events page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {
              echo $seo_details_row['seo_page_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "all-products.php") {

          $seo_details_row = getSeo(4); //if Current Page is All Products page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {
              echo $seo_details_row['seo_page_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "blog-posts.php") {

          $seo_details_row = getSeo(5); //if Current Page is All Blogs page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {
              echo $seo_details_row['seo_page_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "profile.php") {

          echo $user_usersqlrow['first_name'] . ' is on ' . $footer_row['website_address'] . ". Join " . $footer_row['website_address'] . " to enjoy our online servers and make your professional community.";

      } elseif ($current_job_page == "jobs/index.php") {

          $seo_details_row = getSeo(6); //if Current Page is Homepage jobs page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {
              echo $seo_details_row['seo_page_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "all-jobs.php") {

          $seo_details_row = getSeo(7); //if Current Page is All jobs page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {
              echo $seo_details_row['seo_page_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "job-details.php") {

          if (!empty($jobrow['seo_description']) || $jobrow['seo_description'] != NULL) {
              echo $jobrow['seo_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "job-profile.php") {

              echo $job_profile_row['profile_name']." is on ". $footer_row['website_address'].". Join ".$footer_row['website_address']." to enjoy our online service and make your professional community.";


      }elseif ($current_page == "company-profile.php") {

          if (!empty($company_row['company_seo_description']) || $company_row['company_seo_description'] != NULL) {
              echo $company_row['company_seo_description'];
          } else {
              echo $company_row['company_name']." is on ". $footer_row['website_address'].". Join ".$footer_row['website_address']." to enjoy our online service and make your professional community.";
          }

      } elseif ($current_expert_page == "service-experts/index.php") {

          $seo_details_row = getSeo(8); //if Current Page is Home service experts page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {
              echo $seo_details_row['seo_page_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "all-service-experts.php") {

          $seo_details_row = getSeo(9); //if Current Page is All service experts page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {
              echo $seo_details_row['seo_page_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "service-experts-profile.php") {

          if (!empty($expertprofilerow['seo_description']) || $expertprofilerow['seo_description'] != NULL) {
              echo $expertprofilerow['seo_description'];
          } else {
              echo " Now easy to book your best " . $expert_category_name . " Experts in " . $expert_city_name . ". We are Specialist for " . $subbbb_cat_nameee;
          }

      } elseif ($current_page == "news-all.php") {

          if (!empty($cat_search_row['category_seo_description']) || $cat_search_row['category_seo_description'] != NULL) {
              echo $cat_search_row['category_seo_description'];
          } else {
              echo $cat_search_row['category_name'];
          }

      } elseif ($current_page == "news-details.php") {

          if (!empty($news_row['seo_description']) || $news_row['seo_description'] != NULL) {
              echo $news_row['seo_description'];
          } else {
              echo stripslashes($news_row['news_title']).' - '.$news_category_name;
          }

      } elseif ($current_page == "place-details.php") {

          if (!empty($place_row['seo_description']) || $place_row['seo_description'] != NULL) {
              echo $place_row['seo_description'];
          } else {
              echo stripslashes($place_row['news_title']).' - '.$news_category_name;
          }

      } elseif ($current_page == "community.php") {

          $seo_details_row = getSeo(10); //if Current Page is Community page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {
              echo $seo_details_row['seo_page_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "pricing-details.php") {

          $seo_details_row = getSeo(11); //if Current Page is Pricing Plan page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {
              echo $seo_details_row['seo_page_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "login.php") {

          $seo_details_row = getSeo(12); //if Current Page is Login page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {
              echo $seo_details_row['seo_page_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "about.php") {

          $seo_details_row = getSeo(13); //if Current Page is About Us page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {
              echo $seo_details_row['seo_page_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "faq.php") {

          $seo_details_row = getSeo(14); //if Current Page is FAQ page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {
              echo $seo_details_row['seo_page_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "feedback.php") {

          $seo_details_row = getSeo(15); //if Current Page is Feedback page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {
              echo $seo_details_row['seo_page_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "contact-us.php") {

          $seo_details_row = getSeo(16); //if Current Page is Contact Us page

          if (!empty($seo_details_row['seo_page_description']) || $seo_details_row['seo_page_description'] != NULL) {
              echo $seo_details_row['seo_page_description'];
          } else {
              echo $footer_row['admin_seo_description'];
          }

      } elseif ($current_page == "all-listing.php") {
          if (isset($_GET['category'])) {

              if (!empty($cat_search_row['category_seo_description'])) {
                  echo $cat_search_row['category_seo_description'];
              } else {
                  echo $cat_search_row['category_name'];
              }
          }
      } elseif ($current_page == "target-listing.php") {

          echo $page_row['page_seo_description'];

      } elseif ($current_page == "ebook.php") {

          echo $page_row['page_seo_description'];

      } elseif ($current_page == "template-default.php") {

          echo $page_row['page_seo_description'];

      } else {
          echo $footer_row['admin_seo_description'];
      } ?>">
<meta name="keyword"
      content="<?php if (!empty($listrow['seo_keywords']) || $listrow['seo_keywords'] != NULL) {
          echo $listrow['seo_keywords'];
      } elseif (!empty($events_a_row['seo_keywords']) || $events_a_row['seo_keywords'] != NULL) {
          echo $events_a_row['seo_keywords'];
      } elseif (!empty($blogs_a_row['seo_keywords']) || $blogs_a_row['seo_keywords'] != NULL) {
          echo $blogs_a_row['seo_keywords'];
      } elseif (!empty($productrow['seo_keywords']) || $productrow['seo_keywords'] != NULL) {
          echo $productrow['seo_keywords'];
      } elseif (!empty($company_row['company_seo_keywords']) || $company_row['company_seo_keywords'] != NULL) {
          echo $company_row['company_seo_keywords'];
      } elseif ($current_page == $slash) {

          $seo_details_row = getSeo(1); //if Current Page is Home page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {

              echo $seo_details_row['seo_page_keywords'];

          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "all-category.php") {

          $seo_details_row = getSeo(2); //if Current Page is All Service page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {
              echo $seo_details_row['seo_page_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "events.php") {

          $seo_details_row = getSeo(3); //if Current Page is All Events page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {
              echo $seo_details_row['seo_page_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "all-products.php") {

          $seo_details_row = getSeo(4); //if Current Page is All Products page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {
              echo $seo_details_row['seo_page_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "blog-posts.php") {

          $seo_details_row = getSeo(5); //if Current Page is All Blogs page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {
              echo $seo_details_row['seo_page_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_job_page == "jobs/index.php") {

          $seo_details_row = getSeo(6); //if Current Page is Home jobs page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {
              echo $seo_details_row['seo_page_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "all-jobs.php") {

          $seo_details_row = getSeo(7); //if Current Page is all jobs page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {
              echo $seo_details_row['seo_page_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "job-details.php") {

          if (!empty($jobrow['seo_keywords']) || $jobrow['seo_keywords'] != NULL) {
              echo $jobrow['seo_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_expert_page == "service-experts/index.php") {

          $seo_details_row = getSeo(8); //if Current Page is Home service expert page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {
              echo $seo_details_row['seo_page_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "all-service-experts.php") {

          $seo_details_row = getSeo(9); //if Current Page is All service expert page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {
              echo $seo_details_row['seo_page_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "service-experts-profile.php") {

          if (!empty($expertprofilerow['seo_keywords']) || $expertprofilerow['seo_keywords'] != NULL) {
              echo $expertprofilerow['seo_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "news-all.php") {

          if (!empty($cat_search_row['category_seo_keywords']) || $cat_search_row['category_seo_keywords'] != NULL) {
              echo $cat_search_row['category_seo_keywords'];
          } else {
              echo $cat_search_row['category_name'];
          }

      } elseif ($current_page == "news-details.php") {

          if (!empty($news_row['seo_keywords']) || $news_row['seo_keywords'] != NULL) {
              echo $news_row['seo_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "place-details.php") {

          if (!empty($place_row['seo_keywords']) || $place_row['seo_keywords'] != NULL) {
              echo $place_row['seo_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "community.php") {

          $seo_details_row = getSeo(10); //if Current Page is Community page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {
              echo $seo_details_row['seo_page_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "pricing-details.php") {

          $seo_details_row = getSeo(11); //if Current Page is Pricing Plan page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {
              echo $seo_details_row['seo_page_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "login.php") {

          $seo_details_row = getSeo(12); //if Current Page is Login page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {
              echo $seo_details_row['seo_page_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "about.php") {

          $seo_details_row = getSeo(13); //if Current Page is About Us page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {
              echo $seo_details_row['seo_page_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "faq.php") {

          $seo_details_row = getSeo(14); //if Current Page is FAQ page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {
              echo $seo_details_row['seo_page_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "feedback.php") {

          $seo_details_row = getSeo(15); //if Current Page is Feedback page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {
              echo $seo_details_row['seo_page_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "contact-us.php") {

          $seo_details_row = getSeo(16); //if Current Page is Contact Us page

          if (!empty($seo_details_row['seo_page_keywords']) || $seo_details_row['seo_page_keywords'] != NULL) {
              echo $seo_details_row['seo_page_keywords'];
          } else {
              echo $footer_row['admin_seo_keywords'];
          }

      } elseif ($current_page == "all-listing.php") {
          if (isset($_GET['category'])) {

              if (!empty($cat_search_row['category_seo_keywords'])) {
                  echo $cat_search_row['category_seo_keywords'];
              } else {
                  echo $cat_search_row['category_name'];
              }
          }
      } elseif ($current_page == "target-listing.php") {

          echo $page_row['page_seo_keyword'];

      } elseif ($current_page == "ebook.php") {

          echo $page_row['page_seo_keyword'];

      } elseif ($current_page == "template-default.php") {

          echo $page_row['page_seo_keyword'];

      } else {
          echo $footer_row['admin_seo_keywords'];
      } ?>">
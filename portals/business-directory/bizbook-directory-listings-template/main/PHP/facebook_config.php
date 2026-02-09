
<script>
    window.fbAsyncInit = function() {
        // FB JavaScript SDK configuration and setup
        FB.init({
            appId      : '<?php echo $footer_row['admin_facebook_app_id']; ?>', // FB App ID
            cookie     : true,  // enable cookies to allow the server to access the session
            xfbml      : true,  // parse social plugins on this page
            version    : 'v3.2' // use graph api version 2.8
        });

        // Check whether the user already logged in
        FB.getLoginStatus(function(response) {
            if (response.status === 'connected') {
                //display user data
                getFbUserData();
            }
        });
    };

    // Load the JavaScript SDK asynchronously
    (function(d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) return;
        js = d.createElement(s); js.id = id;
        js.src = "//connect.facebook.net/en_US/sdk.js";
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));

    // Facebook login with JavaScript SDK
    function fbLogin() {
        FB.login(function (response) {
            if (response.authResponse) {
                // Get and display the user profile data
                getFbUserData();
            } else {
                document.getElementById('status').innerHTML = 'User cancelled login or did not fully authorize.';
            }
        }, {scope: 'email'});
    }

    // Fetch the user profile data from facebook
    function getFbUserData(){
        FB.api('/me', {locale: 'en_US', fields: 'id,first_name,last_name,email,link,gender,locale,picture'},
            function (response) {
                // Save user data
                saveUserData(response);
                
                if(response.email !== null){
                    fbLogout();
                    window.location.href = 'dashboard';
                }else{
                    fbLogout();
                    <?php //$_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?>
                    window.location.href = 'login';
                }

            });
    }

    // Logout from facebook
    function fbLogout() {
        FB.logout(function() {
//            document.getElementById('fbLink').setAttribute("onclick","fbLogin()");
//            document.getElementById('fbLink').innerHTML = '<img src="images/fb-login-btn.png"/>';
//            document.getElementById('userData').innerHTML = '';
//            document.getElementById('status').innerHTML = '<p>You have successfully logout from Facebook.</p>';
        });
    }
</script>
<script>
    // Save user data to the database
    function saveUserData(userData){
        $.ajax({
            type: 'POST',
            url: 'facebook_login.php',
            cache: false,
            data: {oauth_provider:'facebook',userData: JSON.stringify(userData)},
            success: function (response) {
//                alert(response);
                return true;
            }
        });
    }
</script>
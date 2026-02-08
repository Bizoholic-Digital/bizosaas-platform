<?php
$admin_google_client_id = $footer_row['admin_google_client_id'];
$admin_google_client_secret = $footer_row['admin_google_client_secret'];
?>

<meta name="google-signin-client_id" content="<?php echo $admin_google_client_id; ?>">
<script src="https://apis.google.com/js/platform.js" async defer></script>
<script>
    /**
     * Handler for the signin callback triggered after the user selects an account.
     */
    function onSignInCallback(resp) {
        gapi.client.load('plus', 'v1', apiClientLoaded);
    }

    /**
     * Sets up an API call after the Google API client loads.
     */
    function apiClientLoaded() {
        gapi.client.plus.people.get({userId: 'me'}).execute(handleEmailResponse);
    }

    /**
     * Response callback for when the API client receives a response.
     *
     * @param resp The API response object with the user email and profile information.
     */
    function handleEmailResponse(resp) {
        var primaryEmail;
        for (var i=0; i < resp.emails.length; i++) {
            if (resp.emails[i].type === 'account') primaryEmail = resp.emails[i].value;
        }

        $.ajax({
            type: 'POST',
            url: 'google_login.php',
            cache: false,
            data: {gp_details: resp},
            success: function (response) {
            if(response=='1'){
                signOut();
                window.location.reload("dashboard.php");
            }else{
                signOut();
                window.location.reload("dashboard.php");
            }


        }
        });
//        document.getElementById('responseContainer').value = 'Primary email: ' +
//            primaryEmail + '\n\nFull Response:\n' + JSON.stringify(resp);
    }


    function onSignIn(googleUser) {
        var profile = googleUser.getBasicProfile();
        console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
        console.log('Name: ' + profile.getName());
        console.log('Image URL: ' + profile.getImageUrl());
        console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.

        $.ajax({
            type: 'POST',
            url: 'google_login.php',
            cache: false,
            data: {gp_details: profile.getId(),name:profile.getName(),email:profile.getEmail()},
            success: function (response) {
            if(response=='1'){
                signOut();
                window.location.reload("dashboard.php");
            }else{
                signOut();
                window.location.reload("dashboard.php");
            }


        }
        });

    }
</script>
<script>
    function signOut() {
        var auth2 = gapi.auth2.getAuthInstance();
        auth2.signOut().then(function () {
            console.log('User signed out.');
        });

    }
</script>
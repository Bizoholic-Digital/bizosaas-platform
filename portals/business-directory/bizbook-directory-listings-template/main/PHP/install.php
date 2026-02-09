<!DOCTYPE html>
<html>
<head>
    <title>Bizbook Installation</title>
    <!--== CSS FILES ==-->
    <link rel="stylesheet" href="css/style.php">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">

</head>
<style>
    body {
        margin: 0;
        padding: 0;
        background: #f0f2f5;
    }

    .pg-install, .pg-install h4, .pg-install p, .pg-install h6, .pg-install a, .pg-install td, .pg-install button {
        font-family: 'Roboto', sans-serif;
    }
</style>
<!-- START -->
<section class="pg-install">
    <div class="inn">
        <div class="s1"><img src="images/bizbook-black.png" alt="Bizbook template installation"
                             title="Bizbook directory template by Rn53themes.net"></div>
        <div class="s2">
            <h4>Below you should enter your <b>database connection</b> details.</h4>
            <p>Note: First you need to create a new database then follow below details. <a href="#">Tutorial video for
                    how to create a new database.</a></p>
            <form>
                <table>
                    <tbody>
                    <tr>
                        <td><h6>Database Name</h6></td>
                        <td><input type="text" required></td>
                        <td>The name of the <b>database</b>.</td>
                    </tr>
                    <tr>
                        <td><h6>Username</h6></td>
                        <td><input type="text" required></td>
                        <td>Your database <b>username</b>.</td>
                    </tr>
                    <tr>
                        <td><h6>Password</h6></td>
                        <td><input type="text" required></td>
                        <td>Your database <b>password</b>.</td>
                    </tr>
                    <tr>
                        <td><h6>Database Host name</h6></td>
                        <td><input type="text" value="localhost" required></td>
                        <td></td>
                    </tr>
                    <tr>
                        <td></td>
                        <td>
                            <button>Submit Now</button>
                        </td>
                        <td></td>
                    </tr>
                    </tbody>
                </table>
            </form>
        </div>
    </div>
</section>
<!--END-->


<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>
</body>

</html>
$(document).ready(function () {
    $username = $("input.username");
    $first_name = $("input.first-name");
    $last_name = $("input.last-name");
    $email = $("input.email");
    $password = $("input.password");
    $date_of_birth = $("input.date-of-birth");

    $first_name.on('keydown', function() {
        $("div.first-name").text("")
    });

    $last_name.on('keydown', function() {
        $("div.last-name").text("")
    });

    $last_name.on('click', function () {
        if($first_name.val().length < 1){
            $("div.first-name").text("Name field can not be blank")
        }
    });

    $email.on('click', function () {
        if($last_name.val().length < 1){
            $("div.last-name").text("Name field can not be blank")
        }
    });

    // $email.on('keydown', function() {
    //     $("div.email").text("")
    // });

    $email.on('keydown', function () {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        // console.log(re.test($email.val()))
        if(re.test($email.val()) == false && $email.val().length > 0) {
            $("div.email").text($email.val() + " is not a valid email address")
        } else {
            $("div.email").text("")
        }
        // if($last_name.val().length < 1){
        //     $("div.email").text($email.val() + " is not a valid email address")
        // }
    });

    $password.on('click', function (event) {
        // console.log(event)
        if($email.val().length < 1){
            $("div.email").text("Email field can not be blank")
        }
    });

    $password.on('keydown', function() {
        $("div.password").text("")
    });

    $date_of_birth.on('click', function (event) {
        // console.log(event)
        if($password.val().length < 1){
            $("div.password").text("Password can not be blank")
        }
    });

    $("button").on('click', function (event) {
    // $("#signup-form").submit(function(){
        console.log("Button Clicked!")
        // console.log($(this).serialize())
       $.ajax({
           // console.log($(this).serialize())
           data: {
               'username':$username.val(),
               'email':$email.val(),
               'password':$password.val(),
               'date_of_birth':$date_of_birth.val()
           },
           type: "POST",
           url: '/api/signup'
       })
    });

});
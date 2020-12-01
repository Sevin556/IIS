/*$(document).ready(function() {
        $("#pwd_input").change(function() {
            var pwd_value = this.value;
            console.log("Requesting rating")
            $.ajax({
                type: "POST",
                url: "{% url 'rate-pwd' %}",
                data: { csrfmiddlewaretoken: "{{ csrf_token }}", pwd: pwd_value },
                dataType: "json",
                success: function(data) {
                    if (data.rating === "0") {
                        $("#pwd_rating").text("Unsuitable");
                    } else 
                    if (data.rating === "1") {
                        $("#pwd_rating").text("Weak");
                    } else 
                    if (data.rating === "2") {
                        $("#pwd_rating").text("Medium");
                    } else 
                    if (data.rating === "3") {
                        $("#pwd_rating").text("Strong");
                    } else {
                        $("#pwd_rating").text("Very Strong");
                    }
                }
            });
        });
    });*/
    
function check_pwd(){
    var pwd = document.getElementById("pwd_input").value;
    var rating = 0;

    if(pwd.length < 8) {
        document.getElementById("pwd_rating").innerHTML = "Password strength: Unsuitable";
        return;
    }

    if(has_lower(pwd)) {
        rating++;
    }
    if(has_upper(pwd)) {
        rating++;
    }
    if(has_digit(pwd)) {
        rating++;
    }
    if(has_symbol(pwd)) {
        rating++;
    }

    if (rating === 1) {
        document.getElementById("pwd_rating").innerHTML = "Password strength: Weak";
    } else 
    if (rating === 2) {
        document.getElementById("pwd_rating").innerHTML ="Password strength: Medium";
    } else 
    if (rating === 3) {
        document.getElementById("pwd_rating").innerHTML = "Password strength: Strong";
    } else {
        document.getElementById("pwd_rating").innerHTML = "Password strength: Very Strong";
    }
    return;
}

function has_lower(str) {
    return (/[a-z]/.test(str));
}

function has_upper(str) {
    return (/[A-Z]/.test(str));
}

function has_digit(str) {
    return (/[0-9]/.test(str));
}

function has_symbol(str) {
    //const patt = new RegExp(" !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~");
    return (/[-!$%^&*()_+|~=`{}\[\]:";'<>?,.\/]/.test(str));
}

function cmp_pwd() {
    var pwd1 = document.getElementById("pwd_input").value;
    var pwd2 = document.getElementById("repeat_pwd").value;
    
    if(pwd1 == pwd2) {
        document.getElementById("pwd_match").innerHTML = "Passwords match!";
        document.getElementById("submit_btn").disabled = false;
    } else {
        document.getElementById("pwd_match").innerHTML = "Passwords doesn't match!";
        document.getElementById("submit_btn").disabled = true;
    }
    
    return;
}

function unlock_btn() {
    var pwd1 = document.getElementById("pwd_input").value;
    var pwd2 = document.getElementById("repeat_pwd").value;
    
    if(pwd1 == "" && pwd2 == "") {
        document.getElementById("submit_btn").disabled = false;
    } else {
        document.getElementById("submit_btn").disabled = true;
    }
    
    return;
}
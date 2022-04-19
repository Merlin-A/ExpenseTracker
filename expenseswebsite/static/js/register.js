const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid-feedback");
const emailFeedBackArea = document.querySelector(".email-feedback");
const emailField = document.querySelector("#emailField");
const usernameSuccessOutput  = document.querySelector(".usernameSuccessOutput");
const passwordField = document.querySelector("#passwordField")
const passwordField1 = document.querySelector("#passwordField1")

const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");

const handleToggleInput = (e) => {

    if(showPasswordToggle.textContent ==='Show'){

        showPasswordToggle.textContent="Hide";
        
        passwordField.setAttribute("type", "text");

        

    }
    else{
        showPasswordToggle.textContent="Show";
        passwordField.setAttribute("type", "password");





    }




}

showPasswordToggle.addEventListener('click', handleToggleInput);



















emailField.addEventListener("keyup", (e) => { //to check when we are typing in the field

    const emailVal = e.target.value;

    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";
    



    if (emailVal.length > 0) { 
        fetch("/authentication/validate-email", {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
        })

            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                if (data.email_error) {
                    submitBtn.disabled = true; 
                    submitBtn.setAttribute("value", "Register Button Disabled");
                    emailField.classList.add("is-invalid");
                    emailFeedBackArea.style.display = "block";
                    emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;




                }
                else if (emailFeedBackArea.style.display === "none" &&  feedBackArea.style.display === "none"){
                    submitBtn.removeAttribute("disabled");
                    submitBtn.setAttribute("value", "Register");

                }




            });
    }



});


usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
    console.log("77777", 77777);
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`;


    usernameSuccessOutput.style.display="block";

    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = "none";

    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({ username: usernameVal }),
            method: "POST",
        })

            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                usernameSuccessOutput.style.display="none";
                if (data.username_error) {
                    submitBtn.disabled = true; 
                    submitBtn.setAttribute("value", "Register Button Disabled");
                    usernameField.classList.add("is-invalid");
                    feedBackArea.style.display = "block";
                    feedBackArea.innerHTML = `<p>${data.username_error}</p>`;




                }

                else if (emailFeedBackArea.style.display === "none" &&  feedBackArea.style.display === "none"){
                    submitBtn.removeAttribute("disabled");
                    submitBtn.setAttribute("value", "Register");
                }
          




            });
    }



});



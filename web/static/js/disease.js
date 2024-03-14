const leaf = document.getElementById("imageDisplay");
const input = document.getElementById("inputImage");
const button = document.querySelectorAll("#label");
const submitButton = document.querySelectorAll("#label")[1];
const menu = document.getElementById("dropdown");
const diseaseInfo = document.getElementById("diseaseInfo");
let dropdownValue;


//enabling/disabling the buttons(labels) if leaf-type is/isnt chosen
document.addEventListener('DOMContentLoaded', () => {
    button.forEach(btn => {
        btn.style.pointerEvents = 'none';
    });

    menu.addEventListener('change', () => {
        dropdownValue = menu.value;
        if (dropdownValue === "Select") {
            button.forEach(btn => {
                btn.style.pointerEvents = 'none';
            });
        }
        else {
            button.forEach(btn => {
                btn.style.pointerEvents = 'all';
            });
        }
    })
})


//displays the image given as input by the user & displays the dieaseInfo
input.addEventListener('change', () => {
    leaf.src = URL.createObjectURL(input.files[0]);
});


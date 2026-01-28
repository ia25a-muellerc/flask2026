const logo = document.querySelector(".logo");
const instagram = document.querySelector(".card1");
const ticktock = document.querySelector(".card2");


logo.addEventListener("click", ()=>{
    window.open("http://127.0.0.1:5000/", target="_self");
});

instagram.addEventListener("click", ()=>{
    window.open("https://instagram.com/deskdunk/", target="_blank");
});

ticktock.addEventListener("click", ()=>{
    window.open("https://www.tiktok.com/@desk.dunk", target="_blank");
});
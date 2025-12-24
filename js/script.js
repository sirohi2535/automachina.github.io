let earnings = 16746;
let tokens = 339;

function simulateEarnings() {
    let earn = Math.floor(Math.random()*500 + 50);
    let token = Math.floor(Math.random()*10 + 1);

    earnings += earn;
    tokens += token;

    document.getElementById("earnings").innerText = earnings.toFixed(2);
    document.getElementById("tokens").innerText = tokens;
    
    alert(`🚀 You earned ₹${earn} & ${token} tokens!`);
}

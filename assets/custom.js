// Could not find any way to initiate update_simulation upon loading the site. This is the only solution; clicking restart upon loading content. 
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        var resetButton = document.getElementById('reset-button');
        if (resetButton) { 
            resetButton.click(); 
        } 
    }, 100); 
}); 

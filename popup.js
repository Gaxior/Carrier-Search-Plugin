let lastQuery = ""; // Store the last query
let timeout; // Variable to manage debounce timeout

document.getElementById("nameInput").addEventListener("input", function() {
    const searchQuery = document.getElementById("nameInput").value.toLowerCase();

    // If the query hasn't changed, stop the process
    if (searchQuery === lastQuery) return;

    lastQuery = searchQuery;
    
    // Clear previous results
    clearTimeout(timeout);

    // Add a delay for searching to avoid firing every time a letter is typed
    timeout = setTimeout(() => {
        if (searchQuery.trim() === "") return;
        
        chrome.runtime.sendMessage({ type: 'search', query: searchQuery }, function(results) {
            displayResults(results);
        });
    }, 300); // 300ms delay
});

function displayResults(results) {
    const resultContainer = document.getElementById("result");
    resultContainer.innerHTML = ""; // Clear previous results

    if (results.length === 0) {
        resultContainer.innerHTML = "No results found";
    } else {
        // Display only the first 10 results
        const limitedResults = results.slice(0, 10);
        limitedResults.forEach(result => {
            // Exclude MPM ID from the displayed result
            const resultText = `${result.DM_ID} | ${result.Carrier_Integration_Code} | ${result.Carrier_Integration_Name} | ${result.MPM_Stack}`;
            resultContainer.innerHTML += `<p>${resultText}</p>`;
        });
        
        // Adjust the popup width to fit the longest result
        adjustPopupWidth(limitedResults);
    }
}

function adjustPopupWidth(results) {
    const resultContainer = document.getElementById("result");
    let maxLength = 0;

    // Find the longest result string (excluding MPM ID)
    results.forEach(result => {
        const resultText = `${result.DM_ID} | ${result.Carrier_Integration_Code} | ${result.Carrier_Integration_Name} | ${result.MPM_Stack}`;
        maxLength = Math.max(maxLength, resultText.length);
    });

    // Calculate the width based on the longest string (adjust the multiplier as needed)
    const width = 150 + maxLength * 4; // Adjust multiplier (8) to scale properly with your text size
    const maxWidth = 600; // Maximum width for the popup

    // Set the width to the calculated value, but ensure it doesn't exceed the max width
    document.body.style.width = `${Math.min(width, maxWidth)}px`;
}

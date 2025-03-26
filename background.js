let csvData = [];

function loadCSV() {
    fetch(chrome.runtime.getURL('data.csv'))
        .then(response => response.text())
        .then(text => {
            csvData = parseCSV(text);
        })
        .catch(error => console.error("Error loading CSV: ", error));
}

function parseCSV(csvText) {
    const rows = csvText.trim().split("\n");
    const data = rows.map(row => {
        const cols = row.split(",");
        return {
            DM_ID: cols[0],                  // DM ID
            MPM_ID: cols[1],                 // MPM ID (won't be displayed)
            Carrier_Integration_Code: cols[2], // Carrier Integration Code
            Carrier_Integration_Name: cols[3], // Carrier Integration Name
            MPM_Stack: cols[4]               // MPM Stack
        };
    });
    return data;
}

function searchCSV(query) {
    return csvData.filter(row => {
        // Search across all columns except MPM ID
        return Object.values(row).some(value => value.toLowerCase().includes(query));
    });
}

// Listen for messages from popup.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'search') {
        const results = searchCSV(message.query);
        sendResponse(results);
    }
});

// Load CSV on startup
loadCSV();

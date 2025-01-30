// Handle additional information form submission
document.getElementById('additionalInfoForm').addEventListener('submit', (event) => {
    event.preventDefault();
    document.getElementById('submissionMessage').textContent = 'Submitting...';

    const cloudName = document.getElementById('cloudVendor').value;
    const companyName = document.getElementById('companyName').value;
    const addressOne = document.getElementById('addressOne').value;
    const addressTwo = document.getElementById('addressTwo').value;
    const addressThree = document.getElementById('addressThree').value;
    const attn = document.getElementById('attn').value;
    const invoiceDate = new Date(document.getElementById('invoiceDate').value);
    const formattedDate = invoiceDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    const exchangeRate = document.getElementById('exchangeRate').value;

    const queryString = `?cloudName=${encodeURIComponent(cloudName)}&companyName=${encodeURIComponent(companyName)}&addressOne=${encodeURIComponent(addressOne)}&addressTwo=${encodeURIComponent(addressTwo)}&addressThree=${encodeURIComponent(addressThree)}&attn=${encodeURIComponent(attn)}&invoiceDate=${encodeURIComponent(formattedDate)}&exchangeRate=${encodeURIComponent(exchangeRate)}`;
    const apiUrl = `${apiGW}${queryString}`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            console.log('API response:', data);
            if (data) {
                // Extract the base64 string
                const base64String = data.slice(2, -1);
 
                const link = document.createElement('a');
                link.href = `data:application/pdf;base64,${base64String}`;
                link.download = 'invoice.pdf';
                link.textContent = 'Download PDF';
                document.getElementById('submissionMessage').innerHTML = 'Information submitted successfully! ';
                document.getElementById('submissionMessage').appendChild(link);
            } else {
                document.getElementById('submissionMessage').textContent = 'Information submitted successfully!';
            }
        })
        .catch(error => {
            console.error('Error submitting information:', error);
            alert('Submission failed!');
        });
});

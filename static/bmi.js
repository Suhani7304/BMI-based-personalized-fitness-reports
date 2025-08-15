document.getElementById('bmiForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const height = document.getElementById('height').value;
    const weight = document.getElementById('weight').value;

    try {
        const response = await fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ height: parseFloat(height), weight: parseFloat(weight) }),
        });

        const data = await response.json();

        if (response.ok) {
            const { bmi, category, recommendations_bmi } = data;

            // Display results
            document.getElementById('result').innerHTML = `
                <h3>Your BMI: ${bmi}</h3>
                <button id="download-pdf">Generate Report</button>
            `;

            // Add event listener for PDF download
            document.getElementById('download-pdf').addEventListener('click', async () => {
                const currentDate = new Date().toISOString().split('T')[0];
                const pdfResponse = await fetch('/generate-pdf', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({height: parseFloat(height), weight: parseFloat(weight), bmi, category, recommendations_bmi, current_date: currentDate }),
                });

                if (pdfResponse.ok) {
                    const blob = await pdfResponse.blob(); //converts the response body into a binary large object (Blob)...Blob is a file-like object that holds raw data, such as the contents of the PDF in this case.
                    const url = window.URL.createObjectURL(blob); // generates a temporary URL for the Blob that can be used to reference it in the browser.
                    const a = document.createElement('a'); // create an anchor tab
                    a.href = url;   // set the blob url
                    a.download = 'BMI_Report.pdf'; // name of file when downloadd
                    document.body.appendChild(a);
                    a.click(); //simulates a user click on the link, triggering the browser to download the file.
                    a.remove(); // removes the temporary <a> element from the DOM to clean up.
                } else {
                    alert('Failed to generate PDF');
                }
            });
        } else {
            document.getElementById('result').innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        }
    } catch (error) {
        document.getElementById('result').innerHTML = `<p style="color: red;">An error occurred: ${error.message}</p>`;
    }
});

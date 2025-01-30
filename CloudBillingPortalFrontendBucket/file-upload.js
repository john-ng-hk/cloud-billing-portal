// Display selected files
document.getElementById('fileInput').addEventListener('change', (event) => {
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = '';
    Array.from(event.target.files).forEach(file => {
        const li = document.createElement('li');
        li.className = 'file-list-item';
        li.innerHTML = `<span>${file.name}</span><span class="success-message" style="visibility: hidden;">File upload successful!</span>`;
        fileList.appendChild(li);
    });
});

// Function to upload files
async function uploadFiles() {
    console.log('Upload button clicked');
    const files = document.getElementById('fileInput').files;
    if (files.length === 0) {
        console.log('No files selected');
        return;
    }
    console.log('Files selected:', files);

    const s3 = new AWS.S3({
        apiVersion: '2006-03-01',
        params: { Bucket: backendBucket }
    });

    let uploadCount = 0;
    Array.from(files).forEach(file => {
        const params = {
            Key: `${backendBucket}/${file.name}`,
            Body: file,
            ContentType: file.type
        };
        s3.upload(params, function(err, data) {
            if (err) {
                console.error('Error uploading file:', err);
            } else {
                console.log('Successfully uploaded file:', data);
                const fileListItem = Array.from(document.getElementById('fileList').children).find(li => li.textContent.includes(file.name));
                if (fileListItem) {
                    fileListItem.querySelector('.success-message').style.visibility = 'visible';
                }
                uploadCount++;
                if (uploadCount === files.length) {
                    document.getElementById('uploadMessage').textContent = 'All files uploaded successfully! Redirecting...';
                    setTimeout(() => {
                        document.getElementById('uploadSection').style.display = 'none';
                        document.getElementById('additionalInfoSection').style.display = 'block';
                    }, 1000); // Redirect after 1 second
                }
            }
        });
    });
}

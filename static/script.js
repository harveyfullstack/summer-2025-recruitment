const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const testBtn = document.getElementById('testBtn');
const endpoint = document.getElementById('endpoint');
const statusBar = document.getElementById('statusBar');
const statusText = document.getElementById('statusText');
const responseTime = document.getElementById('responseTime');
const responseContainer = document.getElementById('responseContainer');

let selectedFile = null;

uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    selectedFile = file;
    uploadArea.innerHTML = `
        <div>📄 ${file.name}</div>
        <div style="font-size: 12px; color: #6b7280; margin-top: 5px;">${(file.size / 1024).toFixed(1)} KB</div>
    `;
    updateTestButton();
}

function updateTestButton() {
    const isHealthCheck = endpoint.value === '/health';
    const uploadGroup = document.querySelector('.form-group:nth-child(2)');
    const samplesSection = document.querySelector('.samples');
    
    if (isHealthCheck) {
        uploadGroup.style.display = 'none';
        samplesSection.style.display = 'none';
        testBtn.disabled = false;
    } else {
        uploadGroup.style.display = 'flex';
        samplesSection.style.display = 'block';
        testBtn.disabled = !selectedFile;
    }
}

endpoint.addEventListener('change', updateTestButton);

document.querySelectorAll('.sample-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        const filename = btn.dataset.file;
        try {
            const response = await fetch(`/static/samples/${filename}`);
            const blob = await response.blob();
            const file = new File([blob], filename, { type: blob.type });
            handleFileSelect(file);
        } catch (error) {
            console.error('Failed to load sample file:', error);
        }
    });
});

testBtn.addEventListener('click', async () => {
    const endpointValue = endpoint.value;
    const startTime = Date.now();
    
    statusBar.style.display = 'flex';
    statusText.textContent = 'Testing...';
    statusText.className = '';
    responseTime.textContent = '';
    
    responseContainer.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            Making API request...
        </div>
    `;
    
    try {
        let response;
        
        if (endpointValue === '/health') {
            response = await fetch('/health');
        } else {
            const formData = new FormData();
            formData.append('file', selectedFile);
            
            response = await fetch(endpointValue, {
                method: 'POST',
                body: formData
            });
        }
        
        const endTime = Date.now();
        const responseTimeMs = endTime - startTime;
        
        const data = await response.json();
        
        statusText.textContent = `Status: ${response.status} ${response.statusText}`;
        statusText.className = response.ok ? 'status-success' : 'status-error';
        responseTime.textContent = `${(responseTimeMs / 1000).toFixed(2)}s`;
        
        responseContainer.innerHTML = `
            <div class="response-container">${JSON.stringify(data, null, 2)}</div>
        `;
        
    } catch (error) {
        const endTime = Date.now();
        const responseTimeMs = endTime - startTime;
        
        statusText.textContent = 'Error: Request failed';
        statusText.className = 'status-error';
        responseTime.textContent = `${(responseTimeMs / 1000).toFixed(2)}s`;
        
        responseContainer.innerHTML = `
            <div class="response-container">Error: ${error.message}</div>
        `;
    }
});

updateTestButton();
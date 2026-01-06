// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const apiStatusEl = document.getElementById('api-status');
const totalRecordsEl = document.getElementById('total-records');
const metadataCountEl = document.getElementById('metadata-count');
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const uploadProgress = document.getElementById('upload-progress');
const progressFill = document.getElementById('progress-fill');
const progressText = document.getElementById('progress-text');
const uploadResult = document.getElementById('upload-result');
const resultTitle = document.getElementById('result-title');
const resultMessage = document.getElementById('result-message');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    checkApiStatus();
    loadDataCounts();
    setupFileUpload();
    
    // Refresh data every 30 seconds
    setInterval(loadDataCounts, 30000);
});

// Check API status
async function checkApiStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            const data = await response.json();
            apiStatusEl.textContent = 'Online';
            apiStatusEl.className = 'status-text status-online';
        } else {
            throw new Error('API not responding');
        }
    } catch (error) {
        apiStatusEl.textContent = 'Offline';
        apiStatusEl.className = 'status-text status-offline';
        console.error('API Status Check Failed:', error);
    }
}

// Load data counts
async function loadDataCounts() {
    try {
        const response = await fetch(`${API_BASE_URL}/count`);
        if (response.ok) {
            const data = await response.json();
            totalRecordsEl.textContent = data.records.toLocaleString();
            metadataCountEl.textContent = data.metadata_entries.toLocaleString();
        }
    } catch (error) {
        console.error('Failed to load data counts:', error);
    }
}

// Setup file upload functionality
function setupFileUpload() {
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Click to upload
    uploadArea.addEventListener('click', () => fileInput.click());
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        uploadFile(file);
    }
}

// Handle drag over
function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

// Handle drag leave
function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
}

// Handle file drop
function handleDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        uploadFile(files[0]);
    }
}

// Upload file to API
async function uploadFile(file) {
    // Validate file type
    if (!file.name.toLowerCase().endsWith('.xml')) {
        showUploadResult(false, 'Please select a valid XML file');
        return;
    }
    
    // Validate file size (600MB limit)
    const maxSize = 600 * 1024 * 1024; // 600MB
    if (file.size > maxSize) {
        showUploadResult(false, 'File size exceeds 600MB limit');
        return;
    }
    
    // Show progress
    showUploadProgress();
    
    // Create form data
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        // Simulate progress (since we can't track real progress with fetch)
        simulateProgress();
        
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            showUploadResult(true, result.message);
            loadDataCounts(); // Refresh counts
            
            // Refresh analytics after successful upload
            if (window.healthAnalytics) {
                setTimeout(() => {
                    window.healthAnalytics.init();
                }, 1000);
            }
        } else {
            const errorText = await response.text();
            showUploadResult(false, `Upload failed: ${errorText}`);
        }
    } catch (error) {
        showUploadResult(false, `Upload failed: ${error.message}`);
    } finally {
        hideUploadProgress();
    }
}

// Show upload progress
function showUploadProgress() {
    uploadProgress.style.display = 'block';
    uploadResult.style.display = 'none';
    progressFill.style.width = '0%';
    progressText.textContent = 'Preparing upload...';
}

// Hide upload progress
function hideUploadProgress() {
    uploadProgress.style.display = 'none';
}

// Simulate upload progress
function simulateProgress() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) progress = 90;
        
        progressFill.style.width = `${progress}%`;
        progressText.textContent = `Uploading... ${Math.round(progress)}%`;
        
        if (progress >= 90) {
            clearInterval(interval);
        }
    }, 500);
}

// Show upload result
function showUploadResult(success, message) {
    uploadResult.style.display = 'block';
    
    if (success) {
        resultTitle.textContent = 'Upload Successful!';
        resultTitle.style.color = '#10b981';
        resultMessage.textContent = message;
        uploadResult.querySelector('.success-icon').className = 'fas fa-check-circle success-icon';
    } else {
        resultTitle.textContent = 'Upload Failed';
        resultTitle.style.color = '#ef4444';
        resultMessage.textContent = message;
        uploadResult.querySelector('.success-icon').className = 'fas fa-exclamation-circle success-icon';
        uploadResult.querySelector('.success-icon').style.color = '#ef4444';
    }
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        uploadResult.style.display = 'none';
    }, 5000);
}

// Utility function to format numbers
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

// Utility function to format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

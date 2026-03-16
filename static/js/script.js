/**
 * Professional QR Code Generator - Drag & Drop Handler
 * Modern, accessible, performant drag & drop functionality
 */

class QRDropZone {
    constructor() {
        this.dropZone = document.getElementById("dropZone");
        this.fileInput = document.getElementById("fileInput");
        this.linkInput = document.getElementById("linkInput");
        this.generateBtn = document.getElementById("generateBtn");
        this.loadingSpinner = document.querySelector(".loading");
        this.errorMessage = document.getElementById("errorMessage");
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateButtonState();
    }

    bindEvents() {
        // Click to browse files
        this.dropZone.addEventListener("click", (e) => {
            if (!e.target.closest('input')) {
                this.fileInput.click();
            }
        });

        // File input change handler
        this.fileInput.addEventListener("change", (e) => {
            this.handleFileSelect(e.target.files);
        });

        // Drag & Drop Events
        this.dropZone.addEventListener("dragover", this.handleDragOver.bind(this));
        this.dropZone.addEventListener("dragenter", this.handleDragEnter.bind(this));
        this.dropZone.addEventListener("dragleave", this.handleDragLeave.bind(this));
        this.dropZone.addEventListener("drop", this.handleDrop.bind(this));

        // Input validation
        this.linkInput.addEventListener("input", this.updateButtonState.bind(this));
        this.fileInput.addEventListener("change", this.updateButtonState.bind(this));

        // Form submission
        this.generateBtn.addEventListener("click", this.handleGenerate.bind(this));

        // Keyboard accessibility
        this.dropZone.addEventListener("keydown", this.handleKeydown.bind(this));
    }

    handleFileSelect(files) {
        if (files.length > 0) {
            this.displayFileName(files[0].name);
            this.updateButtonState();
        }
    }

    handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        this.dropZone.classList.add("dragover");
    }

    handleDragEnter(e) {
        e.preventDefault();
        e.stopPropagation();
        this.dropZone.classList.add("dragover");
    }

    handleDragLeave(e) {
        e.preventDefault();
        e.stopPropagation();
        if (!this.dropZone.contains(e.relatedTarget)) {
            this.dropZone.classList.remove("dragover");
        }
    }

    handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        
        this.dropZone.classList.remove("dragover");
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.fileInput.files = files;
            this.displayFileName(files[0].name);
            this.updateButtonState();
        }
    }

    displayFileName(filename) {
        const maxLength = 35;
        const displayName = filename.length > maxLength 
            ? filename.substring(0, maxLength) + '...' 
            : filename;
            
        this.dropZone.innerHTML = `
            <div class="file-uploaded">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14,2 14,8 20,8"/>
                </svg>
                <p>Uploaded: <strong>${displayName}</strong></p>
                <button type="button" class="remove-file" title="Remove file">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                </button>
            </div>
        `;
        
        // Bind remove button
        this.dropZone.querySelector('.remove-file').addEventListener('click', () => {
            this.clearFile();
        });
    }

    clearFile() {
        this.fileInput.value = '';
        this.dropZone.innerHTML = this.getDefaultDropZoneHTML();
        this.updateButtonState();
    }

    getDefaultDropZoneHTML() {
        return `
            <div class="icon">📎</div>
            <p>Drop your file here or <strong>click to browse</strong></p>
            <p class="small">Supports PDF, images, documents (max 10MB)</p>
            <input type="file" id="fileInput" accept=".pdf,.jpg,.jpeg,.png,.gif,.doc,.docx,.txt">
        `;
    }

    updateButtonState() {
        const hasLink = this.linkInput.value.trim().length > 0;
        const hasFile = this.fileInput.files.length > 0;
        
        this.generateBtn.disabled = !(hasLink || hasFile);
        this.generateBtn.textContent = hasLink ? 'Generate QR from Link' : 'Generate QR from File';
    }

    handleGenerate() {
        const hasLink = this.linkInput.value.trim().length > 0;
        const hasFile = this.fileInput.files.length > 0;
        
        if (!hasLink && !hasFile) {
            this.showError('Please provide a link or upload a file');
            return;
        }

        // Show loading state
        this.showLoading();
        
        // Simulate API call (replace with actual form submission)
        setTimeout(() => {
            this.hideLoading();
            // Redirect to result or show success
            window.location.href = '/generate';
        }, 2000);
    }

    handleKeydown(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            this.fileInput.click();
        }
        if (e.key === 'Escape') {
            this.clearFile();
        }
    }

    showLoading() {
        this.generateBtn.disabled = true;
        this.generateBtn.innerHTML = `
            <svg class="spinner-btn" width="20" height="20" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" stroke-linecap="round"/>
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" stroke-dasharray="31.4" stroke-dashoffset="31.4" stroke-linecap="round">
                    <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
                </circle>
            </svg>
            Generating QR Code...
        `;
        this.loadingSpinner?.classList.add('show');
    }

    hideLoading() {
        this.generateBtn.disabled = false;
        this.generateBtn.textContent = 'Generate QR Code ✨';
        this.loadingSpinner?.classList.remove('show');
    }

    showError(message) {
        if (this.errorMessage) {
            this.errorMessage.textContent = message;
            this.errorMessage.classList.add('error-message');
            setTimeout(() => {
                this.errorMessage.classList.remove('error-message');
            }, 5000);
        }
    }

    // File validation helper
    validateFile(file) {
        const maxSize = 200 * 1024 * 1024; // 200MB
        const allowedTypes = [
            'application/pdf',
            'image/jpeg', 'image/jpg', 'image/png', 'image/gif',
            'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain'
        ];

        if (file.size > maxSize) {
            throw new Error('File size must be less than 10MB');
        }
        
        if (!allowedTypes.includes(file.type)) {
            throw new Error('Unsupported file type');
        }
        
        return true;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new QRDropZone();
});

// Prevent default drag behaviors on window
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    document.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}
// Clara Onboarding Website JavaScript
// Handles form navigation, validation, and user interactions

// Debug: Log when script loads
console.log('🚀 Clara Onboarding script loaded successfully');

class ClaraOnboarding {
    constructor() {
        console.log('🎯 Initializing ClaraOnboarding class');
        this.currentSection = 1;
        this.totalSections = 3;
        this.formData = {};
        
        // API Configuration - Change this for local development
        this.config = {
            // Set to true when running local agent server
            useLocalAPI: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1',
            localAPIUrl: 'http://localhost:8000',
            productionAPIUrl: '' // Uses relative URLs for Vercel
        };
        
        console.log('🔧 API Config:', this.config);
        
        this.quotes = [
            "Clara is getting her virtual coffee ready... ☕ She's about to become your best front desk assistant!",
            "Fun fact: Clara never calls in sick, never takes lunch breaks, and always answers with a smile! 😊",
            "We're teaching Clara your business so well, she might know it better than you do! 🤓",
            "Clara is practicing her 'professional voice' - she's almost ready to impress your callers! 🎭",
            "Did you know? Clara can handle multiple calls simultaneously without breaking a sweat! 💪",
            "Clara is learning your website faster than a speed reader on espresso! 📚⚡",
            "Almost there! Clara is putting on her customer service cape... 🦸‍♀️",
            "Clara promises to be more reliable than your morning alarm clock! ⏰",
            "Final touches! Clara is rehearsing her 'How may I help you?' - it's going to be perfect! ✨"
        ];
        this.currentQuote = 0;
        this.websiteCount = 1;
        this.ccEmailCount = 0;
        this.smsNumberCount = 1;
        this.uploadedFiles = [];
        this.init();
    }

    init() {
        console.log('🔄 Initializing Clara Onboarding...');
        this.bindEvents();
        this.updateNavigation();
        this.setupConditionalFields();
        this.setupFileUpload();
        console.log('✅ Clara Onboarding initialized successfully');
    }

    bindEvents() {
        // Form input events for real-time validation
        const inputs = document.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('input', () => this.validateCurrentSection());
            input.addEventListener('blur', () => this.validateField(input));
        });

        // Enter key navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const nextBtn = document.getElementById('next-btn');
                if (nextBtn && nextBtn.style.display !== 'none') {
                    this.nextSection();
                }
            }
        });
    }

    setupConditionalFields() {
        // Email checkbox - enabled by default
        const emailCheckbox = document.getElementById('postCallSummaryEmail');
        const emailGroup = document.getElementById('emailSummaryGroup');
        const primaryEmailInput = document.getElementById('primaryEmail');
        
        emailCheckbox.addEventListener('change', () => {
            if (emailCheckbox.checked) {
                emailGroup.style.display = 'block';
                emailGroup.classList.add('active');
                primaryEmailInput.required = true;
            } else {
                emailGroup.style.display = 'none';
                emailGroup.classList.remove('active');
                primaryEmailInput.required = false;
                primaryEmailInput.value = '';
                // Clear CC emails
                this.clearCCEmails();
            }
        });

        // SMS checkbox - enabled by default
        const smsCheckbox = document.getElementById('postCallSummarySMS');
        const smsGroup = document.getElementById('smsSummaryGroup');
        const primarySmsInput = document.getElementById('primarySmsNumber');
        
        smsCheckbox.addEventListener('change', () => {
            if (smsCheckbox.checked) {
                smsGroup.style.display = 'block';
                smsGroup.classList.add('active');
                primarySmsInput.required = true;
            } else {
                smsGroup.style.display = 'none';
                smsGroup.classList.remove('active');
                primarySmsInput.required = false;
                primarySmsInput.value = '';
                // Clear additional SMS numbers
                this.clearAdditionalSMSNumbers();
            }
        });
    }

    setupFileUpload() {
        const fileInput = document.getElementById('documentUpload');
        const uploadArea = document.getElementById('fileUploadArea');
        
        // Handle file selection
        fileInput.addEventListener('change', (e) => {
            this.handleFileUpload(e.target.files);
        });
        
        // Handle drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('drag-over');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
            this.handleFileUpload(e.dataTransfer.files);
        });
    }

    handleFileUpload(files) {
        const maxSize = 50 * 1024 * 1024; // 50MB
        const allowedTypes = ['.doc', '.docx'];
        
        Array.from(files).forEach(file => {
            // Check file size
            if (file.size > maxSize) {
                alert(`File "${file.name}" is too large. Maximum size is 50MB.`);
                return;
            }
            
            // Check file type
            const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
            if (!allowedTypes.includes(fileExtension)) {
                alert(`File "${file.name}" is not supported. Please upload DOC or DOCX files only.`);
                return;
            }
            
            // Add to uploaded files
            this.uploadedFiles.push(file);
            this.displayUploadedFile(file);
        });
    }

    displayUploadedFile(file) {
        const uploadedFilesContainer = document.getElementById('uploadedFiles');
        
        const fileElement = document.createElement('div');
        fileElement.className = 'uploaded-file';
        fileElement.innerHTML = `
            <div class="file-info">
                <i class="fas fa-file-word"></i>
                <span>${file.name}</span>
                <small>(${this.formatFileSize(file.size)})</small>
            </div>
            <button type="button" class="remove-file-btn" onclick="claraOnboarding.removeUploadedFile('${file.name}')">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        uploadedFilesContainer.appendChild(fileElement);
    }

    removeUploadedFile(fileName) {
        this.uploadedFiles = this.uploadedFiles.filter(file => file.name !== fileName);
        
        // Remove from display
        const uploadedFilesContainer = document.getElementById('uploadedFiles');
        const fileElements = uploadedFilesContainer.querySelectorAll('.uploaded-file');
        fileElements.forEach(element => {
            if (element.querySelector('span').textContent === fileName) {
                element.remove();
            }
        });
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Start onboarding from landing page
    startOnboarding() {
        this.showPage('details-page');
        this.animatePageTransition();
    }

    // Navigate to next form section
    nextSection() {
        if (!this.validateCurrentSection()) {
            this.showValidationErrors();
            return;
        }

        this.saveCurrentSectionData();

        if (this.currentSection < this.totalSections) {
            this.currentSection++;
            this.showSection(this.currentSection);
            this.updateNavigation();
            this.updateProgressBar();
        } else {
            this.goToReview();
        }
    }

    // Navigate to previous form section
    previousSection() {
        if (this.currentSection > 1) {
            this.currentSection--;
            this.showSection(this.currentSection);
            this.updateNavigation();
            this.updateProgressBar();
        }
    }

    // Show specific form section
    showSection(sectionNumber) {
        // Hide all sections
        document.querySelectorAll('.form-section').forEach(section => {
            section.classList.remove('active');
        });

        // Show target section
        const targetSection = document.getElementById(`section-${sectionNumber}`);
        if (targetSection) {
            targetSection.classList.add('active');
        }

        // Focus first input in section
        setTimeout(() => {
            const firstInput = targetSection.querySelector('input, select');
            if (firstInput) {
                firstInput.focus();
            }
        }, 300);
    }

    // Update navigation buttons
    updateNavigation() {
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');

        // Previous button
        if (this.currentSection === 1) {
            prevBtn.style.display = 'none';
        } else {
            prevBtn.style.display = 'inline-flex';
        }

        // Next button text
        if (this.currentSection === this.totalSections) {
            nextBtn.innerHTML = 'Review Details <i class="fas fa-arrow-right"></i>';
        } else {
            nextBtn.innerHTML = 'Next <i class="fas fa-arrow-right"></i>';
        }
    }

    // Update progress bar for sidebar layout
    updateProgressBar() {
        const steps = document.querySelectorAll('.progress-step-vertical');
        
        steps.forEach((step, index) => {
            const stepNumber = index + 1;
            step.classList.remove('active', 'completed');
            
            if (stepNumber < this.currentSection) {
                step.classList.add('completed');
            } else if (stepNumber === this.currentSection) {
                step.classList.add('active');
            }
        });
    }

    // Validate current section
    validateCurrentSection() {
        const currentSectionEl = document.getElementById(`section-${this.currentSection}`);
        const requiredInputs = currentSectionEl.querySelectorAll('input[required], select[required]');
        let isValid = true;

        requiredInputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });

        return isValid;
    }

    // Validate individual field
    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Remove existing error styling
        field.classList.remove('error');
        this.removeFieldError(field);

        // Required field validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'This field is required';
        }

        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'Please enter a valid email address';
            }
        }

        // Phone validation
        if (field.type === 'tel' && value) {
            const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
            if (!phoneRegex.test(value.replace(/[\s\-\(\)]/g, ''))) {
                isValid = false;
                errorMessage = 'Please enter a valid phone number';
            }
        }

        // URL validation
        if (field.type === 'url' && value) {
            try {
                new URL(value);
            } catch {
                isValid = false;
                errorMessage = 'Please enter a valid URL';
            }
        }

        // Password validation
        if (field.type === 'password' && value) {
            if (value.length < 8) {
                isValid = false;
                errorMessage = 'Password must be at least 8 characters long';
            }
        }

        // Show error if invalid
        if (!isValid) {
            this.showFieldError(field, errorMessage);
        }

        return isValid;
    }

    // Show field error
    showFieldError(field, message) {
        field.classList.add('error');
        
        // Create error element if it doesn't exist
        let errorEl = field.parentNode.querySelector('.field-error');
        if (!errorEl) {
            errorEl = document.createElement('div');
            errorEl.className = 'field-error';
            field.parentNode.appendChild(errorEl);
        }
        
        errorEl.textContent = message;
        errorEl.style.display = 'block';
    }

    // Remove field error
    removeFieldError(field) {
        const errorEl = field.parentNode.querySelector('.field-error');
        if (errorEl) {
            errorEl.style.display = 'none';
        }
    }

    // Show validation errors with animation
    showValidationErrors() {
        const currentSectionEl = document.getElementById(`section-${this.currentSection}`);
        const invalidInputs = currentSectionEl.querySelectorAll('.error');
        
        if (invalidInputs.length > 0) {
            // Shake animation for the form card
            const formCard = currentSectionEl.querySelector('.form-card');
            formCard.style.animation = 'shake 0.5s ease-in-out';
            
            setTimeout(() => {
                formCard.style.animation = '';
            }, 500);
            
            // Focus first invalid input
            invalidInputs[0].focus();
        }
    }

    // Save current section data
    saveCurrentSectionData() {
        const currentSectionEl = document.getElementById(`section-${this.currentSection}`);
        const inputs = currentSectionEl.querySelectorAll('input:not([type="file"]):not([type="checkbox"]), select');
        
        inputs.forEach(input => {
            if (input.name && input.value) {
                this.formData[input.name] = input.value;
            }
        });
        
        // Handle checkboxes separately
        const checkboxes = currentSectionEl.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            if (checkbox.name) {
                this.formData[checkbox.name] = checkbox.checked;
            }
        });
    }

    // Navigate to review page
    goToReview() {
        this.saveCurrentSectionData();
        this.showPage('review-page');
        this.updateReviewProgressBar();
        this.populateReview();
    }

    // Navigate back to details page from review
    goToDetails() {
        this.showPage('details-page');
        this.currentSection = this.totalSections;
        this.updateNavigation();
        this.updateProgressBar();
    }

    // Confirm details and start agent creation
    confirmDetails() {
        this.showPage('loading-page');
        this.startLoadingAnimation();
        this.createAgentReal();
    }

    // Actually create the agent via API
    async createAgentReal() {
        try {
            // Collect all form data
            const websites = this.getWebsiteUrls();
            const businessDays = this.getSelectedBusinessDays();
            const ccEmails = this.getCCEmails();
            const smsNumbers = this.getSMSNumbers();
            
            // Validate company name length before sending
            const companyName = this.formData.companyName;
            if (companyName && companyName.length > 50) {
                this.showError('Company name is too long for the knowledge base', [
                    `Current name: "${companyName}" (${companyName.length} characters)`,
                    'Please use a shorter company name (maximum 50 characters)',
                    'Go back and edit your company name'
                ]);
                return;
            }
            
            // Prepare data for simplified API
            const apiData = {
                company_name: companyName,
                assistant_name: this.formData.assistantName || 'Clara',
                business_address: this.formData.officeAddress,
                timezone: this.formData.timeZone,
                business_hours: this.formatBusinessHours(businessDays, document.getElementById('startTime').value, document.getElementById('endTime').value),
                website_url: websites[0] || '', // Primary website
                primary_phone_number: this.formData.contactNumber,
                preferred_area_code: this.extractAreaCode(this.formData.contactNumber),
                fallback_area_codes: ['212', '415', '213', '312', '617'], // Default fallbacks
                allow_emergency_transfer: false, // Default to false
                emergency_transfer_number: null
            };

            // Determine API endpoint
            const apiBaseUrl = this.config.useLocalAPI ? this.config.localAPIUrl : this.config.productionAPIUrl;
            const onboardUrl = this.config.useLocalAPI ? `${apiBaseUrl}/onboard` : '/api/onboard';

            // Start onboarding workflow
            const response = await fetch(onboardUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(apiData)
            });

            const result = await response.json();

            if (result.success) {
                // Onboarding completed successfully
                this.completeAgentCreationReal(result);
            } else {
                // Handle API validation errors
                let troubleshootingTips = [];
                const errorMsg = result.error || 'Failed to complete onboarding';
                
                if (errorMsg.includes('Missing required field')) {
                    troubleshootingTips = [
                        'Please fill in all required fields',
                        'Go back and check your form entries',
                        'Make sure all sections are completed'
                    ];
                } else if (errorMsg.includes('company name')) {
                    troubleshootingTips = [
                        'Use a shorter company name (max 50 characters)',
                        'Remove special characters if any',
                        'Try using abbreviations or acronyms'
                    ];
                } else if (errorMsg.includes('phone number')) {
                    troubleshootingTips = [
                        'No phone numbers available in your area code',
                        'Try a different area code',
                        'Contact support for assistance'
                    ];
                }
                
                this.showError(errorMsg, troubleshootingTips);
            }

        } catch (error) {
            console.error('Agent creation error:', error);
            this.showError('Failed to create agent: ' + error.message, [
                'Check your internet connection',
                'Verify all form fields are filled correctly',
                'Try refreshing the page and starting over',
                'Contact support if the problem persists'
            ]);
        }
    }

    // Extract area code from phone number
    extractAreaCode(phoneNumber) {
        if (!phoneNumber) return '212'; // Default to NYC
        
        // Remove all non-digits
        const digits = phoneNumber.replace(/\D/g, '');
        
        // If it's 11 digits and starts with 1, take next 3 digits
        if (digits.length === 11 && digits.startsWith('1')) {
            return digits.substring(1, 4);
        }
        
        // If it's 10 digits, take first 3
        if (digits.length === 10) {
            return digits.substring(0, 3);
        }
        
        // Default fallback
        return '212';
    }

    // Format business hours for backend
    formatBusinessHours(days, startTime, endTime) {
        const formattedStart = this.formatTime(startTime);
        const formattedEnd = this.formatTime(endTime);
        return `${formattedStart} - ${formattedEnd}, ${days.join(', ')}`;
    }

    // Complete agent creation with real data
    completeAgentCreationReal(result) {
        clearInterval(this.quoteInterval);
        
        // Use real credentials from the simplified result
        const phoneNumber = result.phone_number || '+1 (555) 000-0000';
        const dashboardEmail = result.dashboard_email || 'support@company.justclara.ai';
        const dashboardPassword = result.dashboard_password || 'company@321';
        
        // Debug: Log credentials to console
        console.log('Dashboard Credentials:', {
            email: dashboardEmail,
            password: dashboardPassword,
            phone: phoneNumber,
            company_id: result.company_id
        });
        
        // Update success page with real credentials
        document.getElementById('clara-phone').textContent = phoneNumber;
        document.getElementById('dashboard-email').textContent = dashboardEmail;
        document.getElementById('dashboard-password').textContent = dashboardPassword;
        
        this.showPage('success-page');
    }

    // Show error message with troubleshooting tips
    showError(message, troubleshootingTips = []) {
        clearInterval(this.quoteInterval);
        
        // Create troubleshooting tips HTML
        let troubleshootingHTML = '';
        if (troubleshootingTips && troubleshootingTips.length > 0) {
            troubleshootingHTML = `
                <div class="troubleshooting-tips">
                    <h4><i class="fas fa-lightbulb"></i> Troubleshooting Tips:</h4>
                    <ul>
                        ${troubleshootingTips.map(tip => `<li>${tip}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        
        // Create error page content
        const loadingContainer = document.querySelector('.loading-container');
        loadingContainer.innerHTML = `
            <div class="error-animation">
                <div class="error-icon">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
            </div>
            <div class="error-content">
                <h2>Oops! Something went wrong</h2>
                <p class="error-message">${message}</p>
                ${troubleshootingHTML}
                <div class="error-actions">
                    <button class="nav-button primary" onclick="location.reload()">
                        <i class="fas fa-refresh"></i>
                        Try Again
                    </button>
                    <button class="nav-button secondary" onclick="claraOnboarding.goToDetails()">
                        <i class="fas fa-edit"></i>
                        Edit Details
                    </button>
                </div>
            </div>
        `;
    }

    // Show specific page
    showPage(pageId) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });

        // Show target page
        const targetPage = document.getElementById(pageId);
        if (targetPage) {
            targetPage.classList.add('active');
        }

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Update progress bar for review page
    updateReviewProgressBar() {
        const steps = document.querySelectorAll('#review-page .progress-step-vertical');
        steps[0].classList.add('completed');
        steps[1].classList.add('completed');
        steps[2].classList.add('completed');
        steps[3].classList.add('active');
    }

    // Populate review summary
    populateReview() {
        // Company Information
        document.getElementById('review-company').textContent = this.formData.companyName || '';
        document.getElementById('review-address').textContent = this.formData.officeAddress || '';
        
        // Knowledge Base Websites
        const websites = this.getWebsiteUrls();
        document.getElementById('review-websites').textContent = websites.length > 0 ? websites.join(', ') : 'None';
        
        // Uploaded Documents
        document.getElementById('review-documents').textContent = this.uploadedFiles.length > 0 ? 
            this.uploadedFiles.map(f => f.name).join(', ') : 'None';
        
        document.getElementById('review-assistant').textContent = this.formData.assistantName || 'Clara';
        
        // Business Details
        document.getElementById('review-timezone').textContent = this.formData.timeZone ? `${this.formData.timeZone} Time` : '';
        
        // Business Days and Hours
        const businessDays = this.getSelectedBusinessDays();
        document.getElementById('review-business-days').textContent = businessDays.join(', ');
        
        const startTime = document.getElementById('startTime').value;
        const endTime = document.getElementById('endTime').value;
        document.getElementById('review-hours').textContent = `${this.formatTime(startTime)} - ${this.formatTime(endTime)}`;
        
        document.getElementById('review-phone').textContent = this.formData.contactNumber || '';
        
        // Post-Call Summary Options
        const emailEnabled = document.getElementById('postCallSummaryEmail').checked;
        const smsEnabled = document.getElementById('postCallSummarySMS').checked;
        
        document.getElementById('review-email-enabled').textContent = emailEnabled ? 'Yes' : 'No';
        document.getElementById('review-sms-enabled').textContent = smsEnabled ? 'Yes' : 'No';
        
        // Email details
        const primaryEmailItem = document.getElementById('review-primary-email-item');
        const ccEmailsItem = document.getElementById('review-cc-emails-item');
        
        if (emailEnabled) {
            const primaryEmail = document.getElementById('primaryEmail').value;
            document.getElementById('review-primary-email').textContent = primaryEmail;
            primaryEmailItem.style.display = 'flex';
            
            const ccEmails = this.getCCEmails();
            if (ccEmails.length > 0) {
                document.getElementById('review-cc-emails').textContent = ccEmails.join(', ');
                ccEmailsItem.style.display = 'flex';
            } else {
                ccEmailsItem.style.display = 'none';
            }
        } else {
            primaryEmailItem.style.display = 'none';
            ccEmailsItem.style.display = 'none';
        }
        
        // SMS details
        const smsNumbersItem = document.getElementById('review-sms-numbers-item');
        
        if (smsEnabled) {
            const smsNumbers = this.getSMSNumbers();
            document.getElementById('review-sms-numbers').textContent = smsNumbers.join(', ');
            smsNumbersItem.style.display = 'flex';
        } else {
            smsNumbersItem.style.display = 'none';
        }
    }

    // Helper functions for data collection
    getWebsiteUrls() {
        const websiteInputs = document.querySelectorAll('.website-input');
        const urls = [];
        websiteInputs.forEach(input => {
            if (input.value.trim()) {
                urls.push(input.value.trim());
            }
        });
        return urls;
    }

    getSelectedBusinessDays() {
        const dayCheckboxes = document.querySelectorAll('input[name="businessDays"]:checked');
        const days = [];
        dayCheckboxes.forEach(checkbox => {
            days.push(checkbox.nextElementSibling.textContent);
        });
        return days;
    }

    getCCEmails() {
        const ccInputs = document.querySelectorAll('.cc-email-input');
        const emails = [];
        ccInputs.forEach(input => {
            if (input.value.trim()) {
                emails.push(input.value.trim());
            }
        });
        return emails;
    }

    getSMSNumbers() {
        const smsInputs = document.querySelectorAll('.sms-input');
        const numbers = [];
        smsInputs.forEach(input => {
            if (input.value.trim()) {
                numbers.push(input.value.trim());
            }
        });
        return numbers;
    }

    formatTime(timeString) {
        if (!timeString) return '';
        const [hours, minutes] = timeString.split(':');
        const hour = parseInt(hours);
        const ampm = hour >= 12 ? 'PM' : 'AM';
        const displayHour = hour % 12 || 12;
        return `${displayHour}:${minutes} ${ampm}`;
    }

    // Get display name for timezone
    getTimeZoneDisplay(timezone) {
        const timezoneMap = {
            'Chicago': 'Chicago (Central Time)',
            'New_York': 'New York (Eastern Time)',
            'Denver': 'Denver (Mountain Time)',
            'Los_Angeles': 'Los Angeles (Pacific Time)'
        };
        return timezoneMap[timezone] || timezone;
    }

    // Copy text to clipboard
    copyToClipboard(elementId) {
        const element = document.getElementById(elementId);
        const text = element.textContent.trim();
        
        // Debug: Log what's being copied
        console.log(`Copying ${elementId}:`, text);
        
        navigator.clipboard.writeText(text).then(() => {
            // Show feedback
            const button = element.nextElementSibling;
            const originalIcon = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check"></i>';
            button.style.background = '#28a745';
            
            setTimeout(() => {
                button.innerHTML = originalIcon;
                button.style.background = '';
            }, 2000);
        }).catch(() => {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
        });
    }

    // Test call functionality
    testCall() {
        const phone = document.getElementById('clara-phone').textContent;
        window.open(`tel:${phone}`, '_self');
    }

    // Start loading animations and quotes
    startLoadingAnimation() {
        // Start quote rotation (slower pace)
        this.quoteInterval = setInterval(() => {
            this.rotateQuote();
        }, 6000); // Increased from 4000ms to 6000ms for slower pace
    }

    // Rotate funny quotes
    rotateQuote() {
        const quotes = document.querySelectorAll('.quote');
        quotes[this.currentQuote].classList.remove('active');
        
        this.currentQuote = (this.currentQuote + 1) % this.quotes.length;
        quotes[this.currentQuote].classList.add('active');
    }

    // Website management functions
    addWebsite() {
        if (this.websiteCount >= 3) return;
        
        const websiteInputs = document.getElementById('websiteInputs');
        const addBtn = document.getElementById('addWebsiteBtn');
        
        const websiteGroup = document.createElement('div');
        websiteGroup.className = 'website-input-group';
        websiteGroup.innerHTML = `
            <input type="url" class="website-input" placeholder="https://yourwebsite.com" data-index="${this.websiteCount}">
            <button type="button" class="remove-website-btn" onclick="removeWebsite(${this.websiteCount})">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        websiteInputs.appendChild(websiteGroup);
        this.websiteCount++;
        
        if (this.websiteCount >= 3) {
            addBtn.disabled = true;
            addBtn.style.opacity = '0.5';
        }
        
        // Show remove button for first website if there are now multiple
        if (this.websiteCount > 1) {
            const firstRemoveBtn = websiteInputs.querySelector('.remove-website-btn');
            if (firstRemoveBtn) {
                firstRemoveBtn.style.display = 'flex';
            }
        }
    }

    removeWebsite(index) {
        const websiteInputs = document.getElementById('websiteInputs');
        const addBtn = document.getElementById('addWebsiteBtn');
        const websiteGroups = websiteInputs.querySelectorAll('.website-input-group');
        
        // Find and remove the specific website group
        websiteGroups.forEach(group => {
            const input = group.querySelector('.website-input');
            if (input && input.dataset.index == index) {
                group.remove();
                this.websiteCount--;
            }
        });
        
        // Re-enable add button if under limit
        if (this.websiteCount < 3) {
            addBtn.disabled = false;
            addBtn.style.opacity = '1';
        }
        
        // Hide remove button for first website if only one remains
        if (this.websiteCount <= 1) {
            const firstRemoveBtn = websiteInputs.querySelector('.remove-website-btn');
            if (firstRemoveBtn) {
                firstRemoveBtn.style.display = 'none';
            }
        }
    }

    // CC Email management functions
    addCCEmail() {
        const ccContainer = document.getElementById('ccEmailsContainer');
        
        const ccGroup = document.createElement('div');
        ccGroup.className = 'cc-email-group';
        ccGroup.innerHTML = `
            <input type="email" class="cc-email-input" placeholder="cc@email.com" data-index="${this.ccEmailCount}">
            <button type="button" class="remove-cc-btn" onclick="removeCCEmail(${this.ccEmailCount})">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        ccContainer.appendChild(ccGroup);
        this.ccEmailCount++;
    }

    removeCCEmail(index) {
        const ccContainer = document.getElementById('ccEmailsContainer');
        const ccGroups = ccContainer.querySelectorAll('.cc-email-group');
        
        ccGroups.forEach(group => {
            const input = group.querySelector('.cc-email-input');
            if (input && input.dataset.index == index) {
                group.remove();
            }
        });
    }

    clearCCEmails() {
        const ccContainer = document.getElementById('ccEmailsContainer');
        ccContainer.innerHTML = '';
        this.ccEmailCount = 0;
    }

    // SMS Number management functions
    addSMSNumber() {
        const smsContainer = document.getElementById('smsNumbersContainer');
        const pricingNote = document.getElementById('smsPricingNote');
        
        const smsGroup = document.createElement('div');
        smsGroup.className = 'additional-sms-group';
        smsGroup.innerHTML = `
            <input type="tel" class="sms-input" placeholder="e.g., (555) 123-4567" data-index="${this.smsNumberCount}">
            <button type="button" class="remove-sms-btn" onclick="removeSMSNumber(${this.smsNumberCount})">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        smsContainer.appendChild(smsGroup);
        this.smsNumberCount++;
        
        // Show pricing note for additional numbers
        if (this.smsNumberCount > 1) {
            pricingNote.style.display = 'flex';
        }
    }

    removeSMSNumber(index) {
        const smsContainer = document.getElementById('smsNumbersContainer');
        const pricingNote = document.getElementById('smsPricingNote');
        const smsGroups = smsContainer.querySelectorAll('.additional-sms-group');
        
        smsGroups.forEach(group => {
            const input = group.querySelector('.sms-input');
            if (input && input.dataset.index == index) {
                group.remove();
                this.smsNumberCount--;
            }
        });
        
        // Hide pricing note if only primary number remains
        if (this.smsNumberCount <= 1) {
            pricingNote.style.display = 'none';
        }
    }

    clearAdditionalSMSNumbers() {
        const smsContainer = document.getElementById('smsNumbersContainer');
        const additionalGroups = smsContainer.querySelectorAll('.additional-sms-group');
        additionalGroups.forEach(group => group.remove());
        
        const pricingNote = document.getElementById('smsPricingNote');
        pricingNote.style.display = 'none';
        
        this.smsNumberCount = 1;
    }

    // Animate page transitions
    animatePageTransition() {
        // Add any additional transition animations here
        document.body.style.overflow = 'hidden';
        setTimeout(() => {
            document.body.style.overflow = 'auto';
        }, 500);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('📄 DOM Content Loaded');
    
    // Check if CSS is loaded by testing a known class
    const testElement = document.querySelector('.clara-header');
    if (testElement) {
        const styles = window.getComputedStyle(testElement);
        console.log('🎨 CSS Status - Header element found, computed styles:', {
            display: styles.display,
            background: styles.backgroundColor
        });
    } else {
        console.warn('⚠️ CSS Issue - Header element not found or styles not applied');
    }
    
    // Initialize Clara Onboarding
    try {
        window.claraOnboarding = new ClaraOnboarding();
        console.log('✅ Clara Onboarding instance created successfully');
    } catch (error) {
        console.error('❌ Error creating Clara Onboarding instance:', error);
    }
});

// Fallback initialization if DOMContentLoaded already fired
if (document.readyState === 'loading') {
    console.log('📋 Document still loading, waiting for DOMContentLoaded...');
} else {
    console.log('📋 Document already loaded, initializing immediately...');
    const claraOnboarding = new ClaraOnboarding();
}

// Global functions for HTML onclick handlers
function startOnboarding() {
    claraOnboarding.startOnboarding();
}

function nextSection() {
    claraOnboarding.nextSection();
}

function previousSection() {
    claraOnboarding.previousSection();
}

function goToDetails() {
    claraOnboarding.goToDetails();
}

function confirmDetails() {
    claraOnboarding.confirmDetails();
}

function copyToClipboard(elementId) {
    claraOnboarding.copyToClipboard(elementId);
}

function testCall() {
    claraOnboarding.testCall();
}

// Website management functions
function addWebsite() {
    claraOnboarding.addWebsite();
}

function removeWebsite(index) {
    claraOnboarding.removeWebsite(index);
}

// CC Email management functions
function addCCEmail() {
    claraOnboarding.addCCEmail();
}

function removeCCEmail(index) {
    claraOnboarding.removeCCEmail(index);
}

// SMS Number management functions
function addSMSNumber() {
    claraOnboarding.addSMSNumber();
}

function removeSMSNumber(index) {
    claraOnboarding.removeSMSNumber(index);
}

// Contact Modal functions
function openContactModal() {
    const modal = document.getElementById('contactModal');
    const backdrop = document.getElementById('modalBackdrop');
    
    modal.classList.add('active');
    backdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeContactModal() {
    const modal = document.getElementById('contactModal');
    const backdrop = document.getElementById('modalBackdrop');
    
    modal.classList.remove('active');
    backdrop.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Add CSS for error states and animations
const additionalStyles = `
    .error {
        border-color: #dc3545 !important;
        box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1) !important;
    }
    
    .field-error {
        color: #dc3545;
        font-size: 0.875rem;
        margin-top: 0.5rem;
        display: none;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .form-card {
        transition: transform 0.3s ease;
    }
    
    .form-group input:focus,
    .form-group select:focus {
        transform: translateY(-1px);
    }
    
    .troubleshooting-tips {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: left;
    }
    
    .troubleshooting-tips h4 {
        color: #495057;
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .troubleshooting-tips ul {
        margin: 0;
        padding-left: 1.2rem;
        color: #6c757d;
    }
    
    .troubleshooting-tips li {
        margin-bottom: 0.3rem;
        font-size: 0.85rem;
        line-height: 1.4;
    }
    
    .error-actions {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-top: 1.5rem;
        flex-wrap: wrap;
    }
    
    .error-actions .nav-button.secondary {
        background: #6c757d;
        border-color: #6c757d;
    }
    
    .error-actions .nav-button.secondary:hover {
        background: #5a6268;
        border-color: #545b62;
    }
    
    .error-content {
        max-width: 500px;
        margin: 0 auto;
    }
    
    .error-message {
        color: #dc3545;
        font-weight: 500;
        margin-bottom: 1rem;
    }
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);
document.addEventListener('DOMContentLoaded', function() {
    const inputCode = document.getElementById('input-code');
    const output = document.getElementById('output');
    const console = document.getElementById('console');
    const executeButton = document.getElementById('execute-button');
    const lineNumbers = document.querySelector('.line-numbers');
    const codeInput = document.querySelector('.code-input');

    // Function to update line numbers
    function updateLineNumbers() {
        const lines = inputCode.textContent.split('\n').length;
        lineNumbers.innerHTML = Array.from({ length: lines }, (_, i) => i + 1).join('\n');
    }

    function syncScroll() {
        lineNumbers.scrollTop = codeInput.scrollTop;
    }

    // Initialize line numbers on load
    updateLineNumbers();

    inputCode.addEventListener('scroll', syncScroll);

    const observer = new MutationObserver(() => {
        updateLineNumbers();
        syncScroll();
    });

    observer.observe(codeInput, { childList: true, subtree: true });

    // Handle content input to update line numbers
    codeInput.addEventListener('input', function() {
        updateLineNumbers();
    });

    // Sync the scroll positions when the code input is scrolled
    codeInput.addEventListener('scroll', syncScroll);

    // Debounce function for live error checking
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Function to log to console
    function logToConsole(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.className = `console-${type}`;
        logEntry.textContent = `[${timestamp}] ${message}`;
        
        console.insertBefore(logEntry, console.firstChild);
        
        // Keep only the last 100 messages
        while (console.children.length > 100) {
            console.removeChild(console.lastChild);
        }
    }

    // Function to check code for errors
    async function checkCode() {
        const code = inputCode.textContent;
        
        if (!code.trim()) {
            console.innerHTML = ''; // Clear console if no code
            return;
        }

        try {
            const response = await fetch('/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    code: code,
                    check_only: true
                })
            });
            
            const data = await response.json();
            
            // Clear previous error messages
            console.innerHTML = '';
            
            if (data.error) {
                logToConsole(data.error, 'error');
            }
        } catch (error) {
            logToConsole('Error checking code', 'error');
        }
    }

    // Function to execute code
    async function executeCode() {
        const code = inputCode.textContent;
        
        // Clear previous output
        output.textContent = '';
        
        if (!code.trim()) {
            logToConsole('No code to execute', 'error');
            return;
        }

        logToConsole('Executing code...', 'info');
        
        try {
            const response = await fetch('/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    code: code,
                    check_only: false
                })
            });
            
            const data = await response.json();
            
            if (data.error) {
                logToConsole(data.error, 'error');
            } else {
                output.textContent = data.output;
                logToConsole('Code executed successfully', 'success');
                
                if (data.python_code) {
                    logToConsole(`Translated to Python: ${data.python_code}`, 'info');
                }
            }
        } catch (error) {
            logToConsole('Error connecting to server', 'error');
        }
    }

    // Handle tab key and maintain indentation on new lines
    inputCode.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            e.preventDefault();
            const selection = window.getSelection();
            const range = selection.getRangeAt(0);
            const tabNode = document.createTextNode('    ');
            range.insertNode(tabNode);
            
            // Move cursor after the tab
            range.setStartAfter(tabNode);
            range.setEndAfter(tabNode);
            selection.removeAllRanges();
            selection.addRange(range);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            
            // Get the current line's text before the cursor
            const selection = window.getSelection();
            const range = selection.getRangeAt(0);
            const currentLine = range.startContainer.textContent;
            const cursorPosition = range.startOffset;
            const textBeforeCursor = currentLine.substring(0, cursorPosition);
            
            // Calculate indentation of the current line
            const match = textBeforeCursor.match(/^\s*/);
            const indentation = match ? match[0] : '';
            
            // Insert newline with indentation
            const newlineNode = document.createTextNode('\n' + indentation);
            range.deleteContents(); // Remove the current selection (if any)
            range.insertNode(newlineNode);
            
            // Move cursor to the start of the new line
            range.setStartAfter(newlineNode);
            range.setEndAfter(newlineNode);
            selection.removeAllRanges();
            selection.addRange(range);
            
            // Update line numbers
            updateLineNumbers();
        }
    });

    // Update line numbers when content changes
    inputCode.addEventListener('input', function() {
        updateLineNumbers();
        debouncedCheck();
    });

    // Create debounced version of checkCode
    const debouncedCheck = debounce(checkCode, 500);

    // Add input event listener for live error checking
    inputCode.addEventListener('input', debouncedCheck);

    // Add execute button click handler
    executeButton.addEventListener('click', executeCode);

    // Add Ctrl+Enter / Cmd+Enter keyboard shortcut
    inputCode.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            executeCode();
        }
    });

    // Initial console message
    logToConsole('Gyatt Compiler ready', 'success');
});
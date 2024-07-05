function copyCode() {
    const codeBox = document.getElementById('codeBox');
    const textArea = document.createElement('textarea');
    textArea.value = codeBox.textContent;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
    alert("Copied to clipboard!");
}  
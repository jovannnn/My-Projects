document.getElementById('uploadImage').addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profileImage').src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
});

function downloadPDF() {
    const cv = document.getElementById('cv');
    const opt = {
        margin:       0.5,
        filename:     'cv.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2 },
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
    };

    const uploadButton = document.querySelector('.profilnaslika input');
    const saveButton = document.querySelector('button');
    uploadButton.style.display = 'none';
    saveButton.style.display = 'none';

    html2pdf().from(cv).set(opt).save().then(() => {
        uploadButton.style.display = 'block';
        saveButton.style.display = 'block';
    });
}

(function() {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.9.2/html2pdf.bundle.min.js';
    document.head.appendChild(script);
})();




let invoiceVisible = true;

function toggleView() {
      const invoice = document.getElementById('invoice');
      const wrapper = invoice.closest('.page-wrapper');
      const btnText = document.getElementById('view-btn-text');

      if (invoiceVisible) {
        wrapper.style.display = 'none';
        btnText.textContent = 'View';
        invoiceVisible = false;
      } else {
        wrapper.style.display = 'flex';
        btnText.textContent = 'Hide';
        invoiceVisible = true;
      }
    }

function downloadPDF() {
  const invoice = document.getElementById('invoice');

  const options = {
    margin:       10,
    filename:     'Quote_QU240322_FKT_LIMITED.pdf',
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { scale: 2, useCORS: true },
    jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
  };

  html2pdf().set(options).from(invoice).save();
}
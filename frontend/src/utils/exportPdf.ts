import jsPDF from 'jspdf';

export const exportPdf = ({
  topics,
  images = [],
}: {
  topics: string[];
  images: string[]; // Array of base64 images to include in the PDF
}) => {
  const pdf = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4',
  });

  const pageWidth = pdf.internal.pageSize.getWidth();
  const margin = 10;
  let y = 20;

  // Add title for the report
  pdf.setFontSize(18);
  pdf.text('Custom Exchange Rate Report', margin, y);
  y += 15;

  // Add image if provided (this will be the first page image)
  if (images.length > 0) {
    pdf.addImage(images[0], 'PNG', margin, y, pageWidth - 2 * margin, 100);
    y += 105; // Add some space after the image
  }

  // Loop through each topic and add it to the PDF
  topics.forEach((topic, idx) => {
    if (idx !== 0) pdf.addPage(); // Add new page for each topic
    pdf.setFontSize(16);
    pdf.text(topic, margin, y);
    y += 10;

    // Add placeholder content (replace with actual content)
    pdf.setFontSize(12);
    pdf.text(`(Placeholder content for "${topic}")`, margin, y);
    y += 20;
  });

  // Save the PDF
  pdf.save('exchange-rate-report.pdf');
};

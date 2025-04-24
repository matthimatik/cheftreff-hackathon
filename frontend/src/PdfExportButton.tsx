import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

interface Props {
  chartId: string; // the DOM ID of the chart container
  rawData: Record<string, number>;
}

export const PdfExportButton: React.FC<Props> = ({ chartId, rawData }) => {
  const handleExport = async () => {
    const input = document.getElementById(chartId);

    if (!input) return alert('Chart not found');

    const canvas = await html2canvas(input, {
      scale: 2, // High-res
      useCORS: true,
    });

    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4',
    });

    const pageWidth = pdf.internal.pageSize.getWidth();
    const chartHeight = 100;

    pdf.setFontSize(18);
    pdf.text('Exchange Rate Report (SYP)', 10, 20);

    pdf.addImage(imgData, 'PNG', 10, 30, pageWidth - 20, chartHeight);

    pdf.setFontSize(12);
    pdf.text('Daily Aggregated Exchange Rates:', 10, 140);

    const sortedData = Object.entries(rawData).sort(([a], [b]) =>
      new Date(a).getTime() - new Date(b).getTime()
    );

    let y = 150;
    sortedData.forEach(([date, value]) => {
      if (y > 280) {
        pdf.addPage();
        y = 20;
      }
      pdf.text(`${date}: ${value}`, 10, y);
      y += 6;
    });

    pdf.save('exchange-rate-report.pdf');
  };

  return (
    <button
      onClick={handleExport}
      className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
    >
      Export PDF
    </button>
  );
};

import React, { useEffect, useState } from 'react';
import { ActionButton } from '@/ActionButton';
import { exportPdf } from '../utils/exportPdf';

// Define the list of possible topics
const ALL_TOPICS = [
  'HIGHLIGHTS',
  'Economic Updates',
  'Daily wage',
  'Global food prices and inflation trends',
  'Minimum Expenditure Basket (MEB)',
  'Retail prices for key commodities',
  'Exchange rate',
  'Energy prices',
  'Retail prices for MEB food components',
  'Retail prices for MEB non-food components',
  'Map: Population density and MEB Mapping',
];

const Report: React.FC = () => {
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);

  const url = window.location.href;
  const countryName = url.split('/').pop();

  // Toggle selected topics
  const toggleTopic = (topic: string) => {
    setSelectedTopics((prev) =>
      prev.includes(topic) ? prev.filter((t) => t !== topic) : [...prev, topic]
    );
  };

  // Dummy image data (replace with actual base64 images if necessary)
  const images: string[] = [];

  const handleCreateReportTapped = () => {
    const sendData = async () => {
        const body = JSON.stringify({
            country: countryName,
            selected_topics: selectedTopics,
            });

        console.log('Sending data to backend:', body);

      const response = await fetch('http://localhost:8000/report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: body
      });

      if (!response.ok) {
        console.error('Failed to generate report:', await response.text());
        return;
      }

      const data = await response.json();
      console.log('Response from backend:', data);

      // parse html response from backend and show
        const parser = new DOMParser();
        const doc = parser.parseFromString(data.result, 'text/html');
        const pdfPreview = document.getElementById('pdf-preview');
        if (pdfPreview) {
          pdfPreview.innerHTML = ''; // Clear previous content
          pdfPreview.appendChild(doc.documentElement);
        }
        console.log('Parsed HTML:', doc.documentElement);
    };
    sendData();
    // Export the PDF with selected topics and images
    /*exportPdf({
      topics: selectedTopics,
      images,
    });*/ 
    };

  /*useEffect(() => {
    console.log('Country Name:', countryName);

    // send country name to backend
    const sendData = async () => {
        const response = await fetch('http://localhost:8000/countries', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({ country_name: countryName }),
        });
    
        const data = await response.json();
        console.log('Response from backend:', data);
        }

    sendData();
  }, []);*/

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Building Report for: {countryName}</h2>

      <div className="space-y-2">
        {ALL_TOPICS.map((topic) => (
          <label key={topic} className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={selectedTopics.includes(topic)}
              onChange={() => toggleTopic(topic)}
              className="accent-blue-600"
            />
            <span>{topic}</span>
          </label>
        ))}
      </div>

      <div>
        <h3 className="font-medium mt-4 mb-2">Preview</h3>
        <div id="pdf-preview" className="border p-4 rounded bg-white shadow">
          {selectedTopics.map((topic) => (
            <div key={topic} className="mb-6">
              <h4 className="text-lg font-bold text-blue-600">{topic}</h4>
              <p className="text-sm text-gray-600">
                (Sample content placeholder for "{topic}")
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* ActionButton to trigger PDF export */}
      <ActionButton
        label="Export Report as PDF"
        onClick={handleCreateReportTapped}
      />
    </div>
  );
};

export default Report;

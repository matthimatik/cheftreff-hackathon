import React, { useState } from 'react';
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

  // Toggle selected topics
  const toggleTopic = (topic: string) => {
    setSelectedTopics((prev) =>
      prev.includes(topic) ? prev.filter((t) => t !== topic) : [...prev, topic]
    );
  };

  // Dummy image data (replace with actual base64 images if necessary)
  const images: string[] = [];

  // Handle exporting PDF when button is clicked
  const handleExport = () => {
    exportPdf({ topics: selectedTopics, images });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Build Your Report</h2>

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
        onClick={handleExport}
      />
    </div>
  );
};

export default Report;

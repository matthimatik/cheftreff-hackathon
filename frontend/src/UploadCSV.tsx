import React, { useState } from 'react';
import { parseAndAggregateCSV, AggregatedResult } from './utils/parseCsv';
import { Card, CardContent } from '@/components/ui/card';
import { ExchangeRateChart } from './ExchangeRateChart';
import { PdfExportButton } from './PdfExportButton';

const UploadCsv: React.FC = () => {
  const [data, setData] = useState<AggregatedResult | null>(null);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const result = await parseAndAggregateCSV(file);
      setData(result);
    } catch (err) {
      console.error('Failed to parse CSV:', err);
    }
  };

  return (
    <Card className="p-4 space-y-6">
      <CardContent>
        <input type="file" accept=".csv" onChange={handleUpload} />
        {data && (
          <>
            <div id="chart-to-export">
              <ExchangeRateChart data={data} />
            </div>
            <PdfExportButton chartId="chart-to-export" rawData={data} />
          </>
        )}
      </CardContent>
    </Card>
  );
};

export default UploadCsv;

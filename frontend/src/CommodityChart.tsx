// components/CommodityCharts.tsx
import React, { useEffect, useState } from 'react';
import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend, ResponsiveContainer
} from 'recharts';
import { parseAndGroupCommodityCsv } from './utils/parseCsv';

interface Props {
  data: string;
}

const CommodityCharts: React.FC<Props> = ({ data }) => {
  const [groupedData, setGroupedData] = useState<Record<string, { date: string; price: number }[]>>({});

  useEffect(() => {
    const grouped = parseAndGroupCommodityCsv(data);
    setGroupedData(grouped);
  }, []);

  return (
    <div className="space-y-8">
      {Object.entries(groupedData).map(([commodity, data]) => (
        <div key={commodity} className="w-full h-[400px]">
          <h3 className="text-lg font-medium mb-2">{commodity}</h3>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="price" stroke="#8884d8" name={`${commodity} Price`} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      ))}
    </div>
  );
};

export default CommodityCharts;
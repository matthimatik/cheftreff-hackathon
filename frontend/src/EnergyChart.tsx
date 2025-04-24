// components/EnergyChart.tsx
import {
    LineChart, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid, ResponsiveContainer,
  } from 'recharts';
  
  interface Props {
    // dataA: { date: string; price: number }[];
    // dataB: { date: string; price: number }[];
    dataA: string;
    dataB: string;
    labelA: string;
    labelB: string;
  }
  
  const EnergyChart: React.FC<Props> = ({ dataA, dataB, labelA, labelB }) => {
    console.log('Data A:', dataA);
    const dataAParsed = dataA.split('\n').slice(1).map(line => {
        const [_ , date, price] = line.split(',');
        return { date, price: parseFloat(price) };
    });
    const dataBParsed = dataB.split('\n').slice(1).map(line => {
        const [_ , date, price] = line.split(',');
        return { date, price: parseFloat(price) };
    });

    const mergedData = [...dataAParsed, ...dataBParsed]
      .reduce((acc, entry) => {
        const found = acc.find(d => d.date === entry.date);
        if (!found) acc.push({ date: entry.date, [labelA]: null, [labelB]: null });
        return acc;
      }, [] as any[])
      .map(d => {
        const matchA = dataAParsed.find(e => e.date === d.date);
        const matchB = dataBParsed.find(e => e.date === d.date);
        return {
          date: d.date,
          [labelA]: matchA?.price ?? null,
          [labelB]: matchB?.price ?? null,
        };
      });
  
    return (
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={mergedData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey={labelA} stroke="#8884d8" />
          <Line type="monotone" dataKey={labelB} stroke="#82ca9d" />
        </LineChart>
      </ResponsiveContainer>
    );
  };
  
  export default EnergyChart;
  
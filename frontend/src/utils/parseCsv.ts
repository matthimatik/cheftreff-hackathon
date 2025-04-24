import Papa from 'papaparse';
import { parse, isAfter, subMonths } from 'date-fns';

export interface CsvRow {
  Date: string;   // e.g., "5/03/2024"
  Value: string;  // e.g., "14250"
  [key: string]: string; // possible other columns (e.g., Market)
}

export interface AggregatedResult {
  [date: string]: number; // date in YYYY-MM-DD -> averaged value
}

export const parseAndAggregateCSV = (
  file: File
): Promise<AggregatedResult> => {
  return new Promise((resolve, reject) => {
    Papa.parse<CsvRow>(file, {
      header: true,
      skipEmptyLines: true,
      complete: (results: { data: any; }) => {
        const now = new Date();
        const twelveMonthsAgo = subMonths(now, 12);
        const data = results.data;

        const aggregatedMap: Record<string, number[]> = {};

        data.forEach((row) => {
          const parsedDate = parse(row.Date, 'd/MM/yyyy', new Date());

          if (isAfter(parsedDate, twelveMonthsAgo)) {
            const dateKey = parsedDate.toISOString().split('T')[0]; // YYYY-MM-DD
            const value = parseFloat(row.Value);

            if (!isNaN(value)) {
              if (!aggregatedMap[dateKey]) {
                aggregatedMap[dateKey] = [];
              }
              aggregatedMap[dateKey].push(value);
            }
          }
        });

        const averaged: AggregatedResult = {};

        Object.entries(aggregatedMap).forEach(([date, values]) => {
          const sum = values.reduce((a, b) => a + b, 0);
          averaged[date] = parseFloat((sum / values.length).toFixed(2));
        });

        resolve(averaged);
      },
      error: (err) => reject(err),
    });
  });
};

export interface CommodityEntry {
  Commodity: string;
  'Price Date': string;
  Price: number;
}

export function parseAndGroupCommodityCsv(csvText: string): Record<string, { date: string; price: number }[]> {
  const parsed = Papa.parse(csvText, {
    header: true,
    skipEmptyLines: true,
  });

  const entries = (parsed.data as any[]).map(row => ({
    Commodity: row['Commodity'],
    'Price Date': row['Price Date'],
    Price: parseFloat(row['Price']),
  }));

  const grouped: Record<string, { date: string; price: number }[]> = {};

  for (const entry of entries) {
    const { Commodity, 'Price Date': date, Price: price } = entry;

    if (!grouped[Commodity]) {
      grouped[Commodity] = [];
    }

    grouped[Commodity].push({ date, price });
  }

  return grouped;
}
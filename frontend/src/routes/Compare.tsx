// pages/Compare.tsx
import React, { use, useEffect, useState } from 'react';
import CountrySelect from '../CountrySelect';
import EnergyChart from '../EnergyChart';
// import { parseEnergyCsv } from '../utils/parseEnergyCsv';

const Compare = () => {
  const [countries, setCountries] = useState<string[]>([]);
  const [selectedA, setSelectedA] = useState<string>('');
  const [selectedB, setSelectedB] = useState<string>('');
  const [filteredA, setFilteredA] = useState<string>('');
  const [filteredB, setFilteredB] = useState<string>('');
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    const fetchCountries = async () => {
        const response = await fetch('http://localhost:8000/countries');
        const data = await response.json();
    
        if (!response.ok) {
            console.error('Failed to fetch countries:', data);
            return;
        } else {
            setCountries(data.result.countries);
            // setSelectedA(data.result.countries[0]);
            // setSelectedB(data.result.countries[1] || data.result.countries[0]);
        }
    };
    fetchCountries();
    /*const fetchCsv = async () => {
      const res = await fetch('http://localhost:8000/energy-prices.csv');
      const text = await res.text();

      const parsed = parseEnergyCsv(text);
      setData(parsed);

      const countryList = Array.from(new Set(parsed.map(row => row.Country))).sort();

      setCountries(countryList);
      setSelectedA(countryList[0]);
      setSelectedB(countryList[1] || countryList[0]);
    };

    fetchCsv();*/
  }, []);

  // fetch data for country a when selectedA changes
  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(`http://localhost:8000/csv/${selectedA}/energy_prices`);
      
      const data = await response.text();

      if (!response.ok) {
          console.error('Failed to fetch data for country A:', data);
          return;
      } else {
          setFilteredA(data);
      }
    };

    if (selectedA) {
      fetchData();
    }
  }
    , [selectedA]);

    useEffect(() => {
        const fetchData = async () => {
          const response = await fetch(`http://localhost:8000/csv/${selectedB}/energy_prices`);
          // const data = await response.json();

          const data = await response.text();
    
          if (!response.ok) {
              console.error('Failed to fetch data for country A:', data);
              return;
          } else {
              setFilteredB(data);
          }
        };
        if (selectedB) {
          fetchData();
        }
      }
        , [selectedB]);


  /*const filteredA = data
    .filter(d => d.Country === selectedA)
    .map(d => ({ date: d.Date, price: d.EnergyPrice }));

  const filteredB = data
    .filter(d => d.Country === selectedB)
    .map(d => ({ date: d.Date, price: d.EnergyPrice }));*/


  return (
    <div className="p-6 space-y-6">
      <h2 className="text-2xl font-bold">Compare Energy Prices</h2>
      <div className="flex gap-4">
        <CountrySelect
          countries={countries}
          selected={selectedA}
          onChange={setSelectedA}
          label="Country A"
        />
        <CountrySelect
          countries={countries}
          selected={selectedB}
          onChange={setSelectedB}
          label="Country B"
        />
      </div>
      <EnergyChart
        dataA={filteredA}
        dataB={filteredB}
        labelA={selectedA}
        labelB={selectedB}
      />
    </div>
  );
};

export default Compare;

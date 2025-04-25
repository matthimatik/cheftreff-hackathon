import { ActionButton } from '@/ActionButton';
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// Country selection component
const CountrySelection: React.FC = () => {
  const [countries, setCountries] = useState<string[]>([]);
  const [selectedCountry, setSelectedCountry] = useState<string>('');
  const navigate = useNavigate();

  // Fetch countries from the FastAPI backend
  useEffect(() => {
    const fetchCountries = async () => {
      const response = await fetch('http://localhost:8000/countries');
      const data = await response.json();
        if (!response.ok) {
            console.error('Failed to fetch countries:', data);
            return;
        } else {
            setCountries(data.result.countries);
        }
    };

    fetchCountries();
  }, []);

  // Handle country selection
  const handleCountrySelect = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedCountry(event.target.value);
  };

  // Navigate to the report page
  const handleNextStep = () => {
    if (selectedCountry) {
      navigate(`/report/${selectedCountry}`);
    } else {
      alert('Please select a country');
    }
  };

  return (
    <div className="space-y-6 max-w-md mx-auto p-6 border rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold">Welcome to the Report Generator</h2>
      <p>Select the country for which you want to create the report:</p>

      <select
        value={selectedCountry}
        onChange={handleCountrySelect}
        className="w-full p-2 border rounded-md"
      >
        <option value="" disabled>Select a country</option>
        {countries.map((country, idx) => (
          <option key={idx} value={country}>{country}</option>
        ))}
      </select>

      <p>Select the Year and Month for the report:</p>
      <div className="flex space-x-4">
        <input type="number" placeholder="Year" className="w-1/2 p-2 border rounded-md" />
        <select
          className="w-full p-2 border rounded-md"
        >
          <option value="" disabled>Select Month</option>
          <option value="January">January</option>
          <option value="February">February</option>
          <option value="March">March</option>
          <option value="April">April</option>
          <option value="May">May</option>
          <option value="June">June</option>
          <option value="July">July</option>
          <option value="August">August</option>
          <option value="September">September</option>
          <option value="October">October</option>
          <option value="November">November</option>
          <option value="December">December</option>
        </select>
      </div>

      <ActionButton label="Create Report" onClick={handleNextStep} />
    </div>
  );
};

export default CountrySelection;

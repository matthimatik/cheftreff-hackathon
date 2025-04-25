import React, { useEffect, useState } from 'react';
import { ActionButton } from '@/ActionButton';
import { exportPdf } from '../utils/exportPdf';
import { useNavigate } from 'react-router-dom';
import { LineChartComponent } from '@/LineChart';
import { LineChart } from 'recharts';
import CommodityChart from '@/CommodityChart';
import CommodityCharts from '@/CommodityChart';
import { el } from 'date-fns/locale';
import { Button } from '@/components/ui/button';
import { Trash } from 'lucide-react';
import { Input } from '@/components/ui/input';

const ALL_TOPICS = {
    'HIGHLIGHTS': 'HIGHLIGHTS',
    'economic_updates': 'Economic Updates',
    'daily_wage': 'Daily wage',
    'global_food_prices_and_inflation_trends': 'Global food prices and inflation trends',
    'meb': 'Minimum Expenditure Basket (MEB)',
    'retail_prices_key_commodities': 'Retail prices for key commodities',
    'exchange_rate': 'Exchange rate',
    'energy_prices': 'Energy prices',
    'retail_meb_food': 'Retail prices for MEB food components',
    'retail_meb_non-food': 'Retail prices for MEB non-food components',
    'map': 'Map: Population density and MEB Mapping'
};

const Report: React.FC = () => {
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
  // state of csv files per topic
  const [csvFiles, setCsvFiles] = useState<{ [key: string]: string | undefined }>({});
  // is loading state
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);

  // const navigate = useNavigate();

  const url = window.location.href;
  const countryName = url.split('/').pop()?.replace(/%20/g, ' ');

  // set initial value for each csv mapping of selected topics to undefined
  useEffect(() => {
    const initialCsvFiles: { [key: string]: string | undefined } = {};
    Object.keys(ALL_TOPICS).forEach((topic) => {
      initialCsvFiles[topic] = undefined;
    });
    setCsvFiles(initialCsvFiles);
    }, []);

    // Fetch data from the backend and set it to the preview
    const fetchCSVData = async (topic: string) => {
        const response = await fetch(`http://localhost:8000/csv/${countryName}/${topic}`);
    // get response csv
        const data = await response.text();
        // console.log('CSV data:', data);

        // set csv file for the topic
        setCsvFiles((prev) => ({
            ...prev,
            [topic]: data
        }));

        // parse csv and show in preview
        /*const parser = new DOMParser();
        const doc = parser.parseFromString(data, 'text/html');
        const pdfPreview = document.getElementById('pdf-preview');
        if (pdfPreview) {
        pdfPreview.innerHTML = ''; // Clear previous content
        pdfPreview.appendChild(doc.documentElement);
        }
        console.log('Parsed HTML:', doc.documentElement);*/
    };


    /*useEffect(() => {
        // Fetch data from the backend and set it to the preview
        const fetchData = async () => {
            const response = await fetch(`http://localhost:8000/csv/${countryName}/${selectedTopics[0]}`);
        // get response csv
            const data = await response.text();
            console.log('CSV data:', data);

            // parse csv and show in preview
            const parser = new DOMParser();
            const doc = parser.parseFromString(data, 'text/html');
            const pdfPreview = document.getElementById('pdf-preview');
            if (pdfPreview) {
            pdfPreview.innerHTML = ''; // Clear previous content
            pdfPreview.appendChild(doc.documentElement);
            }
            console.log('Parsed HTML:', doc.documentElement);
        };

        if (selectedTopics.length > 0) {
            console.log('Selected topics:', selectedTopics);
            fetchData();
        }

    // Cleanup function to reset the preview when topics change
    return () => {
        const pdfPreview = document.getElementById('pdf-preview');
        if (pdfPreview) {
        pdfPreview.innerHTML = ''; // Clear previous content
        }
    };
    }, [selectedTopics]);*/

  // Toggle selected topics
  const toggleTopic = (topic: string) => {
    setSelectedTopics((prev) =>
      prev.includes(topic) ? prev.filter((t) => t !== topic) : [...prev, topic]
    );
    fetchCSVData(topic);
  };

  // Dummy image data (replace with actual base64 images if necessary)
  const images: string[] = [];

  const display_plot = (topic: string) => {
    // return line chart with csv data
    const csvData = csvFiles[topic];

    console.log('CSV data for topic:', topic, csvData);

    // change data from csv to json
    /*const jsonData = csvData?.split('\n').map((line) => {
      const [date, value] = line.split(',');
      return { date, value: parseFloat(value) };
    });

    console.log(jsonData);*/

    if (csvData) {
      // if topic == energy_prices, show commodity chart
        if (topic === 'energy_prices') {
            return (
                <CommodityCharts
                    data={csvData}
                />
            );
        } else if (topic === 'exchange_rate') {
            return (
                <CommodityCharts
                    data={csvData}
                />
            );
        }

        return (
            < div/>
      );
    }
  }

  const handleCreateReportTapped = () => {
    const sendData = async () => {
        setLoading(true);
        const body = JSON.stringify({
            country: countryName,
            selected_topics: selectedTopics,
            urls: urlList,
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
        // const parser = new DOMParser();
        // const doc = parser.parseFromString(data.result, 'text/html');
        setResult(data.result);
        setLoading(false);
        /* const pdfPreview = document.getElementById('pdf-preview');
        if (pdfPreview) {
          pdfPreview.innerHTML = ''; // Clear previous content
          pdfPreview.appendChild(doc.documentElement);
        }
        console.log('Parsed HTML:', doc.documentElement);*/
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

  const [newUrl, setNewUrl] = useState<string>('');
  const [urlList, setUrlList] = useState<string[]>([]);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setNewUrl(event.target.value);
  };

  const handleAddUrl = () => {
    if (newUrl.trim() !== '') {
      // Basic URL validation (you might want a more robust one)
      try {
        console.log('Adding URL:', newUrl);
        // add to url: https://
        new URL(newUrl + (newUrl.startsWith('http') ? '' : 'https://'));
        setUrlList([...urlList, newUrl]);
        setNewUrl('');
      } catch (error) {
        alert('Please enter a valid URL.');
      }
    }
  };

  const handleRemoveUrl = (index: number) => {
    const updatedList = urlList.filter((_, i) => i !== index);
    setUrlList(updatedList);
  };

  return (
    <>
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Building Report for: {countryName}</h2>

        { loading ? (
        <div className ="flex flex-col items-center justify-center h-full">
            <div className="flex items-center">
            <p className="text-lg font-semibold mr-4">
                Generating report... 
            </p>
            <p className="text-sm text-gray-500">
                This may take a few seconds (or minutes).
            </p>
            </div>
          <img src="/loading.gif" alt="Loading..." />
        </div>
        )
        :
        result ? (
          <div id="pdf-preview" className="border p-4 rounded bg-white shadow">
            <div dangerouslySetInnerHTML={{ __html: result }} />
          </div>
        ) :
      <>
      <>
      <div className="flex items-center mb-4">
        <Input
          type="url"
          placeholder="Add a datasource URL"
          value={newUrl}
          onChange={handleInputChange}
          className="mr-2"
        />
        <Button onClick={handleAddUrl}>Add URL</Button>
      </div>

      <p className="text-sm text-gray-500">
            Select the topics you want to include in the report:
      </p>

      {urlList.length > 0 && (
        <div className="mb-4">
          <h2 className="text-lg font-semibold mb-2">Trustworthy datasources: </h2>
          <ul className="border rounded-md">
            {urlList.map((url, index) => (
              <li
                key={index}
                className="px-4 py-2 border-b last:border-b-0 flex items-center justify-between"
              >
                <span className="truncate">{url}</span>
                <Button
                  variant="destructive"
                  size="icon"
                  onClick={() => handleRemoveUrl(index)}
                >
                  <Trash className="h-4 w-4 text-red-500" />
                </Button>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="space-y-2">
        {/* for each topic */}
        {Object.entries(ALL_TOPICS).map(([key, value]) => (
          <div key={key} className="flex items-center">
            <input
              type="checkbox"
              id={key}
              checked={selectedTopics.includes(key)}
              onChange={() => toggleTopic(key)}
              className="mr-2"
            />
            <label htmlFor={key} className="text-sm text-gray-700">
              {value}
            </label>
          </div>
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
              <div>
                {display_plot(topic)}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ActionButton to trigger PDF export */}
      <ActionButton
        label="🪄 Generate Report"
        onClick={handleCreateReportTapped}
      />
      </>
      </> }
    </div>
    </>
  );
};

export default Report;

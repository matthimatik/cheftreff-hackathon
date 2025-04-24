import { Button } from "@/components/ui/button"
import { LineChartComponent } from "./LineChart"
import UploadCsv from "./UploadCSV"
 
function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-svh">
      <UploadCsv />
      <Button>Create Report</Button>
    </div>
  )
}
 
export default App
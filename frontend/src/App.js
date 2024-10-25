import './App.css';


import AvgChart from "./components/AvgChart";
import AvgChartRange from "./components/AvgChartRange";
import AddMeasurement from "./components/AddMeasurement";
import MeasurementTable from "./components/MeasurementTable";

function App() {

  const url = "http://127.0.0.1:5000/api/allrows";

  return (
    <div>
      <div>
        <h1>hearttrace</h1>
        <AvgChartRange props={{url}}></AvgChartRange>
      </div>
      <AddMeasurement props={{url}}></AddMeasurement>
      <MeasurementTable props={{url}}></MeasurementTable>
    </div>

  );
}

export default App;

import { Sensor1 } from "./Sensores/Sensor1";
function App() {
  return (
    <div className="flex flex-col min-h-screen gap-y-2">
      <div className="bg-gradient-to-r from-red-500 to-purple-500 h-4"></div>
      <h1 className="text-4xl font-bold text-center my-4">Panel</h1>
      <h1 className="text-2xl text-right">Equipo 5</h1>
      <div className="w-full h-full grid place-items-center">
        <div className="container">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 my-2">
            <Sensor1 />
            <Sensor1 />
            <Sensor1 />
            <Sensor1 />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

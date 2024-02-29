import { useEffect, useState } from "react";
import { Card } from "../Card";

const path = "/ajax/1";

export function Sensor1() {
  const [value, setValue] = useState<string | undefined>(undefined);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<boolean>(false);

  const handle = () => {
    if (loading) {
      return;
    }
    setLoading(true);
    fetch(path)
      .then((res) => res.text())
      .then(setValue)
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    handle();
  }, []);

  return (
    <Card title="Sensor de tempreratura">
      <button
        className="bg-blue-600 active:bg-blue-700 text-white rounded-sm p-2"
        onClick={() => {
          if (loading) {
            return;
          }
          setError(false);
          setValue(undefined);
          setLoading(true);
          fetch(path)
            .then((res) => res.text())
            .then(setValue)
            .catch(() => setError(true))
            .finally(() => setLoading(false));
        }}
      >
        Actualizar valor
      </button>
      {loading && <p>Loading...</p>} {value && <p>Valor: {value} C°</p>}{" "}
      {error && (
        <p className="text-red-500">
          Sucedio un error al obtener la informacion
        </p>
      )}
    </Card>
  );
}

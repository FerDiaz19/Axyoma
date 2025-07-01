// src/App.tsx
import { useEffect, useState } from "react";
import { getItems } from "./api/items";

interface Item {
  id: number;
  name: string;
  quantity: number;
}

function App() {
  const [items, setItems] = useState<Item[]>([]);

  useEffect(() => {
    getItems().then(setItems);
  }, []);

  return (
    <div>
      <h1>Items</h1>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            {item.name} - {item.quantity}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;

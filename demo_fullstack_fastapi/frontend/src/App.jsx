import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [entries, setEntries] = useState([]);
  const [error, setError] = useState(null);
  const [newEntry, setNewEntry] = useState({ title: "", content: "", author_name: "" });
  const [updateEntry, setUpdateEntry] = useState({ id: "", title: "", content: "" });

  const API_URL = "http://localhost:8001/api/entries";

  // Fetch all entries
  useEffect(() => {
    fetch(API_URL)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Error fetching entries");
        }
        return response.json();
      })
      .then((data) => setEntries(data))
      .catch((error) => setError(error.message));
  }, []);

  // Create a new entry
  const handleCreateEntry = () => {
    fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newEntry),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Error creating entry");
        }
        return response.json();
      })
      .then((data) => setEntries((prev) => [...prev, data]))
      .catch((error) => setError(error.message));
  };

  // Update an entry
  const handleUpdateEntry = () => {
    fetch(`${API_URL}/${updateEntry.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: updateEntry.title, content: updateEntry.content }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Error updating entry");
        }
        return response.json();
      })
      .then((data) => {
        setEntries((prev) =>
          prev.map((entry) => (entry.id === data.id ? data : entry))
        );
      })
      .catch((error) => setError(error.message));
  };

  // Delete an entry
  const handleDeleteEntry = (id) => {
    fetch(`${API_URL}/${id}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Error deleting entry");
        }
        setEntries((prev) => prev.filter((entry) => entry.id !== id));
      })
      .catch((error) => setError(error.message));
  };

  return (
    <div>
      <h1>CRUD de Entries</h1>
      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      <h2>Lista de Entries</h2>
      <ul>
        {entries.length>0 && entries.map((entry) => (
          <li key={entry.id}>
            {entry.title}: {entry.content} {" "}
            <button onClick={() => handleDeleteEntry(entry.id)}>Eliminar</button>
          </li>
        ))}
      </ul>

      <h2>Crear Entry</h2>
      <input
        type="text"
        placeholder="Título"
        value={newEntry.title}
        onChange={(e) => setNewEntry({ ...newEntry, title: e.target.value })}
      />
      <input
        type="text"
        placeholder="Contenido"
        value={newEntry.content}
        onChange={(e) => setNewEntry({ ...newEntry, content: e.target.value })}
      />
      <input
        type="text"
        placeholder="Nombre del Autor"
        value={newEntry.author_name}
        onChange={(e) => setNewEntry({ ...newEntry, author_name: e.target.value })}
      />
      <button onClick={handleCreateEntry}>Crear</button>

      <h2>Actualizar Entry</h2>
      <input
        type="number"
        placeholder="ID"
        value={updateEntry.id}
        onChange={(e) => setUpdateEntry({ ...updateEntry, id: e.target.value })}
      />
      <input
        type="text"
        placeholder="Nuevo Título"
        value={updateEntry.title}
        onChange={(e) => setUpdateEntry({ ...updateEntry, title: e.target.value })}
      />
      <input
        type="text"
        placeholder="Nuevo Contenido"
        value={updateEntry.content}
        onChange={(e) => setUpdateEntry({ ...updateEntry, content: e.target.value })}
      />
      <button onClick={handleUpdateEntry}>Actualizar</button>
    </div>
  );
}

export default App;

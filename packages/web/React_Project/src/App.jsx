
import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [books, setBooks] = useState([]);

  const [form, setForm] = useState({
    title: "",
    author: "",
    genre: "",
    year: ""
  });

  const [editId, setEditId] = useState(null);
  const [message, setMessage] = useState("");

  // GET: Fetch all books
  async function getBooks() {
    try {
      const response = await fetch(`${API_URL}/books`);

      if (!response.ok) {
        throw new Error("Could not fetch books");
      }

      const data = await response.json();
      setBooks(data);
    } catch (error) {
      setMessage(error.message);
    }
  }

  // Fetch books when page loads
  useEffect(() => {
    getBooks();
  }, []);

  // Handle form input
  function handleChange(e) {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  }

  // POST: Add book
  // PUT: Update book
  async function handleSubmit(e) {
    e.preventDefault();

    const isEditing = editId !== null;

    const url = isEditing
      ? `${API_URL}/books/${editId}`
      : `${API_URL}/books`;

    const method = isEditing ? "PUT" : "POST";

    try {
      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          ...form,
          year: Number(form.year)
        })
      });

      if (!response.ok) {
        throw new Error("Operation failed");
      }

      setMessage(
        isEditing
          ? "Book updated successfully!"
          : "Book added successfully!"
      );

      resetForm();
      await getBooks();

    } catch (error) {
      setMessage(error.message);
    }
  }

  // Clear form
  function resetForm() {
    setForm({
      title: "",
      author: "",
      genre: "",
      year: ""
    });

    setEditId(null);
  }

  // Load book details for editing
  function handleEdit(book) {
    setEditId(book.id);

    setForm({
      title: book.title,
      author: book.author,
      genre: book.genre,
      year: String(book.year)
    });

    window.scrollTo(0, 0);
  }

  // DELETE: Remove book
  async function handleDelete(id) {
    if (!window.confirm("Are you sure you want to remove this book?")) {
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/books/${id}`,
        { method: "DELETE" }
      );

      if (!response.ok) {
        throw new Error("Could not delete book");
      }

      setMessage("Book removed successfully!");
      await getBooks();

    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div className="library">

      <header className="header">
        <div>
          <h1>📚 My Library</h1>
          <p>Manage your personal book collection</p>
        </div>

        <span className="book-count">
          {books.length} Books
        </span>
      </header>

      <section className="form-section">
        <h2>
          {editId !== null ? "Update Book" : "Add a New Book"}
        </h2>

        <form onSubmit={handleSubmit}>

          <input
            name="title"
            placeholder="Book Title"
            value={form.title}
            onChange={handleChange}
            required
          />

          <input
            name="author"
            placeholder="Author Name"
            value={form.author}
            onChange={handleChange}
            required
          />

          <input
            name="genre"
            placeholder="Genre"
            value={form.genre}
            onChange={handleChange}
            required
          />

          <input
            name="year"
            type="number"
            placeholder="Publication Year"
            min="1"
            value={form.year}
            onChange={handleChange}
            required
          />

          <button type="submit" className="primary-btn">
            {editId !== null ? "Update Book (PUT)" : "Add Book (POST)"}
          </button>

          {editId !== null && (
            <button
              type="button"
              onClick={resetForm}
              className="secondary-btn"
            >
              Cancel
            </button>
          )}

        </form>

        {message && <p className="message">{message}</p>}
      </section>

      <section className="books-section">

        <div className="section-heading">
          <h2>My Collection</h2>

          <button onClick={getBooks} className="secondary-btn">
            Refresh (GET)
          </button>
        </div>

        {books.length === 0 ? (
          <p>No books found. Add your first book!</p>
        ) : (

          <div className="books-grid">

            {books.map((book) => (
              <div className="book-card" key={book.id}>

                <div className="book-icon">📖</div>

                <h3>{book.title}</h3>

                <p>By {book.author}</p>

                <p>Genre: {book.genre}</p>

                <p>Published: {book.year}</p>

                <div className="actions">

                  <button
                    onClick={() => handleEdit(book)}
                    className="edit-btn"
                  >
                    Edit (PUT)
                  </button>

                  <button
                    onClick={() => handleDelete(book.id)}
                    className="delete-btn"
                  >
                    Remove (DELETE)
                  </button>

                </div>

              </div>
            ))}

          </div>
        )}

      </section>

    </div>
  );
}

export default App;

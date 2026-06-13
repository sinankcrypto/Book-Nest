import { useEffect, useState } from "react";

import MainLayout from "../layouts/MainLayout";

import BookCard from "../components/books/BookCard";

import { getBooks } from "../services/bookService";

const Home = () => {
  const [books, setBooks] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const data =
          await getBooks({
            ordering:
              "-created_at",
          });

        setBooks(
          data.results.slice(0, 6)
        );
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    };

    fetchBooks();
  }, []);

  return (
    <>
      <section className="bg-white rounded-2xl border border-gray-200 p-8">
        <h1 className="text-4xl font-bold text-gray-900">
          Discover Your Next Great Read
        </h1>

        <p className="mt-4 text-gray-600 max-w-2xl">
          Explore books uploaded by readers,
          organize them into reading lists,
          and build your own digital library.
        </p>
      </section>

      <section className="mt-10">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-semibold">
            Featured Books
          </h2>
        </div>

        {loading ? (
          <p>Loading...</p>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {books.map((book) => (
              <BookCard
                key={book.id}
                book={book}
              />
            ))}
          </div>
        )}
      </section>
    </>
      
  );

}

export default Home;
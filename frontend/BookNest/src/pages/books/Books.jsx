import {
  useEffect,
  useState,
} from "react";

import MainLayout from "../../layouts/MainLayout";

import BookCard from "../../components/books/BookCard";

import { getBooks } from "../../services/bookService";

const Books = () => {
  const [books, setBooks] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [search, setSearch] =
    useState("");

  const [page, setPage] =
    useState(1);

  const [nextPage, setNextPage] =
    useState(null);

  const [previousPage, setPreviousPage] =
    useState(null);

  const fetchBooks = async () => {
    try {
      setLoading(true);

      const data = await getBooks({
        search,
        page,
      });

      setBooks(data.results);

      setNextPage(data.next);

      setPreviousPage(
        data.previous
      );
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(
      () => {
        fetchBooks();
      },
      500
    );

    return () =>
      clearTimeout(timer);
  }, [search, page]);

  return (
      <div className="space-y-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Browse Books
          </h1>

          <p className="text-gray-500 mt-2">
            Discover books uploaded
            by the community.
          </p>
        </div>

        <div className="bg-white p-4 rounded-xl border border-gray-200">
          <input
            type="text"
            placeholder="Search by title, author or genre..."
            value={search}
            onChange={(e) => {
              setPage(1);
              setSearch(
                e.target.value
              );
            }}
            className="w-full px-3 py-2 rounded-lg border border-gray-300 outline-none focus:ring-2 focus:ring-yellow-400"
          />
        </div>

        {loading ? (
          <div className="text-center py-20">
            Loading books...
          </div>
        ) : books.length === 0 ? (
          <div className="bg-white rounded-xl border border-gray-200 p-10 text-center">
            No books found.
          </div>
        ) : (
          <>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
              {books.map((book) => (
                <BookCard
                  key={book.id}
                  book={book}
                />
              ))}
            </div>

            <div className="flex justify-center gap-4">
              <button
                disabled={!previousPage}
                onClick={() =>
                  setPage(
                    (prev) =>
                      prev - 1
                  )
                }
                className="px-4 py-2 rounded-lg border border-gray-300 disabled:opacity-50"
              >
                Previous
              </button>

              <span className="flex items-center font-medium">
                Page {page}
              </span>

              <button
                disabled={!nextPage}
                onClick={() =>
                  setPage(
                    (prev) =>
                      prev + 1
                  )
                }
                className="px-4 py-2 rounded-lg border border-gray-300 disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>
  );
};

export default Books;
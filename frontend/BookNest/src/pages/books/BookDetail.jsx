import {
  useEffect,
  useState,
} from "react";

import {
  useParams,
} from "react-router-dom";

import MainLayout from "../../layouts/MainLayout";

import { getBook } from "../../services/bookService";
import AddToReadingListModal from "../readingLists/AddToReadingListModal";

const BookDetail = () => {
  const { id } = useParams();

  const [book, setBook] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [showModal, setShowModal] =
    useState(false);

  useEffect(() => {
    const fetchBook =
      async () => {
        try {
          const data =
            await getBook(id);

          setBook(data);
        } catch (error) {
          console.log(error);
        } finally {
          setLoading(false);
        }
      };

    fetchBook();
  }, [id]);

  if (loading) {
    return (
      <MainLayout>
        <div>
          Loading book...
        </div>
      </MainLayout>
    );
  }

  if (!book) {
    return (
      <MainLayout>
        <div>
          Book not found.
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="bg-white rounded-2xl border border-gray-200 p-8">
        <div className="grid lg:grid-cols-3 gap-10">
          <div>
            {book.cover_image ? (
              <img
                src={
                  book.cover_image
                }
                alt={book.title}
                className="w-full rounded-xl"
              />
            ) : (
              <div className="aspect-[3/4] bg-gray-100 rounded-xl flex items-center justify-center text-gray-400">
                No Cover
              </div>
            )}
          </div>

          <div className="lg:col-span-2">
            <h1 className="text-4xl font-bold">
              {book.title}
            </h1>

            <p className="mt-3 text-lg text-gray-600">
              {book.author}
            </p>

            <div className="flex flex-wrap gap-3 mt-6">
              <span className="bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full text-sm">
                {book.genre}
              </span>

              <span className="bg-gray-100 px-3 py-1 rounded-full text-sm">
                Published:
                {" "}
                {
                  book.publication_date
                }
              </span>
            </div>

            <div className="mt-8">
              <h2 className="font-semibold text-xl mb-3">
                Description
              </h2>

              <p className="text-gray-600 leading-relaxed">
                {book.description ||
                  "No description available."}
              </p>
            </div>

            <div className="mt-10 flex gap-4 flex-wrap">
              {book.pdf_file && (
                <a
                  href={
                    book.pdf_file
                  }
                  target="_blank"
                  rel="noreferrer"
                  className="bg-yellow-400 hover:bg-yellow-500 px-5 py-3 rounded-lg font-medium"
                >
                  Read PDF
                </a>
              )}

              <button
                onClick={() =>
                  setShowModal(true)
                }
                className="bg-gray-100 hover:bg-gray-200 px-5 py-3 rounded-lg font-medium"
              >
                Add To Reading List
              </button>
            </div>
          </div>
        </div>
      </div>

      <AddToReadingListModal
        open={showModal}
        onClose={() =>
          setShowModal(false)
        }
        bookId={book.id}
      />
    </MainLayout>
  );
};

export default BookDetail;
import { Link } from "react-router-dom";

const BookCard = ({ book }) => {
  return (
    <Link
      to={`/books/${book.id}`}
      className="bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-md transition"
    >
      <div className="aspect-[3/4] bg-gray-100">
        {book.cover_image ? (
          <img
            src={book.cover_image}
            alt={book.title}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="h-full flex items-center justify-center text-gray-400">
            No Cover
          </div>
        )}
      </div>

      <div className="p-4">
        <h3 className="font-semibold line-clamp-1">
          {book.title}
        </h3>

        <p className="text-sm text-gray-500 mt-1">
          {book.author}
        </p>

        <span className="inline-block mt-3 px-2 py-1 rounded bg-yellow-100 text-yellow-700 text-xs">
          {book.genre}
        </span>
      </div>
    </Link>
  );
};

export default BookCard;
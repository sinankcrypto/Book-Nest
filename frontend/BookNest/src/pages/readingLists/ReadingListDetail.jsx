import {
  useEffect,
  useState,
} from "react";

import {
  useParams,
} from "react-router-dom";

import toast from "react-hot-toast";

import MainLayout from "../../layouts/MainLayout";

import {
  getReadingListDetail,
  removeBookFromReadingList,
} from "../../services/readingListService";

const ReadingListDetail = () => {
  const { id } = useParams();

  const [list, setList] =
    useState(null);

  const fetchList =
    async () => {
      try {
        const data =
          await getReadingListDetail(
            id
          );

        setList(data);
      } catch (error) {
        console.log(error);
      }
    };

  useEffect(() => {
    fetchList();
  }, [id]);

  const handleRemove =
    async (bookId) => {
      try {
        await removeBookFromReadingList(
          id,
          bookId
        );

        toast.success(
          "Book removed"
        );

        fetchList();
      } catch {
        toast.error(
          "Failed to remove book"
        );
      }
    };

  if (!list)
    return (
      <MainLayout>
        Loading...
      </MainLayout>
    );

  return (
    <MainLayout>
      <div>
        <h1 className="text-3xl font-bold mb-8">
          {list.name}
        </h1>

        <div className="space-y-4">
          {list.books?.map(
            (item) => (
              <div
                key={item.id}
                className="bg-white border border-gray-200 rounded-xl p-4 flex justify-between items-center"
              >
                <div className="flex items-center gap-4">
                  {item.cover_image ? (
                    <img
                      src={item.cover_image}
                      alt={item.title}
                      className="w-16 h-24 object-cover rounded-lg"
                    />
                  ) : (
                    <div className="w-16 h-24 bg-gray-100 rounded-lg flex items-center justify-center text-xs text-gray-400">
                      No Cover
                    </div>
                  )}

                  <div>
                    <h3 className="font-semibold">
                      {item.title}
                    </h3>

                    <p className="text-sm text-gray-500">
                      Position: {item.position}
                    </p>
                  </div>
                </div>

                <button
                  onClick={() =>
                    handleRemove(item.book)
                  }
                  className="bg-red-100 text-red-600 px-4 py-2 rounded-lg"
                >
                  Remove
                </button>
              </div>
            )
          )}
        </div>
      </div>
    </MainLayout>
  );
};

export default ReadingListDetail;
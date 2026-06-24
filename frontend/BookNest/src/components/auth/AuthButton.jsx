const AuthButton = ({
  children,
  loading,
  ...props
}) => {
  return (
    <button
      {...props}
      disabled={loading}
      className="
        w-full
        py-3.5
        rounded-xl
        bg-gradient-to-r
        from-amber-500
        to-yellow-500
        text-white
        font-semibold
        shadow-lg
        shadow-amber-200/50
        transition-all
        duration-200
        hover:from-amber-600
        hover:to-yellow-600
        hover:-translate-y-0.5
        hover:shadow-xl
        hover:shadow-amber-300/50
        active:translate-y-0
        disabled:opacity-70
        disabled:cursor-not-allowed
        disabled:hover:translate-y-0
        disabled:hover:shadow-lg
      "
    >
      {loading ? (
        <span className="flex items-center justify-center gap-2">
          <svg
            className="w-5 h-5 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
            />
          </svg>
          Please wait...
        </span>
      ) : (
        children
      )}
    </button>
  );
};

export default AuthButton;
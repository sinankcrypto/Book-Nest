const AuthInput = ({
  label,
  type = "text",
  value,
  onChange,
  placeholder,
  disabled,
  autoComplete,
  name,
}) => {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-gray-700">
        {label}
      </label>

      <input
        type={type}
        name={name}
        value={value}
        placeholder={placeholder}
        onChange={onChange}
        disabled={disabled}
        autoComplete={autoComplete}
        className="
          w-full
          rounded-xl
          border
          border-gray-200
          bg-gray-50
          px-4
          py-3
          text-gray-900
          placeholder:text-gray-400
          transition-all
          duration-200
          outline-none
          focus:bg-white
          focus:border-amber-400
          focus:ring-4
          focus:ring-amber-100
          disabled:opacity-60
          disabled:cursor-not-allowed
        "
      />
    </div>
  );
};

export default AuthInput;
import { BookOpen } from "lucide-react";

const AuthLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-white to-yellow-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="bg-white/90 backdrop-blur-sm border border-amber-100 rounded-3xl shadow-xl p-8">
          <div className="text-center mb-8">
            <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-amber-100 flex items-center justify-center">
              <BookOpen className="w-8 h-8 text-amber-600" />
            </div>

            <h1 className="text-4xl font-bold text-gray-900">
              BookNest
            </h1>

            <p className="mt-3 text-gray-500">
              Build your personal digital library
            </p>
          </div>

          {children}
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
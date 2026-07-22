import Link from "next/link";

import { AuthForm } from "@/components/auth-form";

export default function SignUpPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-md items-center px-4">
      <div className="w-full space-y-4">
        <AuthForm mode="signup" />
        <p className="text-center text-sm text-zinc-600 dark:text-zinc-400">
          Already have an account?{" "}
          <Link href="/signin" className="text-brand-700 hover:underline dark:text-brand-200">
            Sign in
          </Link>
        </p>
      </div>
    </main>
  );
}


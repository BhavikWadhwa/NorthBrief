import Link from "next/link";

import { AuthForm } from "@/components/auth-form";

export default function SignInPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-md items-center px-4">
      <div className="w-full space-y-4">
        <AuthForm mode="signin" />
        <p className="text-center text-sm text-zinc-600 dark:text-zinc-400">
          New here?{" "}
          <Link href="/signup" className="text-brand-700 hover:underline dark:text-brand-200">
            Create an account
          </Link>
        </p>
      </div>
    </main>
  );
}

